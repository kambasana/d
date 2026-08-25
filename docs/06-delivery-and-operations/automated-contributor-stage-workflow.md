---
title: Automated Contributor Stage Workflow
document_id: AWG-OPS-012
status: draft
version: 0.2.0
last_updated: '2026-08-24'
normative: true
owners:
- AWG architecture
audience:
- engineering
- research
- product
depends_on:
- AWG-GOV-003
- AWG-OPS-001
- AWG-OPS-002
- AWG-OPS-006
- AWG-OPS-009
linear_issue: ELE-147
supersedes: []
---

# Automated Contributor Stage Workflow

## Purpose

Define the executable workflow by which automated contributors scope, trace, implement, validate, and close each roadmap stage without skipping authority, evidence, or approval boundaries.

## Status and authority

This document is normative and **draft**. The Simulation Constitution, accepted ADRs, and the authority order in `AGENTS.md` take precedence.

## Scope

- Role separation for coordination, scope, traceability, implementation, contracts, verification, and closeout.
- Ordered steps for MVP 0 through MVP 5.
- Machine-readable stage state, prerequisites, required outputs, validation commands, and closeout records.
- Fail-closed stage advancement.

## Non-goals

- This workflow does not grant an automated contributor authority to approve the Constitution, licences, security exceptions, destructive migrations, empirical validity, or production release.
- It does not permit later-MVP work to bypass an open prerequisite.
- It does not make generated reports or an issue tracker authoritative.

## Normative requirements

- Every stage MUST execute `scope`, `traceability`, `implementation`, `contracts`, `verification`, and `closeout` in that order.
- Every step MUST declare an automated-contributor role, required outputs, and at least one validation command.
- Only one stage MAY be active.
- A stage MUST NOT close while an earlier step is pending, a required output is absent, a registered acceptance test is unknown, or required validation fails.
- Closeout MUST include every phase-gate field from AWG-OPS-001 and MUST identify exact commands, evidence files, limitations, unresolved risks, and a bounded release decision.
- Closed-stage evidence MUST remain repository-readable and validation results MUST NOT be rewritten from failure to success.
- Completion of a workflow record MUST NOT be interpreted as human approval of a draft normative decision.

## Detailed specification

## Canonical workflow files

| Path | Authority |
| --- | --- |
| `workflow/stages.yaml` | Authored stage order, state, roles, outputs, and checks |
| `workflow/roles.yaml` | Authored role catalogue |
| `workflow/roles/*.md` | Role-specific operating instructions |
| `workflow/closeouts/mvp*.yaml` | Authored phase-gate records |
| `scripts/stage_workflow.py` | Deterministic workflow validator and coordinator |
| `generated/validation-report.md` | Generated pack validation evidence |

## Agent-role sequence

1. **Coordinator** reads the next task packet and dispatches one unblocked step.
2. **Scope** bounds the stage and records dependencies, risks, non-goals, and stop conditions.
3. **Traceability** creates requirement/test mappings before implementation.
4. **Implementation** builds the smallest constitutional vertical slice.
5. **Contracts** aligns schemas, fixtures, catalogues, and migrations.
6. **Verification** runs targeted, stage, full-pack, offline/security, replay, and performance checks.
7. **Closeout** completes the phase-gate record and asks the coordinator to enforce the gate.

One contributor MAY perform multiple roles sequentially, but MUST preserve the role boundaries and checks.

## Coordinator commands

```bash
make workflow-check
make workflow-status
make workflow-next
python3 scripts/stage_workflow.py check mvp3
python3 scripts/stage_workflow.py complete mvp3 scope
python3 scripts/stage_workflow.py gate mvp3
python3 scripts/stage_workflow.py loop --limit 64
```

`workflow-next` emits a machine-readable task packet containing the active stage, first pending step, role instructions, required outputs, validation commands, and closeout path.

`workflow-graph` emits the directed stage/step graph: sequential edges inside a stage and prerequisite edges from one closeout to the next scope. `workflow-run` prints status, the graph, and the next packet, then exits 2 while work remains.

`workflow-loop` drives the graph without further prompting. It repeatedly takes the next unblocked packet and completes it, which runs that step's declared validation commands, until one of the following happens:

- every stage is closed and the loop reports `plan_complete`;
- a step's outputs, evidence, or validation commands fail and the loop reports `blocked` with the failing stage, step, and reason;
- a step returns without advancing the graph, which the loop reports as blocked rather than spinning;
- the step limit is reached.

The loop MUST NOT skip a step, edit stage state directly, or continue past a failed gate. Because step validation runs `make test`, the loop refuses to start a nested run that would execute repository steps recursively.

```text
mvpN/scope -> traceability -> implementation -> contracts -> verification -> closeout
mvpN/closeout -.prerequisite.-> mvpN+1/scope
```

`complete` runs the step validation before changing stage state. Completing `closeout` additionally runs all gate evidence commands, closes the stage, and activates only the next stage whose prerequisites are closed.

## Validation and closeout

Verification MUST include:

- targeted requirement and invariant tests;
- contract/fixture validation;
- deterministic replay where state changes;
- offline, security, and failure behavior required by the stage;
- measured performance target;
- the stage runner;
- `make validate`;
- `make test`.

An open closeout record is a plan, not evidence. The closeout role changes it to `ready` only after its documentation flag, acceptance tests, evidence commands, and evidence files all describe completed work. Successful completion changes both the closeout and stage to `closed`.

## Human stop conditions

Automation MUST stop and request an explicit decision for:

- constitutional or accepted-ADR change;
- licence or redistribution approval;
- handling of sensitive real-person data;
- destructive or irreversible migration;
- security exception or secret exposure;
- empirical validation claim;
- production release decision not already delegated.

## Failure modes

- Marking steps complete without executing their declared validation.
- Running a later stage while a prerequisite remains open.
- Using a fluent model response as implementation evidence.
- Weakening tests or contracts to hide an invariant failure.
- Closing a gate with missing limitations, risks, or evidence.
- Treating Linear status as overriding repository validation.

## Security and privacy considerations

- Role instructions and model output are untrusted inputs to normal command and review boundaries.
- Automated contributors MUST NOT read or expose secrets beyond the task's declared capability.
- Remote providers introduced in MVP 3 MUST use the same fail-closed workflow and data-boundary review.
- Closeout records MUST avoid sensitive payloads and link to governed evidence instead.

## Performance and scale considerations

- Workflow validation SHOULD remain fast enough to run before every stage action.
- Expensive soak, security, or performance commands MAY run separately, but their exact successful command evidence remains mandatory for closeout.
- Parallel agents MAY explore independent areas, but canonical edits and stage state changes require deterministic reconciliation.

## Acceptance criteria

- Invalid stage order, unknown roles, missing closeout fields, missing completed outputs, unknown test IDs, and contradictory stage states fail validation.
- The loop advances every pending step of a ready stage and stops at the first failing gate without completing later steps.
- A nested loop started from inside a step validation is refused.
- `workflow-next` selects MVP 3 scope after MVP 0-2 are closed.
- MVP 3 cannot close while prior steps and evidence are incomplete.
- Full pack validation and pytest include the workflow checks.
- Advancing one stage activates only its immediate unblocked successor.

## Related documents

- AWG-GOV-003
- AWG-OPS-001
- AWG-OPS-002
- AWG-OPS-006
- AWG-OPS-009
