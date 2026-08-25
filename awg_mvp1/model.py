from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class RouteNode:
    node_id: str
    longitude: float
    latitude: float
    place_id: str | None = None
    entrance_id: str | None = None


@dataclass(frozen=True, slots=True)
class RouteEdge:
    edge_id: str
    source: str
    target: str
    distance_m: float
    modes: tuple[str, ...]
    accessible: bool = True


@dataclass(frozen=True, slots=True)
class Route:
    route_id: str
    node_ids: tuple[str, ...]
    edge_ids: tuple[str, ...]
    distance_m: float
    duration_seconds: int


@dataclass(frozen=True, slots=True)
class TravelCommand:
    command_id: str
    actor_id: str
    origin_place_id: str
    destination_place_id: str
    transport_mode: str
    issued_at: str


@dataclass(frozen=True, slots=True)
class AgentState:
    agent_id: str
    place_id: str
    route_node_id: str
    building_id: str | None
    room_id: str | None
    movement_state: str = "stationary"
    journey_id: str | None = None


@dataclass(frozen=True, slots=True)
class DomainEvent:
    schema_version: str
    event_id: str
    event_type: str
    world_id: str
    scenario_id: str
    branch_id: str
    simulation_time: str
    sequence: int
    recorded_at: str
    actor_id: str | None
    target_ids: tuple[str, ...]
    command_id: str | None
    parent_event_ids: tuple[str, ...]
    caused_by_event_ids: tuple[str, ...]
    location: dict[str, Any]
    payload: dict[str, Any]

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class Snapshot:
    schema_version: str
    world_id: str
    scenario_id: str
    branch_id: str
    simulation_time: str
    sequence: int
    event_digest: str
    state_checksum: str
    agents: tuple[AgentState, ...]
    occupancy: tuple[tuple[str, tuple[str, ...]], ...]
    smart_object_occupancy: tuple[tuple[str, tuple[str, ...]], ...]
