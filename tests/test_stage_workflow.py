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
)


def test_workflow_configuration_and_closed_evidence_are_valid() -> None:
    assert validate_workflow() == []
    for stage_id in ("mvp0", "mvp1", "mvp2"):
        assert check_stage(stage_id) == []


def test_next_packet_dispatches_first_pending_step_of_active_stage() -> None:
    packet = next_packet()
    assert packet["stage"] == "mvp3"
    assert packet["step"] == "scope"
    assert packet["role"] == "scope"
    assert packet["required_outputs"] == ["workflow/closeouts/mvp3.yaml"]
    assert "Do not implement code" in packet["instructions"]


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


def test_open_stage_cannot_close_without_completed_steps_and_evidence() -> None:
    with pytest.raises(WorkflowError, match="scope through verification"):
        gate_stage("mvp3", execute=False)
