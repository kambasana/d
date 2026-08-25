from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from awg_mvp1 import SimulationKernel, load_reference_bundle
from awg_mvp1.kernel import _format_time, _parse_time
from awg_mvp4 import InformationKernel
from awg_mvp5.scale import ScaleKernel, compare_branches

UTC = timezone.utc
PRESERVED_INVARIANTS = ("INV-001", "INV-006", "INV-007", "INV-011", "INV-016")


@dataclass(frozen=True, slots=True)
class ReviewBundle:
    """Immutable review bundle derived from MVP 1, MVP 4, and MVP 5 kernels."""

    schema_version: str
    bundle_id: str
    spatial: dict[str, Any]
    information: dict[str, Any]
    scale: dict[str, Any]
    invariants_preserved: tuple[str, ...]
    external_network_dependencies: tuple[str, ...]
    _mvp1_events: tuple[Any, ...]
    _mvp4_events: tuple[dict[str, Any], ...]
    _mvp4_kernel: InformationKernel
    _mvp5_kernel: ScaleKernel
    _mvp5_branch_comparison: dict[str, Any]

    @property
    def start_time(self) -> str:
        return self.spatial["start_time"]

    @property
    def end_time(self) -> str:
        return self.spatial["end_time"]

    def spatial_kernel_at(self, simulation_time: str) -> SimulationKernel:
        bundle = load_reference_bundle()
        target = _parse_time(simulation_time)
        start = _parse_time(self.start_time)
        end = _parse_time(self.end_time)
        if target < start or target > end:
            raise ValueError("simulation_time is outside the review bundle window")
        events = tuple(
            event
            for event in self._mvp1_events
            if _parse_time(event.simulation_time) <= target
        )
        kernel = SimulationKernel.replay(bundle, events)
        kernel.run_until(target)
        return kernel

    def firehose_page(
        self,
        *,
        from_sequence: int = 1,
        limit: int = 50,
        world_id: str | None = None,
    ) -> dict[str, Any]:
        limit = max(1, min(limit, 200))
        spatial_events = [
            {
                "source": "mvp1-spatial",
                "sequence": event.sequence,
                "event_id": event.event_id,
                "event_type": event.event_type,
                "world_id": event.world_id,
                "simulation_time": event.simulation_time,
                "actor_id": event.actor_id,
                "payload": event.payload,
            }
            for event in self._mvp1_events
            if event.sequence >= from_sequence
        ]
        information_events = [
            {
                "source": "mvp4-information",
                "sequence": event["sequence"],
                "event_id": event["event_id"],
                "event_type": event["event_type"],
                "world_id": event["world_id"],
                "simulation_time": event["simulation_time"],
                "actor_id": event.get("actor_id"),
                "payload": event["payload"],
            }
            for event in self._mvp4_events
            if event["sequence"] >= from_sequence
        ]
        scale_events = [
            {
                "source": "mvp5-scale",
                "sequence": event["sequence"],
                "event_id": f"event:mvp5-{event['sequence']:08d}",
                "event_type": event["event_type"],
                "world_id": "world:mvp5-scale",
                "simulation_time": self.end_time,
                "actor_id": None,
                "payload": event["payload"],
            }
            for event in self._mvp5_kernel.events
            if event["sequence"] >= from_sequence
        ]
        combined = sorted(
            spatial_events + information_events + scale_events,
            key=lambda item: (item["simulation_time"], item["sequence"]),
        )
        if world_id:
            combined = [item for item in combined if item["world_id"] == world_id]
        page = combined[:limit]
        next_sequence = page[-1]["sequence"] + 1 if page else from_sequence
        return {
            "schema_version": self.schema_version,
            "from_sequence": from_sequence,
            "limit": limit,
            "returned": len(page),
            "next_sequence": next_sequence if len(page) == limit else None,
            "events": page,
        }

    def timeline_summary(self) -> dict[str, Any]:
        markers = [
            {
                "label": "spatial_start",
                "simulation_time": self.start_time,
                "world_id": self.spatial["world_id"],
            },
            {
                "label": "spatial_end",
                "simulation_time": self.end_time,
                "world_id": self.spatial["world_id"],
            },
            {
                "label": "information_reference",
                "simulation_time": self.information["reference_time"],
                "world_id": self.information["world_id"],
            },
        ]
        return {
            "schema_version": self.schema_version,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "markers": markers,
            "event_totals": {
                "spatial": len(self._mvp1_events),
                "information": len(self._mvp4_events),
                "scale": len(self._mvp5_kernel.events),
            },
        }

    def information_summary(self, *, agent_id: str | None = None, mode: str = "participant") -> dict[str, Any]:
        kernel = self._mvp4_kernel
        if mode == "analyst":
            projection = kernel.analyst_projection()
            return {
                "schema_version": self.schema_version,
                "mode": "analyst",
                "projection": projection,
                "claims": len(kernel.claims),
                "posts": len(kernel.posts),
                "actors": len(kernel.actors),
                "belief_separate_from_world_truth": True,
            }
        selected = agent_id or kernel.outsider
        projection = kernel.participant_projection(selected)
        return {
            "schema_version": self.schema_version,
            "mode": "participant",
            "agent_id": selected,
            "projection": projection,
            "likes_are_not_belief": True,
            "world_truth_exposed": projection["world_truth"] is not None,
        }

    def scale_summary(self) -> dict[str, Any]:
        totals = self._mvp5_kernel.totals()
        fidelity_counts: dict[str, int] = {}
        for record in self._mvp5_kernel.population.values():
            fidelity_counts[record["fidelity"]] = fidelity_counts.get(record["fidelity"], 0) + 1
        return {
            "schema_version": self.schema_version,
            "totals": totals,
            "fidelity_counts": fidelity_counts,
            "branch_comparison": self._mvp5_branch_comparison,
            "population_separate_from_active_cognition": totals["population_records"] != totals["active_cognition"],
        }

    def context(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "bundle_id": self.bundle_id,
            "read_only": True,
            "mutation_allowed": False,
            "invariants_preserved": list(self.invariants_preserved),
            "external_network_dependencies": list(self.external_network_dependencies),
            "worlds": {
                "spatial": self.spatial,
                "information": self.information,
                "scale": self.scale,
            },
            "static_assets_root": "apps/world-explorer/dist",
            "pmtiles_authority": "presentation_only",
        }

    def status(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "bundle_id": self.bundle_id,
            "healthy": True,
            "read_only": True,
            "spatial_state_checksum": self.spatial["state_checksum"],
            "information_state_checksum": self.information["state_checksum"],
            "scale_state_checksum": self.scale["state_checksum"],
            "event_counts": {
                "spatial": len(self._mvp1_events),
                "information": len(self._mvp4_events),
                "scale": len(self._mvp5_kernel.events),
            },
        }


