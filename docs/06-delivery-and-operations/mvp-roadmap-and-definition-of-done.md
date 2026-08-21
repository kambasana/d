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
