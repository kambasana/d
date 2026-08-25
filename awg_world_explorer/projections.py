from __future__ import annotations

from datetime import timedelta
from typing import Any

from awg_mvp1 import building_occupancy, semantic_clusters
from awg_mvp1.kernel import _format_time, _parse_time

from .bundle import ReviewBundle

PROJECTION_NOTICE = (
    "This bundle is a read-only review projection. Map clusters, PMTiles display tiles, "
    "and screen-space markers do not alter authoritative simulation state."
)


def world_projection(
    bundle: ReviewBundle,
    *,
    simulation_time: str,
    zoom: int,
    building_id: str | None = None,
) -> dict[str, Any]:
    """Build a read-only world projection without mutating kernel state."""
    kernel = bundle.spatial_kernel_at(simulation_time)
    checksum_before = kernel.state_checksum()
    district_bundle = kernel.bundle

    agents = [
        {
            "agent_id": agent.agent_id,
            "place_id": agent.place_id,
            "route_node_id": agent.route_node_id,
            "building_id": agent.building_id,
            "room_id": agent.room_id,
            "movement_state": agent.movement_state,
            "journey_id": agent.journey_id,
            "position_authority": "authoritative",
        }
        for agent in sorted(kernel.agents.values(), key=lambda item: item.agent_id)
    ]
    clusters = list(semantic_clusters(kernel.agents, district_bundle, zoom=zoom))
    occupancy = None
    if building_id:
        occupancy = building_occupancy(building_id, kernel.agents, district_bundle)

    checksum_after = kernel.state_checksum()
    if checksum_before != checksum_after:
        raise RuntimeError("projection mutated authoritative kernel state")

    return {
        "schema_version": bundle.schema_version,
        "simulation_time": simulation_time,
        "zoom": zoom,
        "world_id": kernel.world_id,
        "state_checksum": checksum_after,
        "agents": agents,
        "clusters": clusters,
        "building_occupancy": occupancy,
        "cluster_position_authority": "projection_only",
        "pmtiles_authority": "presentation_only",
        "read_only": True,
    }


def _display_name(agent_id: str) -> str:
    return agent_id.replace("agent:", "").replace("-", " ")


def _cluster_kind(cluster_type: str) -> str:
    if cluster_type == "co_location":
        return "co_location"
    return "geographic"


