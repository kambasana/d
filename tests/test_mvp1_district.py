from __future__ import annotations

import socket
import time
from datetime import timedelta

import pytest

from awg_mvp1 import SimulationKernel, building_occupancy, load_reference_bundle, semantic_clusters
from awg_mvp1.bundle import BundleError
from awg_mvp1.kernel import CommandRejected, _format_time
from awg_mvp1.model import TravelCommand
from scripts.build_mvp1_pmtiles import build_archive


def _command(kernel: SimulationKernel, destination: str, mode: str = "walk") -> TravelCommand:
    agent = kernel.agents["agent:district-0000"]
    return TravelCommand(
        command_id="command:test-travel",
        actor_id=agent.agent_id,
        origin_place_id=agent.place_id,
        destination_place_id=destination,
        transport_mode=mode,
        issued_at=_format_time(kernel.now),
    )


def test_offline_bundle_contains_coherent_spatial_assets() -> None:
    bundle = load_reference_bundle()
    assert bundle.population == 100
    assert bundle.manifest["external_network_dependencies"] == []
    assert bundle.manifest["source_classification"] == "generated"
    assert bundle.search("civic")[0]["place_id"] == "place:office"
    assert (bundle.root / bundle.manifest["pmtiles_file"]).read_bytes() == build_archive()
    assert bundle.nodes[bundle.places["place:office"]["route_node_id"]].entrance_id == "entrance:office"


def test_routes_enforce_topology_modes_time_and_no_teleport() -> None:
    bundle = load_reference_bundle()
    kernel = SimulationKernel(bundle)
    with pytest.raises(CommandRejected, match="teleport"):
        kernel.submit_travel(_command(kernel, "place:office", mode="teleport"))
    with pytest.raises(CommandRejected, match="no wheelchair route"):
        kernel.submit_travel(_command(kernel, "place:cafe", mode="wheelchair"))

    route = kernel.submit_travel(_command(kernel, "place:office"))
    assert route.edge_ids == ("edge:home-a-square", "edge:square-office")
    assert route.distance_m == 950.0
    assert route.duration_seconds == 679
    assert kernel.agents["agent:district-0000"].place_id == "place:home-a"
    assert kernel.agents["agent:district-0000"].movement_state == "in_transit"

    kernel.run_until(kernel.now + timedelta(seconds=route.duration_seconds - 1))
    assert kernel.agents["agent:district-0000"].place_id == "place:home-a"
    kernel.run_until(kernel.now + timedelta(seconds=1))
    assert kernel.agents["agent:district-0000"].place_id == "place:office"


def test_building_entry_uses_route_entrance_and_updates_occupancy() -> None:
    bundle = load_reference_bundle()
    kernel = SimulationKernel(bundle)
    route = kernel.submit_travel(_command(kernel, "place:office"))
    kernel.run_until(kernel.now + timedelta(seconds=route.duration_seconds))

    entered = next(event for event in kernel.firehose if event.event_type == "LocationEntered")
    assert entered.payload["entrance_id"] == "entrance:office"
    assert entered.payload["route_node_id"] == "1004"
    assert "agent:district-0000" in kernel.occupancy["building:office"]
    assert "agent:district-0000" not in kernel.occupancy["building:home-a"]
    assert "agent:district-0000" in kernel.smart_object_occupancy["object:office-desks"]
    assert kernel.state_integrity_errors() == []


def test_snapshot_and_immutable_firehose_replay_to_identical_state() -> None:
    bundle = load_reference_bundle()
    kernel = SimulationKernel(bundle)
    kernel.run_24_hours()
    snapshot = kernel.snapshot()
    replayed = SimulationKernel.replay(bundle, kernel.firehose)

    assert isinstance(kernel.firehose, tuple)
    assert replayed.state_checksum() == snapshot.state_checksum
    assert replayed.snapshot().event_digest == snapshot.event_digest
    assert replayed.state_integrity_errors() == []


def test_semantic_zoom_and_occupancy_are_read_only_projections() -> None:
    bundle = load_reference_bundle()
    kernel = SimulationKernel(bundle)
    kernel.run_until(kernel.now + timedelta(hours=10))
    checksum = kernel.state_checksum()

    district_clusters = semantic_clusters(kernel.agents, bundle, zoom=10)
    place_clusters = semantic_clusters(kernel.agents, bundle, zoom=14)
    colocated_clusters = semantic_clusters(kernel.agents, bundle, zoom=17)
    office = building_occupancy("building:office", kernel.agents, bundle)

    assert len(district_clusters) == 1
    assert district_clusters[0]["member_count"] == 100
    assert len(place_clusters) == 2
    assert {cluster["cluster_type"] for cluster in colocated_clusters} == {"co_location"}
    assert office["occupant_count"] == 50
    assert office["floors"][0]["rooms"]["room:office-main"]["occupant_count"] == 50
    assert kernel.state_checksum() == checksum


def test_24_hour_target_population_runs_offline_without_integrity_failures(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def network_denied(*args: object, **kwargs: object) -> None:
        raise AssertionError("MVP 1 runtime attempted external networking")

    monkeypatch.setattr(socket, "create_connection", network_denied)
    started = time.perf_counter()
    bundle = load_reference_bundle()
    kernel = SimulationKernel(bundle)
    kernel.run_24_hours()
    elapsed = time.perf_counter() - started

    assert bundle.population == bundle.manifest["target_population"] == 100
    assert len(kernel.firehose) == 1400
    assert all(agent.movement_state == "stationary" for agent in kernel.agents.values())
    assert all(
        kernel.agents[agent.agent_id].place_id == agent.place_id for agent in bundle.initial_agents
    )
    assert kernel.state_integrity_errors() == []
    assert elapsed < 5.0


def test_bundle_rejects_checksum_drift(tmp_path) -> None:
    source = load_reference_bundle().root
    copied = tmp_path / "district"
    import shutil

    shutil.copytree(source, copied)
    (copied / "gazetteer.json").write_text("[]", encoding="utf-8")
    with pytest.raises(BundleError, match="checksum mismatch"):
        load_reference_bundle(copied)
