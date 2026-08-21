---
title: MVP Roadmap and Definition of Done
document_id: AWG-OPS-001
status: draft
version: 0.2.0
last_updated: '2026-08-21'
normative: true
owners:
- AWG architecture
audience:
- engineering
- research
- product
depends_on:
- AWG-GOV-001
- AWG-PLAT-001
- AWG-SCN-002
linear_issue: ELE-147
supersedes: []
---

# MVP Roadmap and Definition of Done

## Purpose

Define a phased path from one offline district and deterministic movement through bounded AI, information space, validation, and multi-resolution scale.

## Status and authority

This document is normative. Its current status is **draft**. Where this document conflicts with the Simulation Constitution, the Constitution takes precedence.

## Scope

- Define a phased path from one offline district and deterministic movement through bounded AI, information space, validation, and multi-resolution scale.

## Non-goals

- This document does not authorize bypassing the simulation kernel, provenance model, security boundary, or event history.
- It does not claim that a plausible simulation output is an empirically validated forecast.
- It does not make a specific vendor, model, database, or rendering engine part of the core domain contract unless explicitly stated.

## Normative requirements

- The implementation must conform to the rules defined in this specification for mvp roadmap and definition of done.
- All state-changing operations must use typed commands, validation, and append-only domain events where applicable.
- Any uncertainty, approximation, generated data, or external dependency must be explicitly identified and traceable.
- Implementations must preserve offline operation and provider replaceability unless a capability is explicitly declared optional.

## Detailed specification

## Delivery rule

Do not start at planet scale. Prove invariants, replay, offline operation, and spatial causality in a bounded district/city slice before scaling.

## MVP 0 - Constitution and executable contracts

### Scope
- accepted simulation constitution;
- canonical terminology/domain entities;
- command/event envelope drafts;
- scenario package draft;
- plugin interface draft;
- traceability matrix;
- CI test skeleton.

### Done when
- no core domain component requires an LLM to execute basic world state transitions;
- every planned subsystem maps to owned contracts;
- invariants have acceptance-test IDs.

### MVP 0 phase gate (ELE-147)