def load_review_bundle() -> ReviewBundle:
    """Build an offline review bundle from the MVP reference kernels."""
    district_bundle = load_reference_bundle()
    spatial_kernel = SimulationKernel(district_bundle)
    spatial_kernel.run_24_hours()
    spatial_snapshot = spatial_kernel.snapshot()

    information_kernel = InformationKernel()
    information_kernel.run_reference()
    information_replay = InformationKernel.replay(information_kernel.events)

    scale_kernel = ScaleKernel(seed=11)
    scale_kernel.run_profile()
    branch_comparison = compare_branches(seed=11)

    return ReviewBundle(
        schema_version="0.2.0",
        bundle_id="bundle:world-explorer-review",
        spatial={
            "world_id": spatial_kernel.world_id,
            "scenario_id": spatial_kernel.scenario_id,
            "branch_id": spatial_kernel.branch_id,
            "district_id": district_bundle.manifest["district_id"],
            "population": district_bundle.population,
            "start_time": district_bundle.manifest["start_time"],
            "end_time": _format_time(spatial_kernel.now),
            "state_checksum": spatial_snapshot.state_checksum,
            "pmtiles_file": district_bundle.manifest["pmtiles_file"],
            "pmtiles_authority": "presentation_only",
            "buildings": sorted(district_bundle.buildings.keys()),
        },
        information={
            "world_id": information_kernel.world_id,
            "scenario_id": information_kernel.scenario_id,
            "branch_id": information_kernel.branch_id,
            "reference_time": information_kernel._format_time(),
            "state_checksum": information_kernel.state_checksum(),
            "actors": len(information_kernel.actors),
            "events": len(information_kernel.events),
            "replay_matches": information_replay.state_checksum() == information_kernel.state_checksum(),
        },
        scale={
            "world_id": "world:mvp5-scale",
            "scenario_id": "scenario:mvp5-reference",
            "branch_id": "branch:main",
            "state_checksum": scale_kernel.checksum(),
            "population_records": scale_kernel.totals()["population_records"],
            "active_cognition": scale_kernel.totals()["active_cognition"],
        },
        invariants_preserved=PRESERVED_INVARIANTS,
        external_network_dependencies=(),
        _mvp1_events=spatial_kernel.firehose,
        _mvp4_events=tuple(information_kernel.events),
        _mvp4_kernel=information_kernel,
        _mvp5_kernel=scale_kernel,
        _mvp5_branch_comparison=branch_comparison,
    )