def ui_review_bundle(bundle: ReviewBundle) -> dict[str, Any]:
    """Compose the GET /api/review-bundle payload for the World Explorer UI."""
    kernel = bundle.spatial_kernel_at(bundle.end_time)
    checksum_before = kernel.state_checksum()
    district = kernel.bundle
    lons = [node.longitude for node in district.nodes.values()]
    lats = [node.latitude for node in district.nodes.values()]
    last_event_by_agent: dict[str, Any] = {}
    for event in bundle._mvp1_events:
        if event.actor_id:
            last_event_by_agent[event.actor_id] = event

    occupancy_by_building = {
        building_id: building_occupancy(building_id, kernel.agents, district)
        for building_id in sorted(district.buildings)
    }

    agents = []
    agent_details: dict[str, Any] = {}
    for agent in sorted(kernel.agents.values(), key=lambda item: item.agent_id):
        node = district.nodes[agent.route_node_id]
        place = district.places.get(agent.place_id, {})
        building = district.buildings.get(agent.building_id or "", {})
        last_event = last_event_by_agent.get(agent.agent_id)
        agents.append(
            {
                "agent_id": agent.agent_id,
                "display_name": _display_name(agent.agent_id),
                "longitude": node.longitude,
                "latitude": node.latitude,
                "place_id": agent.place_id,
                "building_id": agent.building_id,
                "status": agent.movement_state,
                "cluster_id": None,
            }
        )
        agent_details[agent.agent_id] = {
            "agent_id": agent.agent_id,
            "display_name": _display_name(agent.agent_id),
            "world_truth": {
                "current_place_id": agent.place_id,
                "current_place_name": place.get("name", agent.place_id),
                "building_id": agent.building_id,
                "building_name": building.get("name"),
                "journey_status": agent.movement_state,
                "coordinates": {"longitude": node.longitude, "latitude": node.latitude},
                "occupancy_zone": agent.room_id,
                "last_event_id": last_event.event_id if last_event else "",
                "last_event_summary": (
                    f"{last_event.event_type} at {last_event.simulation_time}" if last_event else "none"
                ),
                "fidelity": "S4",
            },
            "agent_perspective": {
                "observed_place_name": place.get("name", agent.place_id),
                "belief_summary": (
                    "This agent has no global simulator knowledge. Unobserved claims remain unknown."
                ),
                "confidence": 0.55,
                "claims": [],
                "knowledge_gaps": [
                    "World-truth claims not on an observation path are unknown.",
                    "Likes and views are not beliefs.",
                ],
                "stale": False,
            },
        }

    street_clusters = semantic_clusters(kernel.agents, district, zoom=14)
    district_clusters = semantic_clusters(kernel.agents, district, zoom=12)
    clusters = []
    for item, visible_at in (
        *[(cluster, ["street", "building"]) for cluster in street_clusters],
        *[(cluster, ["district"]) for cluster in district_clusters],
    ):
        centroid = item["representative_location"]
        clusters.append(
            {
                "cluster_id": item["cluster_id"],
                "kind": _cluster_kind(item["cluster_type"]),
                "label": f"{item['cluster_type']} ({item['member_count']})",
                "count": item["member_count"],
                "centroid": {
                    "longitude": centroid["longitude"],
                    "latitude": centroid["latitude"],
                },
                "visible_at": visible_at,
                "member_agent_ids": item["member_agent_ids"],
                "member_building_ids": sorted(
                    {
                        kernel.agents[agent_id].building_id
                        for agent_id in item["member_agent_ids"]
                        if kernel.agents[agent_id].building_id
                    }
                ),
                "projection_notice": "Display cluster only; not authoritative geography.",
            }
        )
        for agent_id in item["member_agent_ids"]:
            for summary in agents:
                if summary["agent_id"] == agent_id and summary["cluster_id"] is None:
                    summary["cluster_id"] = item["cluster_id"]

    buildings = []
    for building_id, building in sorted(district.buildings.items()):
        occupancy = occupancy_by_building[building_id]
        floors = [
            {
                "floor_id": floor["floor_id"],
                "level": floor["level"],
                "label": f"Level {floor['level']}",
                "occupancy": floor["occupant_count"],
                "room_ids": list(floor["rooms"]),
            }
            for floor in occupancy["floors"]
        ]
        entrance = building["entrances"][0]["route_node_id"]
        buildings.append(
            {
                "building_id": building_id,
                "name": building["name"],
                "route_node_id": entrance,
                "capacity": building["capacity"],
                "occupancy": occupancy["occupant_count"],
                "floors": floors,
            }
        )

    firehose = []
    for event in bundle._mvp1_events[-80:]:
        location = event.location or {}
        firehose.append(
            {
                "event_id": event.event_id,
                "sequence": event.sequence,
                "simulation_time": event.simulation_time,
                "event_type": event.event_type,
                "actor_id": event.actor_id,
                "place_id": location.get("place_id"),
                "summary": f"{event.event_type} seq={event.sequence}",
                "causal_parent_ids": list(event.parent_event_ids),
            }
        )

    start = _parse_time(bundle.start_time)
    end = _parse_time(bundle.end_time)
    span_hours = max(1, int((end - start).total_seconds() // 3600))
    tick_hours = (0, span_hours // 4, span_hours // 2, (3 * span_hours) // 4, span_hours)
    ticks = []
    for index, hour in enumerate(tick_hours):
        simulation_time = _format_time(start + timedelta(hours=hour))
        ticks.append(
            {
                "tick_index": index,
                "simulation_time": simulation_time,
                "label": f"H+{hour}",
                "is_historical_projection": hour < span_hours,
                "event_count": sum(
                    1 for event in bundle._mvp1_events if event.simulation_time <= simulation_time
                ),
            }
        )

    info = bundle._mvp4_kernel
    scale = bundle.scale_summary()
    journeys = sum(1 for agent in kernel.agents.values() if agent.journey_id)

    if kernel.state_checksum() != checksum_before:
        raise RuntimeError("UI review bundle mutated authoritative kernel state")

    return {
        "schema_version": bundle.schema_version,
        "bundle_id": bundle.bundle_id,
        "projection_notice": PROJECTION_NOTICE,
        "world": {
            "world_id": kernel.world_id,
            "scenario_id": kernel.scenario_id,
            "branch_id": kernel.branch_id,
            "district_id": district.manifest["district_id"],
            "district_name": "MVP 1 synthetic reference district",
            "simulation_time": bundle.end_time,
            "start_time": bundle.start_time,
            "end_time": bundle.end_time,
            "run_state": "completed",
            "source_classification": "synthetic",
            "agent_count": len(agents),
        },
        "map_projection": {
            "kind": "maplibre_geojson",
            "authority": "projection_only",
            "pmtiles_available": True,
            "pmtiles_label": "PMTiles display archive (presentation only — not routing or world authority)",
            "notice": (
                "MapLibre renders district GeoJSON for review. "
                "PMTiles and cluster markers are visualization projections only. "
                "Authoritative positions remain in simulation state."
            ),
        },
        "semantic_zoom": {
            "default_level": "district",
            "levels": [
                {
                    "id": "district",
                    "label": "District",
                    "description": "Geographic clusters and corridor flows across the reference district.",
                    "min_agent_marker_px": 0,
                },
                {
                    "id": "street",
                    "label": "Street",
                    "description": "Smaller clusters, individual agents, and building occupancy badges.",
                    "min_agent_marker_px": 8,
                },
                {
                    "id": "building",
                    "label": "Building",
                    "description": "Floor and room occupancy drill-down for selected buildings.",
                    "min_agent_marker_px": 12,
                },
            ],
        },
        "district": {
            "bounds": {
                "min_lon": min(lons),
                "max_lon": max(lons),
                "min_lat": min(lats),
                "max_lat": max(lats),
            },
            "nodes": [
                {
                    "node_id": node.node_id,
                    "longitude": node.longitude,
                    "latitude": node.latitude,
                    **({"place_id": node.place_id} if node.place_id else {}),
                }
                for node in sorted(district.nodes.values(), key=lambda item: item.node_id)
            ],
            "edges": [
                {
                    "edge_id": edge.edge_id,
                    "source": edge.source,
                    "target": edge.target,
                    "distance_m": edge.distance_m,
                    "accessible": edge.accessible,
                }
                for edge in district.edges
            ],
            "places": [
                {
                    "place_id": place["place_id"],
                    "name": place["name"],
                    "route_node_id": place["route_node_id"],
                    **({"building_id": place["building_id"]} if place.get("building_id") else {}),
                }
                for place in district.places.values()
            ],
            "buildings": buildings,
        },
        "clusters": clusters,
        "agents": agents,
        "agent_details": agent_details,
        "firehose": firehose,
        "timeline": {"ticks": ticks, "default_tick_index": len(ticks) - 1},
        "information_space": {
            "channels": [
                {
                    "channel_id": "channel:local-feed",
                    "label": "Local feed",
                    "message_count": len(info.posts),
                    "reach_estimate": len(info.actors),
                    "classification": "synthetic",
                }
            ],
            "exposure_edges": sum(len(value) for value in info.exposed.values()),
            "claim_count": len(info.claims),
            "disputed_claim_count": 0,
            "notice": (
                "Likes, views, and follows are not belief. "
                "Analyst world-truth is not shown in participant mode."
            ),
        },
        "scale_summary": {
            "current_level": "district",
            "population_visible": len(agents),
            "population_total": scale["totals"]["population_records"],
            "cluster_count": len(clusters),
            "building_count": len(buildings),
            "active_journeys": journeys,
            "projection_density": "reference-district",
        },
        "read_only": True,
        "mutation_allowed": False,
    }
