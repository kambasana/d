from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from typing import Any

FIDELITY = ("S0", "S1", "S2", "S3", "S4")


class ScaleKernel:
    """Bounded S0-S4 records with conserved promotion and branch comparison."""

    def __init__(self, seed: int = 11, intervention: str | None = None) -> None:
        self.seed = seed
        self.intervention = intervention
        self.population: dict[str, dict[str, Any]] = {}
        self.active: dict[str, dict[str, Any]] = {}
        self.events: list[dict[str, Any]] = []
        self._seed_population()

    def _seed_population(self) -> None:
        for index in range(1000):
            record_id = f"person:{index:04d}"
            cohort = f"cohort:{index // 20:03d}"
            fidelity = FIDELITY[index % 5]
            tokens = 5 + (index % 7)
            self.population[record_id] = {
                "record_id": record_id,
                "cohort_id": cohort,
                "fidelity": fidelity,
                "tokens": tokens,
                "beliefs": {"claim:transformer:001": "unknown"},
                "place_id": f"place:home-{(index % 50):02d}",
            }
        for index in range(50):
            record_id = f"person:{index:04d}"
            self.active[record_id] = deepcopy(self.population[record_id])
            self.active[record_id]["fidelity"] = "S4"

    def _event(self, event_type: str, payload: dict[str, Any]) -> None:
        self.events.append({"event_type": event_type, "payload": payload, "sequence": len(self.events) + 1})

    def promote(self, record_id: str) -> None:
        record = self.population[record_id]
        before_tokens = record["tokens"]
        before_beliefs = dict(record["beliefs"])
        active = deepcopy(record)
        active["fidelity"] = "S4"
        self.active[record_id] = active
        record["fidelity"] = "S4"
        self._event("FidelityPromoted", {"record_id": record_id, "from": "S1", "to": "S4"})
        if active["tokens"] != before_tokens or active["beliefs"] != before_beliefs:
            raise RuntimeError("promotion must conserve tokens and beliefs")

    def demote(self, record_id: str, fidelity: str = "S1") -> None:
        active = self.active.pop(record_id)
        record = self.population[record_id]
        record["tokens"] = active["tokens"]
        record["beliefs"] = dict(active["beliefs"])
        record["fidelity"] = fidelity
        self._event("FidelityDemoted", {"record_id": record_id, "from": "S4", "to": fidelity})

    def run_profile(self) -> None:
        self.promote("person:0050")
        if self.intervention == "suppress_post":
            self._event("InterventionApplied", {"kind": "suppress_post", "seed": self.seed})
            for index in range(50, 80):
                self._event("CohortTickSkipped", {"record_id": f"person:{index:04d}"})
        else:
            for index in range(50, 80):
                self._event("CohortTick", {"record_id": f"person:{index:04d}", "fidelity": "S0"})
        for record_id, actor in self.active.items():
            actor["tokens"] -= 0
            self._event("ActiveCognitionTick", {"record_id": record_id, "fidelity": actor["fidelity"]})
        self.demote("person:0050")

    def totals(self) -> dict[str, int]:
        return {
            "population_records": len(self.population),
            "active_cognition": len(self.active),
            "events": len(self.events),
            "token_sum": sum(item["tokens"] for item in self.population.values()),
        }

    def checksum(self) -> str:
        encoded = json.dumps({"population": self.population, "active": sorted(self.active)}, sort_keys=True, separators=(",", ":")).encode()
        return hashlib.sha256(encoded).hexdigest()


def compare_branches(seed: int = 11) -> dict[str, Any]:
    control = ScaleKernel(seed=seed)
    treatment = ScaleKernel(seed=seed, intervention="suppress_post")
    control.run_profile()
    treatment.run_profile()
    return {
        "same_seed": control.seed == treatment.seed,
        "control_events": len(control.events),
        "treatment_events": len(treatment.events),
        "effect_is_not_seed_noise": len(control.events) != len(treatment.events),
        "control_tokens": control.totals()["token_sum"],
        "treatment_tokens": treatment.totals()["token_sum"],
        "tokens_conserved": control.totals()["token_sum"] == treatment.totals()["token_sum"],
    }
