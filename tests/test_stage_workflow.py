from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from stage_workflow import (  # noqa: E402
    REQUIRED_GATE_FIELDS,
    WorkflowError,
    check_stage,
    gate_stage,
    load_workflow,
    load_yaml,
    next_packet,
    validate_workflow,
    workflow_graph,
)


def test_workflow_configuration_and_closed_evidence_are_valid() -> None:
    assert validate_workflow() == []
    for stage_id in ("mvp0", "mvp1", "mvp2"):
        assert check_stage(stage_id) == []


def test_next_packet_dispatches_first_pending_step_of_active_stage() -> None:
    packet = next_packet()
    workflow, _ = load_workflow()
    active = next(stage for stage in workflow["stages"] if stage["state"] == "active")
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
    active = next(stage for stage in workflow["stages"] if stage["state"] == "active")
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
