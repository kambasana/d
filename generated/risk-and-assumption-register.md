# Risk and Assumption Register

## Risks

| ID | Description | Severity | Mitigation | Documents | Status |
| --- | --- | --- | --- | --- | --- |
| AWG-RISK-001 | LLM output mutates authoritative state | critical | Prevent direct writes; typed command validation and capability isolation. | AWG-GOV-001, AWG-PLAT-007 | open |
| AWG-RISK-002 | Spatially impossible movement or teleportation | critical | Authoritative routes, journey states, elapsed time, and invariant tests. | AWG-DOM-002 | open |
| AWG-RISK-003 | Agents become omniscient through context assembly | high | Observation service, epistemic state, information paths, and access controls. | AWG-DOM-009, AWG-DOM-004 | open |
| AWG-RISK-004 | Per-agent per-tick model calls make scale and cost infeasible | high | Event-driven activation, classical policies, batching, LOD, budgets, and caching. | AWG-DOM-003, AWG-PLAT-005 | open |
| AWG-RISK-005 | Believable dialogue is mistaken for validated human behaviour | critical | Validation framework, responsible claims policy, human baselines, and uncertainty. | AWG-GOV-006, AWG-SCN-002 | open |
| AWG-RISK-006 | Synthetic population stereotypes cause biased outcomes | high | Provenance, calibration, constrained synthesis, sensitivity tests, and ethics review. | AWG-DOM-012, AWG-GOV-005 | open |
| AWG-RISK-007 | Information actions are incorrectly interpreted as belief | high | Separate exposure, reaction, motive inference, belief, and endorsement. | AWG-DOM-004, AWG-DOM-013 | open |
| AWG-RISK-008 | Plugin compromise or dependency supply-chain attack | critical | Permissions, isolation, SBOM, pinning, verification, and contract tests. | AWG-PLAT-003, AWG-OPS-011 | open |
| AWG-RISK-009 | External data or OSM gaps create false precision | high | Coverage metadata, uncertainty, fallback, visible limitations, and local validation. | AWG-DOM-002, AWG-SCN-009 | open |
| AWG-RISK-010 | Indoor geometry and entrances are absent or wrong | medium | Confidence levels, explicit unresolved access, local authoring, and validation. | AWG-DOM-002, AWG-UX-009 | open |
| AWG-RISK-011 | Event volume overwhelms storage and analysis | high | Partitioning, compression, retention classes, projections, and capacity tests. | AWG-PLAT-002, AWG-PLAT-004, AWG-OPS-003 | open |
| AWG-RISK-012 | Model or prompt drift invalidates comparisons | high | Immutable run records, version registry, recorded outputs, and sensitivity analysis. | AWG-SCN-006, AWG-SCN-003 | open |
| AWG-RISK-013 | Visual clusters imply false co-location or movement | medium | Distinct cluster types, precise labels, zoom-to-bounds, and anchored radial expansion. | AWG-UX-002 | open |
| AWG-RISK-014 | Counterfactual results are overclaimed as causal truth | critical | Baseline alignment, uncertainty, validation scope, and responsible-use wording. | AWG-SCN-004, AWG-GOV-006 | open |
| AWG-RISK-015 | Offline deployment still phones home through hidden dependencies | high | Network-deny tests, local assets, provider capability declarations, and telemetry controls. | AWG-PLAT-006, AWG-OPS-002 | open |
| AWG-RISK-016 | Replay diverges due to nondeterministic ordering or missing model records | high | Stable sequencing, random streams, snapshot validation, and recorded inference. | AWG-PLAT-002, AWG-DOM-008 | open |
| AWG-RISK-017 | Licensing obligations block commercial distribution | high | Provisional register, legal review, architecture-pattern-only alternatives, and SBOM. | AWG-OPS-011 | open |
| AWG-RISK-018 | Sensitive real-person or geospatial data is exposed | critical | Classification, least privilege, de-identification, retention, redaction, and audit. | AWG-GOV-002, AWG-GOV-004, AWG-GOV-005 | open |
| AWG-RISK-019 | A single graph database becomes a performance and coupling bottleneck | medium | Semantic graph model over fit-for-purpose stores and projections. | AWG-PLAT-004 | open |
| AWG-RISK-020 | Documentation, schemas, examples, and Linear drift apart | high | Manifest validation, generated indexes, traceability, staged contributor workflow, closeout evidence, CI gates, and canonical source rule. | AWG-OPS-009, AWG-OPS-010 | open |

## Assumptions

| ID | Statement | Documents | Status | Review trigger |
| --- | --- | --- | --- | --- |
| AWG-ASM-001 | A bounded region can be validated before planetary expansion. | AWG-OPS-001 | active | architecture review or contradictory evidence |
| AWG-ASM-002 | OpenStreetMap-derived data provides a useful base but requires local coverage assessment. | AWG-DOM-002 | active | architecture review or contradictory evidence |
| AWG-ASM-003 | Offline deployments can obtain local PBF extracts, tiles, gazetteer, routing data, and model artefacts lawfully. | AWG-PLAT-006 | active | architecture review or contradictory evidence |
| AWG-ASM-004 | Users will distinguish scenario exploration from prediction when the UI and reports communicate uncertainty correctly. | AWG-GOV-006 | active | architecture review or contradictory evidence |
| AWG-ASM-005 | Classical agent systems can handle most routine behaviour without model inference. | AWG-DOM-003 | active | architecture review or contradictory evidence |
| AWG-ASM-006 | World state can be partitioned while maintaining one mutation authority per entity or region. | AWG-PLAT-011 | active | architecture review or contradictory evidence |
| AWG-ASM-007 | Indoor detail will often be incomplete and must support explicit confidence and authoring. | AWG-DOM-002 | active | architecture review or contradictory evidence |
| AWG-ASM-008 | A provider-neutral structured-output boundary is feasible for Ollama, OpenRouter, and future providers. | AWG-PLAT-003 | active | architecture review or contradictory evidence |
| AWG-ASM-009 | Event sourcing plus snapshots is suitable for required replay and audit needs. | AWG-PLAT-002 | active | architecture review or contradictory evidence |
| AWG-ASM-010 | The repository will later be imported into a version-control system with protected review workflow. | AWG-OPS-006 | active | architecture review or contradictory evidence |
