from __future__ import annotations

import hashlib
import heapq
import json
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from typing import Any

from .bundle import BundleError, DistrictBundle
from .model import AgentState, DomainEvent, Route, Snapshot, TravelCommand

UTC = timezone.utc


def _parse_time(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("simulation times must include an offset")
    return parsed.astimezone(UTC)


def _format_time(value: datetime) -> str:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


class CommandRejected(ValueError):
    """A typed command failed deterministic domain validation."""


class SimulationKernel:
    """Small event-driven kernel proving the bounded MVP 1 invariants."""

    def __init__(self, bundle: DistrictBundle) -> None:
        self.bundle = bundle
        self.world_id = bundle.manifest["world_id"]
        self.scenario_id = bundle.manifest["scenario_id"]
        self.branch_id = bundle.manifest["branch_id"]
        self.now = _parse_time(bundle.manifest["start_time"])
        self._agents = {agent.agent_id: agent for agent in bundle.initial_agents}
        self._initial_agents = bundle.initial_agents
        self._events: list[DomainEvent] = []
        self._calendar: list[tuple[datetime, int, str, dict[str, Any]]] = []
        self._calendar_sequence = 0
        self._occupancy = self._initial_occupancy()
        self._smart_object_occupancy = self._initial_smart_object_occupancy()
        self._schedule_daily_agents()

    @property
    def agents(self) -> dict[str, AgentState]:
        return dict(self._agents)

    @property
    def firehose(self) -> tuple[DomainEvent, ...]:
        return tuple(self._events)

    @property
    def occupancy(self) -> dict[str, tuple[str, ...]]:
        return {key: tuple(sorted(value)) for key, value in self._occupancy.items()}

    @property
    def smart_object_occupancy(self) -> dict[str, tuple[str, ...]]:
        return {key: tuple(sorted(value)) for key, value in self._smart_object_occupancy.items()}

    def _initial_occupancy(self) -> dict[str, set[str]]:
        occupancy = {building_id: set() for building_id in self.bundle.buildings}
        for agent in self._agents.values():
            if agent.building_id:
                occupancy[agent.building_id].add(agent.agent_id)
        return occupancy

    def _initial_smart_object_occupancy(self) -> dict[str, set[str]]:
        occupancy = {object_id: set() for object_id in self.bundle.smart_objects}
        for agent in self._agents.values():
            object_id = self._object_at_place(agent.place_id)
            if object_id:
                occupancy[object_id].add(agent.agent_id)
        return occupancy

    def _object_at_place(self, place_id: str) -> str | None:
        for object_id, smart_object in self.bundle.smart_objects.items():
            if smart_object["place_id"] == place_id:
                return object_id
        return None

    def _schedule(self, at: datetime, kind: str, payload: dict[str, Any]) -> None:
        self._calendar_sequence += 1
        heapq.heappush(self._calendar, (at, self._calendar_sequence, kind, payload))

    def _schedule_daily_agents(self) -> None:
        start = self.now
        work_places = tuple(self.bundle.manifest["work_place_ids"])
        for index, agent in enumerate(self.bundle.initial_agents):
            work_place = work_places[index % len(work_places)]
            minute_offset = index % 60
            self._schedule(
                start + timedelta(hours=8, minutes=minute_offset),
                "travel",
                {"agent_id": agent.agent_id, "destination_place_id": work_place, "leg": "outbound"},
            )
            self._schedule(
                start + timedelta(hours=17, minutes=minute_offset),
                "travel",
                {"agent_id": agent.agent_id, "destination_place_id": agent.place_id, "leg": "return"},
            )

    def _event(
        self,
        event_type: str,
        *,
        actor_id: str,
        command_id: str,
        location: dict[str, Any],
        payload: dict[str, Any],
        target_ids: tuple[str, ...] = (),
    ) -> DomainEvent:
        sequence = len(self._events) + 1
        event = DomainEvent(
            schema_version="0.2.0",
            event_id=f"event:mvp1-{sequence:08d}",
            event_type=event_type,
            world_id=self.world_id,
            scenario_id=self.scenario_id,
            branch_id=self.branch_id,
            simulation_time=_format_time(self.now),
            sequence=sequence,
            recorded_at=_format_time(self.now),
            actor_id=actor_id,
            target_ids=target_ids,
            command_id=command_id,
            parent_event_ids=(),
            caused_by_event_ids=(),
            location=location,
            payload=payload,
        )
        self._events.append(event)
        self._apply_event(event)
        return event

    def _apply_event(self, event: DomainEvent) -> None:
        if event.actor_id is None:
            return
        agent = self._agents[event.actor_id]
        if event.event_type == "LocationExited":
            building_id = event.payload.get("building_id")
            if building_id:
                self._occupancy[building_id].discard(agent.agent_id)
        elif event.event_type == "SmartObjectReleased":
            self._smart_object_occupancy[event.payload["object_id"]].discard(agent.agent_id)
        elif event.event_type == "JourneyStarted":
            self._agents[agent.agent_id] = replace(
                agent,
                movement_state="in_transit",
                journey_id=event.payload["journey_id"],
                building_id=None,
                room_id=None,
            )
        elif event.event_type == "LocationEntered":
            self._agents[agent.agent_id] = replace(
                agent,
                place_id=event.payload["place_id"],
                route_node_id=event.payload["route_node_id"],
                building_id=event.payload.get("building_id"),
                room_id=event.payload.get("room_id"),
            )
            building_id = event.payload.get("building_id")
            if building_id:
                self._occupancy[building_id].add(agent.agent_id)
        elif event.event_type == "SmartObjectOccupied":
            self._smart_object_occupancy[event.payload["object_id"]].add(agent.agent_id)
        elif event.event_type == "JourneyCompleted":
            self._agents[agent.agent_id] = replace(agent, movement_state="stationary", journey_id=None)

    def submit_travel(self, command: TravelCommand) -> Route:
        agent = self._agents.get(command.actor_id)
        if agent is None:
            raise CommandRejected("unknown actor")
        if command.transport_mode == "teleport":
            raise CommandRejected("teleport is not a transport mode")
        if agent.movement_state != "stationary":
            raise CommandRejected("actor already has an active journey")
        if command.origin_place_id != agent.place_id:
            raise CommandRejected("command origin does not match authoritative position")
        if _parse_time(command.issued_at) > self.now:
            raise CommandRejected("command was issued in the future")
        try:
            route = self.bundle.route(
                command.origin_place_id,
                command.destination_place_id,
                command.transport_mode,
            )
        except (BundleError, KeyError) as exc:
            raise CommandRejected(str(exc)) from exc
        destination = self.bundle.places[command.destination_place_id]
        destination_node = self.bundle.nodes[route.node_ids[-1]]
        building_id = destination.get("building_id")
        if building_id:
            entrances = {item["entrance_id"] for item in self.bundle.buildings[building_id]["entrances"]}
            if destination_node.entrance_id not in entrances:
                raise CommandRejected("route does not terminate at a valid building entrance")

        journey_id = command.command_id.replace("command:", "journey:", 1)
        origin_location = self._location(agent.place_id)
        self._event(
            "LocationExited",
            actor_id=agent.agent_id,
            command_id=command.command_id,
            location=origin_location,
            target_ids=tuple(filter(None, (agent.building_id,))),
            payload={
                "place_id": agent.place_id,
                "building_id": agent.building_id,
                "room_id": agent.room_id,
                "via_route_node_id": agent.route_node_id,
            },
        )
        object_id = self._object_at_place(agent.place_id)
        if object_id:
            self._event(
                "SmartObjectReleased",
                actor_id=agent.agent_id,
                command_id=command.command_id,
                location=origin_location,
                target_ids=(object_id,),
                payload={"object_id": object_id},
            )
        expected_arrival = self.now + timedelta(seconds=route.duration_seconds)
        self._event(
            "JourneyStarted",
            actor_id=agent.agent_id,
            command_id=command.command_id,
            location=origin_location,
            target_ids=(journey_id, command.destination_place_id),
            payload={
                "journey_id": journey_id,
                "origin": origin_location,
                "destination": self._location(command.destination_place_id),
                "transport_mode": command.transport_mode,
                "route_id": route.route_id,
                "route_node_ids": list(route.node_ids),
                "route_edge_ids": list(route.edge_ids),
                "distance_m": route.distance_m,
                "duration_seconds": route.duration_seconds,
                "expected_arrival": _format_time(expected_arrival),
            },
        )
        self._schedule(
            expected_arrival,
            "arrival",
            {
                "command": command,
                "journey_id": journey_id,
                "route": route,
                "destination_place_id": command.destination_place_id,
            },
        )
        return route

    def _location(self, place_id: str) -> dict[str, Any]:
        place = self.bundle.places[place_id]
        node = self.bundle.nodes[place["route_node_id"]]
        result: dict[str, Any] = {
            "place_id": place_id,
            "coordinates": {"longitude": node.longitude, "latitude": node.latitude},
            "precision": "room" if place.get("room_id") else "exact",
        }
        for field in ("building_id", "room_id"):
            if place.get(field):
                result[field] = place[field]
        return result

    def _process_travel(self, payload: dict[str, Any]) -> None:
        agent = self._agents[payload["agent_id"]]
        command = TravelCommand(
            command_id=f"command:{payload['leg']}:{agent.agent_id}:{int(self.now.timestamp())}",
            actor_id=agent.agent_id,
            origin_place_id=agent.place_id,
            destination_place_id=payload["destination_place_id"],
            transport_mode="walk",
            issued_at=_format_time(self.now),
        )
        self.submit_travel(command)

    def _process_arrival(self, payload: dict[str, Any]) -> None:
        command: TravelCommand = payload["command"]
        route: Route = payload["route"]
        destination = self.bundle.places[payload["destination_place_id"]]
        location = self._location(destination["place_id"])
        self._event(
            "JourneyArrived",
            actor_id=command.actor_id,
            command_id=command.command_id,
            location=location,
            target_ids=(payload["journey_id"], destination["place_id"]),
            payload={
                "journey_id": payload["journey_id"],
                "route_id": route.route_id,
                "via_route_node_id": route.node_ids[-1],
            },
        )
        self._event(
            "LocationEntered",
            actor_id=command.actor_id,
            command_id=command.command_id,
            location=location,
            target_ids=tuple(filter(None, (destination.get("building_id"), destination["place_id"]))),
            payload={
                "place_id": destination["place_id"],
                "route_node_id": route.node_ids[-1],
                "entrance_id": self.bundle.nodes[route.node_ids[-1]].entrance_id,
                "building_id": destination.get("building_id"),
                "room_id": destination.get("room_id"),
            },
        )
        object_id = self._object_at_place(destination["place_id"])
        if object_id:
            capacity = self.bundle.smart_objects[object_id]["capacity"]
            if len(self._smart_object_occupancy[object_id]) >= capacity:
                raise RuntimeError(f"smart-object capacity exceeded: {object_id}")
            self._event(
                "SmartObjectOccupied",
                actor_id=command.actor_id,
                command_id=command.command_id,
                location=location,
                target_ids=(object_id,),
                payload={"object_id": object_id},
            )
        self._event(
            "JourneyCompleted",
            actor_id=command.actor_id,
            command_id=command.command_id,
            location=location,
            target_ids=(payload["journey_id"], destination["place_id"]),
            payload={
                "journey_id": payload["journey_id"],
                "destination": location,
                "elapsed_seconds": route.duration_seconds,
                "route_revisions": 0,
            },
        )

    def run_until(self, end_time: str | datetime) -> None:
        end = _parse_time(end_time) if isinstance(end_time, str) else end_time.astimezone(UTC)
        if end < self.now:
            raise ValueError("simulation clock cannot move backwards")
        while self._calendar and self._calendar[0][0] <= end:
            at, _, kind, payload = heapq.heappop(self._calendar)
            self.now = at
            self._dispatch(kind, payload)
        self.now = end

    def _dispatch(self, kind: str, payload: dict[str, Any]) -> None:
        if kind == "travel":
            self._process_travel(payload)
        elif kind == "arrival":
            self._process_arrival(payload)
        else:
            raise RuntimeError(f"unknown scheduled action: {kind}")

    def run_24_hours(self) -> None:
        self.run_until(self.now + timedelta(hours=24))

    def _state_payload(self) -> dict[str, Any]:
        return {
            "agents": [
                {
                    "agent_id": agent.agent_id,
                    "place_id": agent.place_id,
                    "route_node_id": agent.route_node_id,
                    "building_id": agent.building_id,
                    "room_id": agent.room_id,
                    "movement_state": agent.movement_state,
                    "journey_id": agent.journey_id,
                }
                for agent in sorted(self._agents.values(), key=lambda item: item.agent_id)
            ],
            "occupancy": {key: sorted(value) for key, value in sorted(self._occupancy.items())},
            "smart_object_occupancy": {
                key: sorted(value) for key, value in sorted(self._smart_object_occupancy.items())
            },
        }

    def state_checksum(self) -> str:
        encoded = json.dumps(self._state_payload(), sort_keys=True, separators=(",", ":")).encode()
        return hashlib.sha256(encoded).hexdigest()

    def snapshot(self) -> Snapshot:
        event_bytes = json.dumps(
            [event.as_dict() for event in self._events],
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
        return Snapshot(
            schema_version="0.2.0",
            world_id=self.world_id,
            scenario_id=self.scenario_id,
            branch_id=self.branch_id,
            simulation_time=_format_time(self.now),
            sequence=len(self._events),
            event_digest=hashlib.sha256(event_bytes).hexdigest(),
            state_checksum=self.state_checksum(),
            agents=tuple(sorted(self._agents.values(), key=lambda item: item.agent_id)),
            occupancy=tuple(
                (key, tuple(sorted(value))) for key, value in sorted(self._occupancy.items())
            ),
            smart_object_occupancy=tuple(
                (key, tuple(sorted(value)))
                for key, value in sorted(self._smart_object_occupancy.items())
            ),
        )

    @classmethod
    def replay(cls, bundle: DistrictBundle, events: tuple[DomainEvent, ...]) -> SimulationKernel:
        replayed = cls(bundle)
        replayed._calendar.clear()
        replayed._events.clear()
        for expected_sequence, event in enumerate(events, start=1):
            if event.sequence != expected_sequence:
                raise ValueError("event sequence is not contiguous")
            replayed.now = _parse_time(event.simulation_time)
            replayed._events.append(event)
            replayed._apply_event(event)
        return replayed

    def state_integrity_errors(self) -> list[str]:
        errors: list[str] = []
        occupied_agents: set[str] = set()
        for building_id, agent_ids in self._occupancy.items():
            capacity = self.bundle.buildings[building_id]["capacity"]
            if len(agent_ids) > capacity:
                errors.append(f"{building_id} occupancy exceeds capacity")
            for agent_id in agent_ids:
                if agent_id in occupied_agents:
                    errors.append(f"{agent_id} occupies multiple buildings")
                occupied_agents.add(agent_id)
                if self._agents[agent_id].building_id != building_id:
                    errors.append(f"{agent_id} occupancy diverges from authoritative location")
        for object_id, agent_ids in self._smart_object_occupancy.items():
            if len(agent_ids) > self.bundle.smart_objects[object_id]["capacity"]:
                errors.append(f"{object_id} occupancy exceeds capacity")
        for expected, event in enumerate(self._events, start=1):
            if event.sequence != expected:
                errors.append("firehose sequence is not contiguous")
        for before, after in zip(self._events, self._events[1:]):
            if _parse_time(after.simulation_time) < _parse_time(before.simulation_time):
                errors.append("firehose simulation time moved backwards")
        return errors
