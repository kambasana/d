from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from stage_workflow import (  # noqa: E402
    LOOP_GUARD_ENV,
    REQUIRED_GATE_FIELDS,
    WorkflowError,
    check_stage,
    gate_stage,
    load_workflow,
    load_yaml,
    loop_workflow,
    next_packet,
    validate_workflow,
    workflow_graph,
)


class FakeGraph:
    """Minimal packet source so the loop can be driven without mutating the repository."""

    def __init__(self, steps: list[tuple[str, str]], failing: tuple[str, str] | None = None) -> None:
        self.pending = list(steps)
        self.failing = failing
        self.completed: list[tuple[str, str]] = []

    def packet(self) -> dict[str, str]:
        if not self.pending:
            return {"status": "plan_complete", "message": "All stages are closed."}
        stage, step = self.pending[0]
        return {"stage": stage, "step": step, "role": step}

    def complete(self, stage: str, step: str) -> None:
        if self.failing == (stage, step):
            raise WorkflowError(f"{stage}/{step} has no validation evidence")
        self.completed.append((stage, step))
        self.pending.pop(0)


def test_loop_drives_every_pending_step_until_the_plan_completes() -> None:
    graph = FakeGraph([("mvpX", "scope"), ("mvpX", "traceability"), ("mvpX", "closeout")])

    report = loop_workflow(packet_fn=graph.packet, complete_fn=graph.complete)

    assert report["status"] == "plan_complete"
    assert report["blocked"] is None
    assert [(item["stage"], item["step"]) for item in report["executed"]] == [
        ("mvpX", "scope"),
        ("mvpX", "traceability"),
        ("mvpX", "closeout"),
    ]
    assert graph.completed == [("mvpX", "scope"), ("mvpX", "traceability"), ("mvpX", "closeout")]


def test_loop_stops_at_the_first_step_that_fails_its_gate() -> None:
    graph = FakeGraph(
        [("mvpX", "scope"), ("mvpX", "verification"), ("mvpX", "closeout")],
        failing=("mvpX", "verification"),
    )

    report = loop_workflow(packet_fn=graph.packet, complete_fn=graph.complete)

    assert report["status"] == "blocked"
    assert report["blocked"]["step"] == "verification"
    assert "no validation evidence" in report["blocked"]["reason"]
    assert [(item["stage"], item["step"]) for item in report["executed"]] == [("mvpX", "scope")]
    assert ("mvpX", "closeout") not in graph.completed


def test_loop_refuses_to_spin_when_a_step_does_not_advance() -> None:
    report = loop_workflow(
        packet_fn=lambda: {"stage": "mvpX", "step": "scope", "role": "scope"},
        complete_fn=lambda stage, step: None,
    )

    assert report["status"] == "blocked"
    assert report["blocked"]["reason"] == "step repeated without advancing the graph"


def test_loop_reads_the_real_graph_without_executing_repository_steps() -> None:
    attempted: list[tuple[str, str]] = []

    def refuse(stage: str, step: str) -> None:
        attempted.append((stage, step))
        raise WorkflowError("the test suite does not execute repository steps")

    report = loop_workflow(complete_fn=refuse)
    workflow, _ = load_workflow()

    assert report["executed"] == []
    if all(stage["state"] == "closed" for stage in workflow["stages"]):
        assert report["status"] == "plan_complete"
        assert attempted == []
    else:
        assert report["status"] == "blocked"
        assert len(attempted) == 1


def test_loop_refuses_to_nest_inside_a_running_step_validation(monkeypatch) -> None:
    monkeypatch.setenv(LOOP_GUARD_ENV, "1")

    with pytest.raises(WorkflowError, match="nested workflow loop"):
        loop_workflow(packet_fn=lambda: {"status": "plan_complete"})

    graph = FakeGraph([("mvpX", "scope")])
    assert loop_workflow(packet_fn=graph.packet, complete_fn=graph.complete)["status"] == "plan_complete"


def test_workflow_configuration_and_closed_evidence_are_valid() -> None:
    assert validate_workflow() == []
    for stage_id in ("mvp0", "mvp1", "mvp2"):
        assert check_stage(stage_id) == []


def test_next_packet_dispatches_first_pending_step_of_active_stage() -> None:
    packet = next_packet()
    workflow, _ = load_workflow()
    active = next((stage for stage in workflow["stages"] if stage["state"] == "active"), None)
    if active is None:
        assert packet["status"] == "plan_complete"
        return
    pending = next(step for step in active["steps"] if step["status"] == "pending")
    assert packet["stage"] == active["id"]
    assert packet["step"] == pending["id"]
    assert packet["role"] == pending["role"]
    assert packet["required_outputs"] == pending["outputs"]
    assert packet["instructions"].startswith("# ")


def test_each_role_has_readable_instructions() -> None:
    _, roles_doc = load_workflow()
    for role in roles_doc["roles"]:
        instructions = ROOT / role["instructions"]
        assert instructions.is_file()
        assert instructions.read_text(encoding="utf-8").startswith("# ")


def test_every_stage_has_ordered_validated_steps_and_closeout_fields() -> None:
    workflow, _ = load_workflow()
    for stage in workflow["stages"]:
        assert [step["id"] for step in stage["steps"]] == workflow["step_order"]
        assert all(step["validations"] for step in stage["steps"])
        closeout = load_yaml(ROOT / stage["closeout"])
        assert REQUIRED_GATE_FIELDS <= set(closeout)


def test_workflow_graph_encodes_sequence_and_prerequisites() -> None:
    graph = workflow_graph()
    step_nodes = [node for node in graph["nodes"] if node["kind"] == "step"]
    assert [node["id"] for node in step_nodes] == [
        f"mvp{stage}/{step}"
        for stage in range(6)
        for step in ("scope", "traceability", "implementation", "contracts", "verification", "closeout")
    ]
    assert {"from": "mvp3/closeout", "to": "mvp4/scope", "kind": "prerequisite"} in graph["edges"]
    assert {"from": "mvp4/closeout", "to": "mvp5/scope", "kind": "prerequisite"} in graph["edges"]
    assert graph["stop_conditions"]
    if graph["plan_complete"]:
        assert graph["next"] is None
    else:
        assert graph["next"]["stage"] in {"mvp4", "mvp5"}


def test_active_stage_gate_matches_its_recorded_readiness() -> None:
    workflow, _ = load_workflow()
    active = next((stage for stage in workflow["stages"] if stage["state"] == "active"), None)
    if active is None:
        assert all(stage["state"] == "closed" for stage in workflow["stages"])
        return
    closeout = load_yaml(ROOT / active["closeout"])
    ready = (
        all(step["status"] == "completed" for step in active["steps"][:-1])
        and closeout["status"] == "ready"
    )
    if ready:
        gate_stage(active["id"], execute=False)
    else:
        with pytest.raises(WorkflowError):
            gate_stage(active["id"], execute=False)
