from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from awg_mvp1.bundle import DistrictBundle, load_reference_bundle
from awg_mvp1.kernel import CommandRejected, SimulationKernel, _format_time, _parse_time
from awg_mvp1.model import DomainEvent, TravelCommand

ROOT = Path(__file__).resolve().parents[1]
SOCIETY_PATH = ROOT / "examples" / "mvp2-npc" / "society.json"

ACTION_CHANNELS: dict[str, frozenset[str]] = {
    "travel": frozenset({"locomotion", "attention"}),
    "work": frozenset({"hands", "attention"}),
    "eat": frozenset({"hands", "attention"}),
    "sleep": frozenset({"locomotion", "hands", "attention", "posture"}),
}

VISIBLE_EVENT_TYPES = {
    "LocationEntered",
    "LocationExited",
    "JourneyStarted",
    "JourneyCompleted",
    "SmartObjectOccupied",
    "SmartObjectReleased",
    "SlotReserved",
    "ActionStarted",
    "ActionCompleted",
}


class NpcKernel(SimulationKernel):
    """Deterministic NPC stack: needs, utility, channels, ownership, perception."""

    def __init__(self, bundle: DistrictBundle | None = None, society_path: Path = SOCIETY_PATH) -> None:
        self.society = json.loads(society_path.read_text(encoding="utf-8"))
        super().__init__(bundle or load_reference_bundle())
        self.scenario_id = "scenario:mvp2-classical-npc"
        self._needs: dict[str, dict[str, float]] = {
            agent.agent_id: {"hunger": 0.35, "fatigue": 0.2} for agent in self._initial_agents
        }
        self._channels: dict[str, set[str]] = {agent.agent_id: set() for agent in self._initial_agents}
        self._current_action: dict[str, str | None] = {agent.agent_id: None for agent in self._initial_agents}
        self._inventories: dict[str, dict[str, int]] = {}
        self._owners: dict[str, str] = {}
        self._reservations: dict[str, str] = {}
        self._observations: dict[str, set[str]] = defaultdict(set)
        self._households: dict[str, str] = {}
        self._membership: dict[str, str] = {}
        self._last_need_time = self.now
        self._bootstrapped = False
        self._init_social_index()

    def _init_social_index(self) -> None:
        work_places = tuple(self.bundle.manifest["work_place_ids"])
        for index, agent in enumerate(self._initial_agents):
            household_id = f"household:{(index // 2) + 1:03d}"
            self._households[agent.agent_id] = household_id
            work_place = work_places[index % len(work_places)]
            org = next(
                item for item in self.society["organizations"] if work_place in item["place_ids"]
            )
            self._membership[agent.agent_id] = org["organization_id"]

    def _schedule_daily_agents(self) -> None:
        self._schedule(self.now, "npc_bootstrap", {})
        for hour in range(24):
            self._schedule(self.now + timedelta(hours=hour), "npc_tick", {"hour": hour})

    def _dispatch(self, kind: str, payload: dict[str, Any]) -> None:
        if kind == "npc_bootstrap":
            self._bootstrap()
        elif kind == "npc_tick":
            self._tick(int(payload["hour"]))
        elif kind == "npc_complete":
            self._complete_action(payload)
        else:
            super()._dispatch(kind, payload)

    def _holders(self) -> list[str]:
        ids = [agent.agent_id for agent in self._initial_agents]
        ids.extend(org["organization_id"] for org in self.society["organizations"])
        return ids

    def _bootstrap(self) -> None:
        if self._bootstrapped:
            return
        self._bootstrapped = True
        for org in self.society["organizations"]:
            self._grant(org["organization_id"], "token", int(org["starting_tokens"]))
            for asset_id in org["asset_ids"]:
                self._event(
                    "OwnershipTransferred",
                    actor_id=self._initial_agents[0].agent_id,
                    command_id="command:bootstrap-ownership",
                    location=self._location(self._initial_agents[0].place_id),
                    target_ids=(asset_id, org["organization_id"]),
                    payload={
                        "asset_id": asset_id,
                        "from_holder_id": None,
                        "to_holder_id": org["organization_id"],
                    },
                )
        for agent in self._initial_agents:
            self._grant(agent.agent_id, "token", int(self.society["starting_agent_tokens"]))
            self._grant(agent.agent_id, "meal", int(self.society["starting_agent_meals"]))

    def _grant(self, holder_id: str, resource_type: str, quantity: int) -> None:
        actor = holder_id if holder_id in self._agents else self._initial_agents[0].agent_id
        self._event(
            "ResourceGranted",
            actor_id=actor,
            command_id="command:bootstrap-resources",
            location=self._location(self._agents[actor].place_id),
            target_ids=(holder_id,),
            payload={"holder_id": holder_id, "resource_type": resource_type, "quantity": quantity},
        )

    def _advance_needs(self) -> None:
        elapsed_hours = max(0.0, (self.now - self._last_need_time).total_seconds() / 3600.0)
        if elapsed_hours <= 0:
            return
        hunger_rate = float(self.society["need_rates_per_hour"]["hunger"])
        fatigue_rate = float(self.society["need_rates_per_hour"]["fatigue"])
        for agent_id, needs in list(self._needs.items()):
            action = self._current_action.get(agent_id)
            if action == "sleep":
                fatigue = max(0.0, needs["fatigue"] - 0.4 * elapsed_hours)
            else:
                fatigue = min(1.0, needs["fatigue"] + fatigue_rate * elapsed_hours)
            if action == "eat":
                hunger = max(0.0, needs["hunger"] - 0.6 * elapsed_hours)
            else:
                hunger = min(1.0, needs["hunger"] + hunger_rate * elapsed_hours)
            if round(hunger, 6) != round(needs["hunger"], 6) or round(fatigue, 6) != round(needs["fatigue"], 6):
                self._set_needs(agent_id, hunger, fatigue)
        self._last_need_time = self.now

    def _set_needs(self, agent_id: str, hunger: float, fatigue: float) -> None:
        self._event(
            "NeedUpdated",
            actor_id=agent_id,
            command_id="command:need-update",
            location=self._location(self._agents[agent_id].place_id),
            payload={"hunger": hunger, "fatigue": fatigue},
        )

    def occupied_channels(self, agent_id: str) -> frozenset[str]:
        return frozenset(self._channels[agent_id])

    def can_start(self, agent_id: str, action: str) -> bool:
        requested = ACTION_CHANNELS[action]
        return self._channels[agent_id].isdisjoint(requested)

    def _claim_channels(self, agent_id: str, action: str, command_id: str) -> None:
        if not self.can_start(agent_id, action):
            raise CommandRejected(f"action {action} conflicts with occupied channels")
        self._channels[agent_id].update(ACTION_CHANNELS[action])
        self._current_action[agent_id] = action
        agent = self._agents[agent_id]
        self._event(
            "ActionStarted",
            actor_id=agent_id,
            command_id=command_id,
            location=self._location(agent.place_id),
            payload={"action": action, "channels": sorted(ACTION_CHANNELS[action])},
        )

    def _release_channels(self, agent_id: str, action: str, command_id: str) -> None:
        self._channels[agent_id].difference_update(ACTION_CHANNELS[action])
        if self._current_action.get(agent_id) == action:
            self._current_action[agent_id] = None
        agent = self._agents[agent_id]
        self._event(
            "ActionCompleted",
            actor_id=agent_id,
            command_id=command_id,
            location=self._location(agent.place_id),
            payload={"action": action},
        )

    def utility(self, agent_id: str, hour: int) -> dict[str, float]:
        needs = self._needs[agent_id]
        work_place = self._work_place(agent_id)
        night = hour >= 22 or hour < 6
        scores = {
            "sleep": needs["fatigue"] * 80.0 + (45.0 if night and needs["fatigue"] >= 0.5 else 0.0),
            "work": (85.0 if 8 <= hour < 17 else 0.0) - needs["hunger"] * 20.0,
            "eat": needs["hunger"] * 130.0 if needs["hunger"] >= 0.55 else needs["hunger"] * 5.0,
            "home": 18.0 + (12.0 if 17 <= hour < 22 else 0.0),
        }
        if work_place is None:
            scores["work"] = -100.0
        return scores

    def _work_place(self, agent_id: str) -> str:
        org_id = self._membership[agent_id]
        org = next(item for item in self.society["organizations"] if item["organization_id"] == org_id)
        return org["place_ids"][0]

    def _home_place(self, agent_id: str) -> str:
        return next(agent.place_id for agent in self._initial_agents if agent.agent_id == agent_id)

    def _tick(self, hour: int) -> None:
        self._advance_needs()
        for agent in self._initial_agents:
            if self._agents[agent.agent_id].movement_state != "stationary":
                continue
            if self._channels[agent.agent_id] or self._current_action.get(agent.agent_id):
                continue
            self._decide(agent.agent_id, hour)

    def _decide(self, agent_id: str, hour: int) -> None:
        ranked = sorted(self.utility(agent_id, hour).items(), key=lambda item: (-item[1], item[0]))
        goal = ranked[0][0]
        if goal == "eat":
            self._plan_eat(agent_id)
        elif goal == "sleep":
            self._plan_sleep(agent_id)
        elif goal == "work":
            self._plan_be_at(agent_id, self._work_place(agent_id), "work", duration_seconds=3600)
        else:
            self._plan_be_at(agent_id, self._home_place(agent_id), None, duration_seconds=0)

    def _plan_be_at(self, agent_id: str, place_id: str, action: str | None, duration_seconds: int) -> None:
        agent = self._agents[agent_id]
        if agent.place_id != place_id:
            self.start_travel(agent_id, place_id)
            return
        if action:
            command_id = f"command:{action}:{agent_id}:{int(self.now.timestamp())}"
            self._claim_channels(agent_id, action, command_id)
            self._schedule(
                self.now + timedelta(seconds=duration_seconds),
                "npc_complete",
                {"agent_id": agent_id, "action": action, "command_id": command_id},
            )

    def _plan_eat(self, agent_id: str) -> None:
        agent = self._agents[agent_id]
        home = self._home_place(agent_id)
        if self._inventories[agent_id]["meal"] >= 1 and agent.place_id == home:
            self._consume_meal(agent_id)
            return
        if self._inventories[agent_id]["meal"] >= 1 and agent.place_id != home:
            self.start_travel(agent_id, home)
            return
        if agent.place_id != "place:cafe":
            cafe_seating = self.bundle.smart_objects["object:cafe-seating"]["capacity"]
            occupying = len(self._smart_object_occupancy.get("object:cafe-seating", set()))
            pending = sum(
                1
                for item in self._calendar
                if item[2] == "arrival" and item[3].get("destination_place_id") == "place:cafe"
            )
            if occupying + pending >= cafe_seating:
                return
            self.start_travel(agent_id, "place:cafe")
            return
        try:
            self.reserve_slot(agent_id, "object:cafe-counter")
        except CommandRejected:
            return
        if self._inventories.get(agent_id, {}).get("token", 0) < 2:
            self.release_slot(agent_id, "object:cafe-counter")
            return
        self._pay(agent_id, "org:district-cafe", 2)
        command_id = f"command:eat:{agent_id}:{int(self.now.timestamp())}"
        self._claim_channels(agent_id, "eat", command_id)
        self._set_needs(agent_id, 0.0, self._needs[agent_id]["fatigue"])
        self._schedule(
            self.now + timedelta(minutes=20),
            "npc_complete",
            {
                "agent_id": agent_id,
                "action": "eat",
                "command_id": command_id,
                "release_object": "object:cafe-counter",
            },
        )

    def _plan_sleep(self, agent_id: str) -> None:
        home = self._home_place(agent_id)
        agent = self._agents[agent_id]
        if agent.place_id != home:
            self.start_travel(agent_id, home)
            return
        command_id = f"command:sleep:{agent_id}:{int(self.now.timestamp())}"
        self._claim_channels(agent_id, "sleep", command_id)
        self._schedule(
            self.now + timedelta(hours=1),
            "npc_complete",
            {"agent_id": agent_id, "action": "sleep", "command_id": command_id},
        )

    def _complete_action(self, payload: dict[str, Any]) -> None:
        agent_id = payload["agent_id"]
        action = payload["action"]
        if action == "sleep":
            self._set_needs(agent_id, self._needs[agent_id]["hunger"], 0.0)
        if payload.get("release_object"):
            self.release_slot(agent_id, payload["release_object"])
        self._release_channels(agent_id, action, payload["command_id"])

    def start_travel(self, agent_id: str, destination_place_id: str) -> None:
        agent = self._agents[agent_id]
        if agent.place_id == destination_place_id:
            return
        command_id = f"command:travel:{agent_id}:{int(self.now.timestamp())}:{destination_place_id}"
        self._claim_channels(agent_id, "travel", command_id)
        self.submit_travel(
            TravelCommand(
                command_id=command_id,
                actor_id=agent_id,
                origin_place_id=agent.place_id,
                destination_place_id=destination_place_id,
                transport_mode="walk",
                issued_at=_format_time(self.now),
            )
        )

    def submit_travel(self, command: TravelCommand):
        return super().submit_travel(command)

    def _process_arrival(self, payload: dict[str, Any]) -> None:
        super()._process_arrival(payload)
        actor_id = payload["command"].actor_id
        if "locomotion" in self._channels.get(actor_id, set()):
            self._release_channels(actor_id, "travel", payload["command"].command_id)

    def reserve_slot(self, agent_id: str, object_id: str) -> None:
        spec = next(item for item in self.society["exclusive_objects"] if item["object_id"] == object_id)
        agent = self._agents[agent_id]
        if agent.place_id != spec["place_id"]:
            raise CommandRejected("cannot reserve a smart object from another place")
        if self._reservations.get(agent_id) == object_id:
            return
        held = sum(1 for reserved in self._reservations.values() if reserved == object_id)
        if held >= spec["capacity"]:
            raise CommandRejected(f"{object_id} exclusive slot is already reserved")
        self._event(
            "SlotReserved",
            actor_id=agent_id,
            command_id=f"command:reserve:{object_id}",
            location=self._location(agent.place_id),
            target_ids=(object_id,),
            payload={"object_id": object_id, "affordance_id": spec["affordance_id"]},
        )

    def release_slot(self, agent_id: str, object_id: str) -> None:
        if self._reservations.get(agent_id) == object_id:
            del self._reservations[agent_id]
            self._event(
                "SlotReleased",
                actor_id=agent_id,
                command_id=f"command:release:{object_id}",
                location=self._location(self._agents[agent_id].place_id),
                target_ids=(object_id,),
                payload={"object_id": object_id},
            )

    def transfer_resource(
        self,
        from_holder_id: str,
        to_holder_id: str,
        resource_type: str,
        quantity: int,
        asset_id: str | None = None,
    ) -> None:
        if quantity < 1:
            raise CommandRejected("transfer quantity MUST be at least 1")
        if resource_type == "unique_asset":
            if not asset_id or self._owners.get(asset_id) != from_holder_id:
                raise CommandRejected("actor does not own the unique asset")
            actor = from_holder_id if from_holder_id in self._agents else self._initial_agents[0].agent_id
            self._event(
                "OwnershipTransferred",
                actor_id=actor,
                command_id="command:transfer-asset",
                location=self._location(self._agents[actor].place_id),
                target_ids=(asset_id, to_holder_id),
                payload={
                    "asset_id": asset_id,
                    "from_holder_id": from_holder_id,
                    "to_holder_id": to_holder_id,
                },
            )
            return
        available = self._inventories.get(from_holder_id, {}).get(resource_type, 0)
        if available < quantity:
            raise CommandRejected("insufficient resources")
        actor = from_holder_id if from_holder_id in self._agents else self._initial_agents[0].agent_id
        self._event(
            "ResourceTransferred",
            actor_id=actor,
            command_id="command:transfer-resource",
            location=self._location(self._agents[actor].place_id),
            target_ids=(from_holder_id, to_holder_id),
            payload={
                "from_holder_id": from_holder_id,
                "to_holder_id": to_holder_id,
                "resource_type": resource_type,
                "quantity": quantity,
            },
        )

    def _pay(self, agent_id: str, org_id: str, quantity: int) -> None:
        self.transfer_resource(agent_id, org_id, "token", quantity)

    def _consume_meal(self, agent_id: str) -> None:
        available = self._inventories[agent_id]["meal"]
        if available < 1:
            raise CommandRejected("no meal to consume")
        command_id = f"command:eat:{agent_id}:{int(self.now.timestamp())}"
        self._claim_channels(agent_id, "eat", command_id)
        self._set_needs(agent_id, 0.0, self._needs[agent_id]["fatigue"])
        self._event(
            "ResourceConsumed",
            actor_id=agent_id,
            command_id=command_id,
            location=self._location(self._agents[agent_id].place_id),
            payload={"holder_id": agent_id, "resource_type": "meal", "quantity": 1},
        )
        self._schedule(
            self.now + timedelta(minutes=15),
            "npc_complete",
            {"agent_id": agent_id, "action": "eat", "command_id": command_id},
        )

    def resource_totals(self) -> dict[str, int]:
        totals = {"token": 0, "meal": 0}
        for inventory in self._inventories.values():
            for resource_type in totals:
                totals[resource_type] += inventory.get(resource_type, 0)
        return totals

    def known_event_ids(self, agent_id: str) -> set[str]:
        return set(self._observations[agent_id])

    def knows(self, agent_id: str, event_id: str) -> bool:
        return event_id in self._observations[agent_id]

    def _event(self, event_type: str, **kwargs: Any) -> DomainEvent:
        event = super()._event(event_type, **kwargs)
        self._record_actor_knowledge(event)
        self._fanout_observations(event)
        return event

    def _record_actor_knowledge(self, event: DomainEvent) -> None:
        if event.actor_id:
            self._observations[event.actor_id].add(event.event_id)

    def _fanout_observations(self, event: DomainEvent) -> None:
        if event.event_type not in VISIBLE_EVENT_TYPES:
            return
        place_id = event.location.get("place_id")
        if not place_id:
            return
        for agent in self._agents.values():
            if agent.agent_id == event.actor_id:
                continue
            if agent.place_id != place_id or agent.movement_state != "stationary":
                continue
            observation_id = f"observation:{event.sequence}:{agent.agent_id}"
            self._observations[agent.agent_id].add(event.event_id)
            super()._event(
                "AgentObserved",
                actor_id=agent.agent_id,
                command_id=event.command_id or "command:perception",
                location=self._location(agent.place_id),
                target_ids=(event.actor_id,) if event.actor_id else (),
                payload={
                    "observer_id": agent.agent_id,
                    "observed_event_id": event.event_id,
                    "observation_id": observation_id,
                    "channel": "vision",
                    "fidelity": 0.9,
                    "uncertainty": 0.1,
                    "content": {"event_type": event.event_type},
                },
            )
            self._observations[agent.agent_id].add(self._events[-1].event_id)

    def _apply_event(self, event: DomainEvent) -> None:
        super()._apply_event(event)
        payload = event.payload
        if event.event_type == "NeedUpdated":
            self._needs[event.actor_id] = {
                "hunger": float(payload["hunger"]),
                "fatigue": float(payload["fatigue"]),
            }
        elif event.event_type == "ResourceGranted":
            holder_id = payload["holder_id"]
            self._inventories.setdefault(holder_id, {"token": 0, "meal": 0})
            self._inventories[holder_id][payload["resource_type"]] = self._inventories[holder_id].get(
                payload["resource_type"], 0
            ) + int(payload["quantity"])
        elif event.event_type == "ResourceTransferred":
            source = self._inventories.setdefault(payload["from_holder_id"], {"token": 0, "meal": 0})
            target = self._inventories.setdefault(payload["to_holder_id"], {"token": 0, "meal": 0})
            source[payload["resource_type"]] = source.get(payload["resource_type"], 0) - int(payload["quantity"])
            target[payload["resource_type"]] = target.get(payload["resource_type"], 0) + int(payload["quantity"])
        elif event.event_type == "ResourceConsumed":
            holder = self._inventories.setdefault(payload["holder_id"], {"token": 0, "meal": 0})
            holder[payload["resource_type"]] = holder.get(payload["resource_type"], 0) - int(payload["quantity"])
        elif event.event_type == "OwnershipTransferred" and payload.get("to_holder_id"):
            self._owners[payload["asset_id"]] = payload["to_holder_id"]
        elif event.event_type == "SlotReserved":
            self._reservations[event.actor_id] = payload["object_id"]
        elif event.event_type == "SlotReleased" and event.actor_id in self._reservations:
            del self._reservations[event.actor_id]
        elif event.event_type == "ActionStarted":
            self._channels.setdefault(event.actor_id, set()).update(payload.get("channels", []))
            self._current_action[event.actor_id] = payload.get("action")
        elif event.event_type == "ActionCompleted":
            action = payload.get("action")
            if action in ACTION_CHANNELS:
                self._channels.setdefault(event.actor_id, set()).difference_update(ACTION_CHANNELS[action])
            if self._current_action.get(event.actor_id) == action:
                self._current_action[event.actor_id] = None
        elif event.event_type == "AgentObserved":
            self._observations[payload["observer_id"]].add(payload["observed_event_id"])
            self._observations[payload["observer_id"]].add(event.event_id)
        if event.actor_id:
            self._observations[event.actor_id].add(event.event_id)

    def _state_payload(self) -> dict[str, Any]:
        payload = super()._state_payload()
        payload["needs"] = {key: dict(sorted(value.items())) for key, value in sorted(self._needs.items())}
        payload["inventories"] = {
            key: dict(sorted(value.items())) for key, value in sorted(self._inventories.items())
        }
        payload["owners"] = dict(sorted(self._owners.items()))
        payload["reservations"] = dict(sorted(self._reservations.items()))
        payload["channels"] = {key: sorted(value) for key, value in sorted(self._channels.items())}
        payload["current_action"] = dict(sorted((key, value) for key, value in self._current_action.items()))
        payload["households"] = dict(sorted(self._households.items()))
        payload["membership"] = dict(sorted(self._membership.items()))
        payload["observations"] = {
            key: sorted(value) for key, value in sorted(self._observations.items())
        }
        return payload

    def state_integrity_errors(self) -> list[str]:
        errors = super().state_integrity_errors()
        for holder_id, inventory in self._inventories.items():
            for resource_type, quantity in inventory.items():
                if quantity < 0:
                    errors.append(f"{holder_id} has negative {resource_type}")
        reserved_counts: dict[str, int] = defaultdict(int)
        for object_id in self._reservations.values():
            reserved_counts[object_id] += 1
        for spec in self.society["exclusive_objects"]:
            if reserved_counts.get(spec["object_id"], 0) > spec["capacity"]:
                errors.append(f"{spec['object_id']} reservation exceeds exclusive capacity")
        owners = list(self._owners.values())
        if len(self._owners) != len(set(self._owners)):
            errors.append("unique assets have duplicate identifiers")
        if len(owners) != len(self._owners):
            errors.append("unique asset ownership is inconsistent")
        return errors

    @classmethod
    def replay(cls, bundle: DistrictBundle, events: tuple[DomainEvent, ...]) -> NpcKernel:
        replayed = cls(bundle)
        replayed._calendar.clear()
        replayed._events.clear()
        replayed._inventories = {}
        replayed._owners = {}
        replayed._reservations = {}
        replayed._observations = defaultdict(set)
        replayed._channels = {agent.agent_id: set() for agent in replayed._initial_agents}
        replayed._current_action = {agent.agent_id: None for agent in replayed._initial_agents}
        replayed._bootstrapped = True
        for expected_sequence, event in enumerate(events, start=1):
            if event.sequence != expected_sequence:
                raise ValueError("event sequence is not contiguous")
            replayed.now = _parse_time(event.simulation_time)
            replayed._events.append(event)
            replayed._apply_event(event)
        return replayed

    def daily_place_counts(self) -> dict[str, int]:
        visited: dict[str, set[str]] = defaultdict(set)
        for agent in self._initial_agents:
            visited[agent.agent_id].add(agent.place_id)
        for event in self._events:
            if event.event_type == "LocationEntered" and event.actor_id:
                visited[event.actor_id].add(event.payload["place_id"])
        return {agent_id: len(places) for agent_id, places in visited.items()}
