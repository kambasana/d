# Instructions for AI Agents and Automated Contributors

## Mandatory reading order

Before changing any file, read:

1. `README.md`
2. this file
3. `docs/01-governance-and-safety/simulation-constitution-and-invariants.md`
4. `generated/glossary-and-controlled-vocabulary.md`
5. `generated/document-map.md`
6. the target normative specification
7. related requirements, schemas, tests, risks, evidence, and ADRs

## Authority order

1. Simulation Constitution
2. Accepted ADRs
3. Accepted normative specifications
4. Versioned machine-readable contracts
5. Draft normative specifications
6. Informative research and examples
7. Generated indexes and projections
8. Archived conversation-derived material

## Non-negotiable behaviour

- Never allow an LLM, UI, projection, or plugin to mutate authoritative world state directly.
- Never invent physical movement, arrival, ownership, access, knowledge, or causal success.
- Never give an agent global simulator knowledge; observations require a physical or informational path.
- Never treat a like, repost, comment, view, or follow as proof of belief or endorsement.
- Never use PMTiles or display clusters as authoritative geography.
- Never merge world truth, agent belief, UI projection, and software telemetry into one semantic plane.
- Never replace seeded, typed randomness with unexplained activity intended only to make the world look alive.
- Never silently alter model, prompt, plugin, dataset, scenario, or schema versions during a run.
- Never present fluent dialogue or a visually convincing map as scientific validation.
- Never edit generated files directly.

## Change procedure

1. Identify the Linear issue or create a local work record.
2. Identify affected document IDs, requirement IDs, test IDs, schemas, risks, assumptions, data sources, and ADRs.
3. Change canonical authored files or YAML registers.
4. Update executable contracts and examples when semantics change.
5. Run `python scripts/validate_all.py` and `pytest -q`.
6. Rebuild generated reports and release artefacts.
7. Record breaking changes and migrations.

## Roadmap stage workflow

For MVP roadmap work:

1. Run `make workflow-check`.
2. Run `make workflow-loop` to drive every unblocked step to closure, or `make workflow-next` to perform only the next returned role/step.
3. Produce every declared output.
4. Complete the step with `python3 scripts/stage_workflow.py complete <stage> <step>`; this runs its validation before updating workflow state.
5. Repeat through `scope`, `traceability`, `implementation`, `contracts`, `verification`, and `closeout` until `plan_complete` or a human stop condition.
6. The closeout role must set the gate record to `ready`; completing closeout reruns gate evidence, closes the stage, and activates the next prerequisite-safe stage.

Never edit a stage to `closed` merely to bypass the coordinator. Follow AWG-OPS-012 and stop at its human decision boundaries.

## Terminology

Use canonical terms from `registers/glossary.yaml`. Do not treat `agent`, `LLM`, `user`, `actor`, `cohort`, `entity`, and `account` as interchangeable. Do not introduce a new core noun without a glossary entry and ontology review.

## Normative language

Use MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY for requirements. Every new normative rule requires a stable requirement ID and an acceptance-test mapping.

## File placement

- Narrative specifications: `docs/`
- JSON Schemas: `contracts/`
- Canonical structured records: `registers/`
- Generated Markdown/JSON: `generated/`
- Valid and invalid fixtures: `examples/fixtures/`
- Architecture decisions: `decisions/`
- Validation code: `scripts/` and `tests/`
- Historical source material: `archive/`

## Completion rule

Do not claim that the pack or a document is complete merely because files exist. Completion requires the manifest, required sections, traceability, schemas, examples, tests, links, provenance, licensing records, checksums, and validation report to agree.