Local work record for Linear issue [ELE-147](https://linear.app/elenta/issue/ELE-147/awg-review-mvp-roadmap-testing-and-performance-gates). This gate closes only the documentation-and-contract slice of MVP 0. It MUST NOT be read as MVP 1 completion or as human acceptance of the Constitution.

| Gate field | MVP 0 record |
| --- | --- |
| Objectives | Make the constitution, glossary, command/event envelopes, scenario package, plugin interface, traceability matrix, and CI skeleton executable and reviewable. |
| In-scope | Authored specs, YAML registers, JSON Schemas, fixtures, pack validators, pytest, GitHub documentation-quality workflow. |
| Non-goals | OSM/PostGIS/routing/PMTiles runtime, live agents, LLM adapters, planetary scale, claiming the Constitution is accepted. |
| Dependencies | AWG-GOV-001, AWG-DOM-001, AWG-PLAT-001, AWG-PLAT-002, AWG-PLAT-003, AWG-SCN-001, AWG-OPS-002, AWG-OPS-006, AWG-OPS-009, AWG-APP-003. |
| Acceptance tests | AWG-TEST-INV-001 through AWG-TEST-INV-020; AWG-TEST-COV-044; pack `validate_all` and pytest. |
| Performance target | Pack validation and pytest complete on a clean Python 3.12 environment without GPU or model calls. |
| Security/offline target | Validation MUST run offline. Pack Python MUST NOT import an AI provider to validate commands, events, or fixtures. |
| Validation evidence | `generated/validation-report.md` after `python scripts/validate_all.py`; pytest results; INV requirement/test IDs in registers. |
| Documentation complete | Constitution remains **draft**. INV rules MUST have requirement IDs. Core engines MUST map to contract groups in AWG-PLAT-001. |
| Known limitations | No deterministic kernel runtime yet. INV tests at this gate prove traceability and contract rejection of invalid typed input, not a 24-hour district simulation. |
| Unresolved risks | Human approval of draft normative documents; future kernel implementers may ignore catalogue tests unless CI keeps them failing-closed. |
| Release decision | MVP 0 pack-slice MAY proceed. MVP 1 MUST NOT start from planet scale and MUST NOT introduce an LLM into the state-transition path. |

## MVP 1 - One district, no AI dependency

### Scope
- local OSM extract;
- PostGIS spatial model;
- local gazetteer;
- local routing;
- PMTiles/Protomaps map;
- simulation clock;
- buildings and entrances;
- scheduled agents;
- valid journeys/movement;
- basic smart objects/occupancy;
- immutable event firehose;
- snapshot/replay;
- semantic zoom and clusters;
- building occupancy inspector.

### Definition of done
- agents cannot teleport in invariant tests;
- travel time and route constraints are enforced;
- building entry uses valid transitions;
- replay reproduces deterministic world state;
- map clustering never alters positions;
- scenario operates with required services offline;
- 24-hour simulated run completes without state-integrity failures under target test population.

### MVP 1 phase gate (ELE-147)

This gate closes the bounded correctness reference for MVP 1. It does not approve candidate third-party components, claim empirical realism, or establish production capacity.

| Gate field | MVP 1 record |
| --- | --- |
| Objectives | Prove one generated district can execute scheduled movement, occupancy, immutable event history, replay, and read-only map/inspector projections without AI or network access. |
| In-scope | Checksummed synthetic OSM XML; PostGIS spatial migration; local gazetteer and mode-aware route graph; PMTiles v3 presentation archive; 100 S2 agents; simulation clock; valid entrances; smart-object/building occupancy; snapshot/replay; semantic clusters; occupancy inspector. |
| Non-goals | Real-world OSM calibration; redistribution or production deployment of candidate PostgreSQL/PostGIS/Nominatim/Protomaps/Valhalla implementations; interactive map UI; distributed execution; empirical human-behaviour claims. |
| Dependencies | AWG-GOV-001, AWG-DOM-002, AWG-DOM-008, AWG-DOM-010, AWG-PLAT-002, AWG-PLAT-004, AWG-PLAT-006, AWG-PLAT-007, AWG-UX-002, AWG-UX-009, AWG-OPS-002, AWG-OPS-003. |
| Acceptance tests | AWG-TEST-MVP1-001 through AWG-TEST-MVP1-007; existing AWG-TEST-COV-004, 005, 010, 014-016, 031, 034, 037, 038; AWG-TEST-TIME-001; AWG-TEST-OBJ-001; AWG-TEST-KER-001. |
| Performance target | The 100-agent, 200-journey, 1,400-event, 24-hour profile completes in less than 5 seconds on documentation-pack CI with zero state-integrity errors. |
| Security/offline target | Runtime has zero external network dependencies, imports no AI provider, validates asset checksums, and uses generated geography only. |
| Validation evidence | `tests/test_mvp1_district.py`; `make mvp1`; `make validate`; `make test`; generated validation and traceability reports. |
| Documentation complete | Spatial authority, kernel behavior, reference performance budget, generated data provenance, risks, requirements, test mappings, and known limits are recorded. |
| Known limitations | Local graph is the executable routing authority for this fixture; the PostGIS migration is structurally checked but no production database, gazetteer daemon, renderer, or routing daemon is exercised. PMTiles contains one bounded presentation tile. |
| Unresolved risks | External-component legal/security approval; real OSM and indoor-data quality; production spatial/service integration; UI accessibility and frame-rate evidence; larger population and event-volume baselines. |
| Release decision | The MVP 1 bounded reference MAY proceed to MVP 2 classical NPC work. Production or external-data deployment MUST remain blocked until component approvals and integration gates are complete. |

## MVP 2 - Classical NPC and social systems

### Scope
- needs/drives;
- schedules/routines;
- utility AI;
- state machine/behavior tree/StateTree pattern;
- GOAP/HTN planning where needed;
- action channels/concurrency;
- smart-object reservations;
- relationships/households/groups;
- organizations;
- resources/ownership/basic transactions;
- perception gating.

### Definition of done
- agents already produce coherent daily activity without LLM calls;
- impossible concurrent actions are blocked;
- resource/ownership conservation tests pass;
- perception tests prevent global-state knowledge leakage.

### MVP 2 phase gate (ELE-147)

This gate closes the classical NPC correctness reference. It does not add bounded LLM adapters or claim empirically validated human behaviour.

| Gate field | MVP 2 record |
| --- | --- |
| Objectives | Prove scheduled agents already live in the district through needs, utility, action channels, households/organizations, conserved resources, and gated perception, with no LLM in the state path. |
| In-scope | Needs/drives; utility AI; GOAP-style eat plans; action channels; exclusive smart-object reservations; households; two generated organizations; token/meal/unique-asset conservation; co-location perception. |
| Non-goals | Ollama/OpenRouter adapters; dialogue realization; information-space social media; real-person populations; production GOAP/HTN engines; claiming Constitution acceptance. |
| Dependencies | AWG-GOV-001, AWG-DOM-003, AWG-DOM-005, AWG-DOM-006, AWG-DOM-009, AWG-DOM-010, AWG-DOM-011, AWG-PLAT-007, AWG-OPS-001, AWG-OPS-002. |
| Acceptance tests | AWG-TEST-MVP2-001 through AWG-TEST-MVP2-004; AWG-TEST-OBJ-001; AWG-TEST-PER-001; AWG-TEST-KER-001. |
| Performance target | The 100-agent 24-hour classical profile completes on documentation-pack CI with zero integrity errors and a matching replay checksum. |
| Security/offline target | No AI provider import; generated society data only; kernel remains the sole authority for transfers, reservations, and observations. |
| Validation evidence | `tests/test_mvp2_npc.py`; `make mvp2`; `make validate`; `make test`. |
| Documentation complete | Agent runtime, economy, perception, organization, requirements, tests, and known limits are recorded. |
| Known limitations | Hourly utility ticks, not a full behavior-tree authoring tool; one exclusive cafe counter; perception is place co-location only; households are generated pairs. |
| Unresolved risks | Scaling event volume from co-located observations; richer indoor perception; production planner adapters; human review of draft normative documents. |
| Release decision | The MVP 2 classical reference MAY proceed to MVP 3 bounded AI adapters. LLM output MUST remain unable to mutate authoritative state. |

## MVP 3 - Bounded AI adapters

### Scope
- AIProviderAdapter;
- Ollama implementation;
- OpenRouter implementation;
- structured intent proposal;
- dialogue realization;
- claim extraction;
- memory summarization;
- bounded option ranking;
- model provenance;
- deterministic fallback/degraded behavior.

### Definition of done
- switching Ollama/OpenRouter does not change domain schemas;
- malformed/timeout model output cannot mutate world state;
- recorded model output can be replayed without provider call;
- model/provider/prompt-policy versions are traceable.

## MVP 4 - Information world and virtual social platform

### Scope
- claims/evidence/beliefs;
- contextual trust;
- direct messages/group communication;
- public posts/comments/reposts/reactions;
- exposure/feed mechanics;
- information-space-only actors;
- bad actors/deception;
- fact-check/contact-source actions;
- provenance graph;
- information-space UI.

### Definition of done
- A->B->C->post->repost chains are reconstructable;
- belief is separate from world truth;
- social reactions do not imply belief automatically;
- corrections/retractions preserve original history;
- agents cannot know unexposed claims.

## MVP 5 - Multi-resolution scale and experimentation

### Scope
- S0-S4 fidelity levels;
- cohort/individual promotion/demotion;
- event-driven activation;
- distributed/partitioned execution where required;
- scenario branch comparison;
- validation/calibration framework;
- sensitivity runs;
- performance/cost dashboards.

### Definition of done
- scale benchmarks define population records vs active cognition separately;
- promotion/demotion conserves key state/resources;
- branch comparison distinguishes intervention effects from seed/model variance;
- validation reports expose limitations and uncertainty.

## Phase gate template

Every MVP gate must list:

- objectives;
- in-scope/non-goals;
- dependencies;
- acceptance tests;
- performance target;
- security/offline target;
- validation evidence;
- documentation complete;
- known limitations;
- unresolved risks;
- release decision.

## Failure modes

- Silent divergence between authoritative state and projections.
- A plugin or model bypasses validation or provenance controls.
- A dependency failure produces fabricated success rather than an explicit degraded or failed state.
- A schema or terminology change is introduced without versioning and migration notes.

## Security and privacy considerations

- Apply least privilege to plugins, model providers, data stores, and operator actions.
- Treat model output, imported data, agent messages, and social content as untrusted input.
- Record audit events for privileged changes and protect sensitive data according to classification.

## Performance and scale considerations

- Use event-driven activation, batching, caching, and level-of-detail policies before increasing hardware cost.
- Measure latency, throughput, memory, storage growth, and degradation behaviour under representative load.
- Do not trade away correctness, causality, or provenance to improve benchmark numbers.

## Acceptance criteria

- The defined inputs, outputs, states, and failure paths are testable.
- Normative requirements are linked to stable requirement IDs and acceptance-test IDs.
- At least one valid example and one invalid example are documented or represented in executable fixtures.
- Offline and degraded-mode behaviour is explicit.
- No LLM or visualization component can override authoritative state.

## Related documents

- AWG-GOV-001
- AWG-PLAT-001
- AWG-SCN-002
