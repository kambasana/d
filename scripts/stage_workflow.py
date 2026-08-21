from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
STAGES_PATH = ROOT / "workflow" / "stages.yaml"
ROLES_PATH = ROOT / "workflow" / "roles.yaml"
REQUIRED_GATE_FIELDS = {
    "stage",
    "status",
    "issue",
    "objectives",
    "in_scope",
    "non_goals",
    "dependencies",
    "acceptance_tests",
    "performance_target",
    "security_offline_target",
    "validation_evidence",
    "documentation_complete",
    "known_limitations",
    "unresolved_risks",
    "release_decision",
    "evidence_files",
}
STAGE_STATES = {"blocked", "active", "closed"}
STEP_STATES = {"pending", "completed"}


class WorkflowError(RuntimeError):
    pass


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise WorkflowError(f"{path.relative_to(ROOT)} must contain a mapping")
    return data


def load_workflow() -> tuple[dict[str, Any], dict[str, Any]]:
    return load_yaml(STAGES_PATH), load_yaml(ROLES_PATH)


def stage_map(workflow: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {stage["id"]: stage for stage in workflow["stages"]}


def validate_workflow() -> list[str]:
    errors: list[str] = []
    workflow, roles_doc = load_workflow()
    roles = {role["id"]: role for role in roles_doc.get("roles", [])}
    stages = workflow.get("stages", [])
    stages_by_id = stage_map(workflow)
    expected_ids = [f"mvp{number}" for number in range(6)]
    actual_ids = [stage.get("id") for stage in stages]
    if actual_ids != expected_ids:
        errors.append(f"stages must be ordered exactly as {expected_ids}")
    if len(roles) != len(roles_doc.get("roles", [])):
        errors.append("workflow role IDs must be unique")
    active = [stage["id"] for stage in stages if stage.get("state") == "active"]
    if len(active) > 1:
        errors.append(f"only one stage may be active, found {active}")

    test_ids = {
        item["id"] for item in load_yaml(ROOT / "registers" / "tests.yaml").get("tests", [])
    }
    roadmap_path = ROOT / workflow.get("roadmap", "")
    roadmap = roadmap_path.read_text(encoding="utf-8") if roadmap_path.is_file() else ""
    if not roadmap:
        errors.append("workflow roadmap is missing")

    for index, stage in enumerate(stages):
        stage_id = stage.get("id", f"stage-{index}")
        if stage.get("state") not in STAGE_STATES:
            errors.append(f"{stage_id} has invalid state {stage.get('state')}")
        if stage.get("title") not in roadmap:
            errors.append(f"{stage_id} title is not present in the roadmap")
        for prerequisite in stage.get("prerequisites", []):
            if prerequisite not in stages_by_id:
                errors.append(f"{stage_id} has unknown prerequisite {prerequisite}")
            elif expected_ids.index(prerequisite) >= index:
                errors.append(f"{stage_id} prerequisite {prerequisite} is not earlier")
        steps = stage.get("steps", [])
        if [step.get("id") for step in steps] != workflow.get("step_order"):
            errors.append(f"{stage_id} steps do not match required order")
        for step in steps:
            if step.get("role") not in roles:
                errors.append(f"{stage_id}/{step.get('id')} has unknown role {step.get('role')}")
            if step.get("status") not in STEP_STATES:
                errors.append(
                    f"{stage_id}/{step.get('id')} has invalid status {step.get('status')}"
                )
            if not isinstance(step.get("outputs"), list) or not step["outputs"]:
                errors.append(f"{stage_id}/{step.get('id')} must declare outputs")
            if not isinstance(step.get("validations"), list) or not step["validations"]:
                errors.append(f"{stage_id}/{step.get('id')} must declare validations")

        closeout_path = ROOT / stage.get("closeout", "")
        if not closeout_path.is_file():
            errors.append(f"{stage_id} closeout record is missing")
            continue
        closeout = load_yaml(closeout_path)
        missing = REQUIRED_GATE_FIELDS - set(closeout)
        if missing:
            errors.append(f"{stage_id} closeout lacks fields {sorted(missing)}")
        if closeout.get("stage") != stage_id:
            errors.append(f"{stage_id} closeout stage does not match")
        if stage.get("state") == "closed":
            if any(step.get("status") != "completed" for step in steps):
                errors.append(f"{stage_id} is closed with incomplete steps")
            if closeout.get("status") != "closed":
                errors.append(f"{stage_id} is closed but its closeout is not")
            if closeout.get("documentation_complete") is not True:
                errors.append(f"{stage_id} closed without documentation completion")
            if not closeout.get("validation_evidence"):
                errors.append(f"{stage_id} closed without validation evidence")
            for evidence in closeout.get("validation_evidence", []):
                if evidence.get("result") != "passed" or not evidence.get("command"):
                    errors.append(f"{stage_id} has invalid validation evidence {evidence}")
            for test_id in closeout.get("acceptance_tests", []):
                if test_id not in test_ids:
                    errors.append(f"{stage_id} closeout references unknown test {test_id}")
            for evidence_file in closeout.get("evidence_files", []):
                if not (ROOT / evidence_file).exists():
                    errors.append(f"{stage_id} evidence file is missing: {evidence_file}")
        elif closeout.get("status") == "closed":
            errors.append(f"{stage_id} has a closed closeout but stage state is {stage.get('state')}")

    for stage in stages:
        if stage.get("state") == "blocked" and all(
            stages_by_id[item].get("state") == "closed"
            for item in stage.get("prerequisites", [])
        ):
            errors.append(f"{stage['id']} is blocked even though all prerequisites are closed")
        if stage.get("state") == "active" and not all(
            stages_by_id[item].get("state") == "closed"
            for item in stage.get("prerequisites", [])
        ):
            errors.append(f"{stage['id']} is active with an open prerequisite")
    return errors


def require_valid() -> None:
    errors = validate_workflow()
    if errors:
        raise WorkflowError("\n".join(errors))


def check_stage(stage_id: str) -> list[str]:
    errors = validate_workflow()
    workflow, _ = load_workflow()
    stage = stage_map(workflow).get(stage_id)
    if stage is None:
        return errors + [f"unknown stage {stage_id}"]
    for step in stage["steps"]:
        if step["status"] != "completed":
            continue
        for output in step["outputs"]:
            if not (ROOT / output).exists():
                errors.append(f"{stage_id}/{step['id']} output is missing: {output}")
    return errors


def next_packet() -> dict[str, Any]:
    require_valid()
    workflow, roles_doc = load_workflow()
    roles = {role["id"]: role for role in roles_doc["roles"]}
    stages = stage_map(workflow)
    for stage in workflow["stages"]:
        if stage["state"] != "active":
            continue
        if not all(stages[item]["state"] == "closed" for item in stage["prerequisites"]):
            raise WorkflowError(f"{stage['id']} has an open prerequisite")
        for step in stage["steps"]:
            if step["status"] == "pending":
                role = roles[step["role"]]
                instructions_path = ROOT / role["instructions"]
                return {
                    "stage": stage["id"],
                    "stage_title": stage["title"],
                    "step": step["id"],
                    "role": role["id"],
                    "purpose": role["purpose"],
                    "instructions": instructions_path.read_text(encoding="utf-8"),
                    "required_outputs": step["outputs"],
                    "validation_commands": step["validations"],
                    "closeout_record": stage["closeout"],
                }
    return {"status": "plan_complete", "message": "All stages are closed."}


def run_commands(commands: list[str]) -> None:
    for command in commands:
        print(f"+ {command}", flush=True)
        completed = subprocess.run(shlex.split(command), cwd=ROOT, check=False)
        if completed.returncode:
            raise WorkflowError(f"validation failed ({completed.returncode}): {command}")


def gate_stage(stage_id: str, execute: bool = True) -> None:
    require_valid()
    workflow, _ = load_workflow()
    stage = stage_map(workflow).get(stage_id)
    if stage is None:
        raise WorkflowError(f"unknown stage {stage_id}")
    if any(step["status"] != "completed" for step in stage["steps"][:-1]):
        raise WorkflowError(f"{stage_id} cannot close before scope through verification complete")
    closeout = load_yaml(ROOT / stage["closeout"])
    if closeout.get("status") != "ready":
        raise WorkflowError(f"{stage_id} closeout status must be ready before gate validation")
    if closeout.get("documentation_complete") is not True:
        raise WorkflowError(f"{stage_id} documentation_complete must be true")
    if not closeout.get("acceptance_tests"):
        raise WorkflowError(f"{stage_id} has no acceptance tests")
    if not closeout.get("validation_evidence"):
        raise WorkflowError(f"{stage_id} has no validation evidence")
    for evidence_file in closeout.get("evidence_files", []):
        if not (ROOT / evidence_file).exists():
            raise WorkflowError(f"{stage_id} evidence file is missing: {evidence_file}")
    if execute:
        run_commands([item["command"] for item in closeout["validation_evidence"]])


def save_workflow(workflow: dict[str, Any]) -> None:
    STAGES_PATH.write_text(
        yaml.safe_dump(workflow, sort_keys=False, width=140, allow_unicode=True),
        encoding="utf-8",
    )


def complete_step(stage_id: str, step_id: str) -> None:
    require_valid()
    workflow, _ = load_workflow()
    stages = stage_map(workflow)
    stage = stages.get(stage_id)
    if stage is None or stage["state"] != "active":
        raise WorkflowError(f"{stage_id} is not the active stage")
    step_ids = [item["id"] for item in stage["steps"]]
    if step_id not in step_ids:
        raise WorkflowError(f"unknown step {stage_id}/{step_id}")
    index = step_ids.index(step_id)
    if any(item["status"] != "completed" for item in stage["steps"][:index]):
        raise WorkflowError(f"{stage_id}/{step_id} is blocked by an earlier step")
    step = stage["steps"][index]
    if step["status"] == "completed":
        print(f"{stage_id}/{step_id} is already complete.")
        return
    for output in step["outputs"]:
        if not (ROOT / output).exists():
            raise WorkflowError(f"required output is missing: {output}")
    if step_id == "closeout":
        gate_stage(stage_id)
    else:
        run_commands(step["validations"])
    step["status"] = "completed"
    if step_id == "closeout":
        closeout_path = ROOT / stage["closeout"]
        closeout = load_yaml(closeout_path)
        closeout["status"] = "closed"
        closeout_path.write_text(
            yaml.safe_dump(closeout, sort_keys=False, width=120),
            encoding="utf-8",
        )
        stage["state"] = "closed"
        stage_index = workflow["stages"].index(stage)
        if stage_index + 1 < len(workflow["stages"]):
            next_stage = workflow["stages"][stage_index + 1]
            if all(stages[item]["state"] == "closed" for item in next_stage["prerequisites"]):
                next_stage["state"] = "active"
                closeout = load_yaml(ROOT / next_stage["closeout"])
                if closeout.get("status") == "blocked":
                    closeout["status"] = "open"
                    (ROOT / next_stage["closeout"]).write_text(
                        yaml.safe_dump(closeout, sort_keys=False, width=120),
                        encoding="utf-8",
                    )
    save_workflow(workflow)
    print(f"Completed {stage_id}/{step_id}.")


def print_status() -> None:
    require_valid()
    workflow, _ = load_workflow()
    for stage in workflow["stages"]:
        completed = sum(step["status"] == "completed" for step in stage["steps"])
        print(f"{stage['id']}: {stage['state']} ({completed}/{len(stage['steps'])} steps)")


def main() -> None:
    parser = argparse.ArgumentParser(description="AWG staged automated-contributor workflow")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("validate")
    subparsers.add_parser("status")
    subparsers.add_parser("next")
    check = subparsers.add_parser("check")
    check.add_argument("stage")
    gate = subparsers.add_parser("gate")
    gate.add_argument("stage")
    complete = subparsers.add_parser("complete")
    complete.add_argument("stage")
    complete.add_argument("step")
    args = parser.parse_args()

    try:
        if args.command == "validate":
            require_valid()
            print("Workflow configuration and closed-stage evidence are valid.")
        elif args.command == "status":
            print_status()
        elif args.command == "next":
            print(json.dumps(next_packet(), indent=2))
        elif args.command == "check":
            errors = check_stage(args.stage)
            if errors:
                raise WorkflowError("\n".join(errors))
            print(f"{args.stage} structure and completed outputs are valid.")
        elif args.command == "gate":
            gate_stage(args.stage)
            print(f"{args.stage} gate validation passed.")
        elif args.command == "complete":
            complete_step(args.stage, args.step)
    except WorkflowError as exc:
        print(f"WORKFLOW ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
