from __future__ import annotations

from typing import Any

from awg_mvp1 import building_occupancy, semantic_clusters
from awg_mvp1.kernel import SimulationKernel

from .bundle import ReviewBundle


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
