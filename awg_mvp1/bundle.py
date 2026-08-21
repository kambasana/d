from __future__ import annotations

import hashlib
import json
import struct
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .model import AgentState, Route, RouteEdge, RouteNode

ROOT = Path(__file__).resolve().parents[1]
REFERENCE_BUNDLE = ROOT / "examples" / "mvp1-district"


class BundleError(ValueError):
    """Raised when an offline district bundle is incomplete or inconsistent."""


@dataclass(frozen=True, slots=True)
class DistrictBundle:
    root: Path
    manifest: dict[str, Any]
    nodes: dict[str, RouteNode]
    edges: tuple[RouteEdge, ...]
    adjacency: dict[str, tuple[RouteEdge, ...]]
    places: dict[str, dict[str, Any]]
    buildings: dict[str, dict[str, Any]]
    smart_objects: dict[str, dict[str, Any]]
    gazetteer: tuple[dict[str, Any], ...]
    initial_agents: tuple[AgentState, ...]

    @property
    def population(self) -> int:
        return len(self.initial_agents)

    def route(self, origin_place_id: str, destination_place_id: str, mode: str) -> Route:
        import heapq

        if mode not in self.manifest["transport_speeds_mps"]:
            raise BundleError(f"unsupported transport mode: {mode}")
        source = self.places[origin_place_id]["route_node_id"]
        target = self.places[destination_place_id]["route_node_id"]
        frontier: list[tuple[float, str, tuple[str, ...], tuple[str, ...]]] = [(0.0, source, (source,), ())]
        best: dict[str, float] = {source: 0.0}
        while frontier:
            distance, node_id, node_path, edge_path = heapq.heappop(frontier)
            if distance != best.get(node_id):
                continue
            if node_id == target:
                speed = float(self.manifest["transport_speeds_mps"][mode])
                duration = max(1, int((distance / speed) + 0.999999))
                digest = hashlib.sha256("|".join(edge_path).encode()).hexdigest()[:16]
                return Route(
                    route_id=f"route:{digest}",
                    node_ids=node_path,
                    edge_ids=edge_path,
                    distance_m=distance,
                    duration_seconds=duration,
                )
            for edge in self.adjacency.get(node_id, ()):
                if not edge.accessible or mode not in edge.modes:
                    continue
                next_distance = distance + edge.distance_m
                if next_distance < best.get(edge.target, float("inf")):
                    best[edge.target] = next_distance
                    heapq.heappush(
                        frontier,
                        (next_distance, edge.target, node_path + (edge.target,), edge_path + (edge.edge_id,)),
                    )
        raise BundleError(f"no {mode} route from {origin_place_id} to {destination_place_id}")

    def search(self, query: str) -> tuple[dict[str, Any], ...]:
        normalized = query.casefold().strip()
        return tuple(
            record
            for record in self.gazetteer
            if normalized in record["display_name"].casefold()
            or any(normalized in alias.casefold() for alias in record.get("aliases", []))
        )


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _validate_pmtiles(path: Path) -> None:
    data = path.read_bytes()
    if len(data) < 127 or data[:7] != b"PMTiles" or data[7] != 3:
        raise BundleError("map archive is not PMTiles v3")
    values = struct.unpack_from("<11Q", data, 8)
    root_offset, root_length, metadata_offset, metadata_length, _, _, tile_offset, tile_length, *counts = values
    if root_offset < 127 or root_length == 0 or metadata_length == 0 or tile_length == 0:
        raise BundleError("PMTiles archive has an empty required section")
    for offset, length in (
        (root_offset, root_length),
        (metadata_offset, metadata_length),
        (tile_offset, tile_length),
    ):
        if offset + length > len(data):
            raise BundleError("PMTiles section exceeds archive length")
    if any(count < 1 for count in counts):
        raise BundleError("PMTiles archive contains no addressed tile")


def _validate_osm(path: Path, expected_nodes: set[str]) -> None:
    root = ET.parse(path).getroot()
    if root.tag != "osm":
        raise BundleError("OSM extract has no osm root")
    actual = {node.attrib["id"] for node in root.findall("node")}
    if not expected_nodes <= actual:
        raise BundleError("OSM extract does not contain every routing node")


def _build_agents(manifest: dict[str, Any], places: dict[str, dict[str, Any]]) -> tuple[AgentState, ...]:
    homes = tuple(manifest["home_place_ids"])
    agents: list[AgentState] = []
    for index in range(manifest["target_population"]):
        place_id = homes[index % len(homes)]
        place = places[place_id]
        agents.append(
            AgentState(
                agent_id=f"agent:district-{index:04d}",
                place_id=place_id,
                route_node_id=place["route_node_id"],
                building_id=place.get("building_id"),
                room_id=place.get("room_id"),
            )
        )
    return tuple(agents)


def load_reference_bundle(root: Path = REFERENCE_BUNDLE) -> DistrictBundle:
    manifest = json.loads((root / "bundle.json").read_text(encoding="utf-8"))
    for relative_path, expected in manifest["checksums"].items():
        path = root / relative_path
        if not path.is_file():
            raise BundleError(f"missing offline asset: {relative_path}")
        if _sha256(path) != expected:
            raise BundleError(f"checksum mismatch for offline asset: {relative_path}")

    district = json.loads((root / manifest["district_file"]).read_text(encoding="utf-8"))
    gazetteer = tuple(json.loads((root / manifest["gazetteer_file"]).read_text(encoding="utf-8")))
    nodes = {item["node_id"]: RouteNode(**item) for item in district["nodes"]}
    raw_edges = tuple(
        RouteEdge(
            edge_id=item["edge_id"],
            source=item["source"],
            target=item["target"],
            distance_m=item["distance_m"],
            modes=tuple(item["modes"]),
            accessible=item.get("accessible", True),
        )
        for item in district["edges"]
    )
    edges = raw_edges + tuple(
        RouteEdge(
            edge_id=f"{edge.edge_id}:reverse",
            source=edge.target,
            target=edge.source,
            distance_m=edge.distance_m,
            modes=edge.modes,
            accessible=edge.accessible,
        )
        for edge in raw_edges
    )
    adjacency_lists: dict[str, list[RouteEdge]] = {}
    for edge in edges:
        if edge.source not in nodes or edge.target not in nodes:
            raise BundleError(f"edge {edge.edge_id} references an unknown node")
        adjacency_lists.setdefault(edge.source, []).append(edge)
    adjacency = {
        node_id: tuple(sorted(node_edges, key=lambda edge: (edge.target, edge.edge_id)))
        for node_id, node_edges in adjacency_lists.items()
    }
    places = {item["place_id"]: item for item in district["places"]}
    buildings = {item["building_id"]: item for item in district["buildings"]}
    smart_objects = {item["object_id"]: item for item in district["smart_objects"]}
    if {record["place_id"] for record in gazetteer} != set(places):
        raise BundleError("gazetteer and district place identities diverge")

    _validate_osm(root / manifest["osm_file"], set(nodes))
    _validate_pmtiles(root / manifest["pmtiles_file"])
    sql = (root / manifest["postgis_migration"]).read_text(encoding="utf-8")
    for required in ("CREATE EXTENSION IF NOT EXISTS postgis", "awg_route_node", "awg_route_edge", "geometry("):
        if required not in sql:
            raise BundleError(f"PostGIS migration lacks {required}")

    return DistrictBundle(
        root=root,
        manifest=manifest,
        nodes=nodes,
        edges=edges,
        adjacency=adjacency,
        places=places,
        buildings=buildings,
        smart_objects=smart_objects,
        gazetteer=gazetteer,
        initial_agents=_build_agents(manifest, places),
    )
