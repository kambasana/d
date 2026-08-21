---
title: Scenario Definition and Experiment Protocol
document_id: AWG-SCN-001
status: draft
version: 0.2.0
last_updated: '2026-08-20'
normative: true
owners:
- AWG architecture
audience:
- engineering
- research
- product
depends_on:
- AWG-GOV-001
- AWG-DOM-001
- AWG-PLAT-002
linear_issue: ELE-144
supersedes: []
---

# Scenario Definition and Experiment Protocol

## Purpose

Define versioned scenario packages, initial state, seeds, interventions, measurements, stop conditions, run records, and reproducible branches.

## Status and authority

This document is normative. Its current status is **draft**. Where this document conflicts with the Simulation Constitution, the Constitution takes precedence.

## Scope

- Define versioned scenario packages, initial state, seeds, interventions, measurements, stop conditions, run records, and reproducible branches.

## Non-goals

- This document does not authorize bypassing the simulation kernel, provenance model, security boundary, or event history.
- It does not claim that a plausible simulation output is an empirically validated forecast.
- It does not make a specific vendor, model, database, or rendering engine part of the core domain contract unless explicitly stated.

## Normative requirements

- The implementation must conform to the rules defined in this specification for scenario definition and experiment protocol.
- All state-changing operations must use typed commands, validation, and append-only domain events where applicable.
- Any uncertainty, approximation, generated data, or external dependency must be explicitly identified and traceable.
- Implementations must preserve offline operation and provider replaceability unless a capability is explicitly declared optional.

## Detailed specification

## Scenario is data, not a prompt

A scenario is a versioned package containing enough information to reconstruct the intended experiment.

## Required scenario metadata

- scenario_id and version;
- title/purpose;
- intended use and non-use;
- base world and geographic extent;
- simulation start time/calendar/time zone;
- population/cohort inputs and synthesis method;
- organizations/institutions;
- infrastructure/resources;
- social/information networks;
- enabled domain systems;
- plugin versions/configurations;
- AI model/prompt-policy references;
- random seeds/streams;
- initial conditions;
- scheduled exogenous events;
- explicit interventions;
- measurements/KPIs;
- validation datasets/targets;
- stop conditions;
- known assumptions/limitations.

## Branch structure

```text
Baseline
├── Branch A: road closure
├── Branch B: price intervention
└── Branch C: information intervention
```

Branches share history to the declared branch point. Differences after the branch point must be attributable to interventions, randomness, model nondeterminism, or changed configuration that is explicitly recorded.

## Intervention types

Examples:

- close road/bridge/building;
- change public transport;
- remove electricity/service;
- change weather/environment;
- change price/resource availability;
- introduce policy/law;
- change organizational leadership;
- create public message/news/social post;
- introduce misinformation/bad actor;
- add/remove employer/service;
- trigger disaster/infrastructure failure.

The scenario engine changes conditions; it does not directly script every agent response.

## Experiment run record

Each run records:

- run_id;
- scenario/version;
- branch;
- execution start/end;
- code/build/version;
- plugin/model versions;
- seeds;
- source dataset versions;
- configuration hashes;
- hardware/runtime metadata relevant to reproducibility;
- snapshots/event ranges;
- validation outputs.

## Stop conditions

Examples include fixed simulation horizon, event condition, convergence criterion, resource exhaustion, or operator stop. Stop reason is recorded.

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
- AWG-DOM-001
- AWG-PLAT-002
