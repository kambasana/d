---
title: System Architecture
document_id: AWG-PLAT-001
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
linear_issue: null
supersedes: []
---

# System Architecture

## Purpose

Define the service boundaries and data planes for the world kernel, geospatial systems, agents, information space, scenarios, event history, AI adapters, and projections.

## Status and authority

This document is normative. Its current status is **draft**. Where this document conflicts with the Simulation Constitution, the Constitution takes precedence.

## Scope

- Define the service boundaries and data planes for the world kernel, geospatial systems, agents, information space, scenarios, event history, AI adapters, and projections.

## Non-goals

- This document does not authorize bypassing the simulation kernel, provenance model, security boundary, or event history.
- It does not claim that a plausible simulation output is an empirically validated forecast.
- It does not make a specific vendor, model, database, or rendering engine part of the core domain contract unless explicitly stated.

## Normative requirements

- The implementation must conform to the rules defined in this specification for system architecture.
- All state-changing operations must use typed commands, validation, and append-only domain events where applicable.
- Any uncertainty, approximation, generated data, or external dependency must be explicitly identified and traceable.
- Implementations must preserve offline operation and provider replaceability unless a capability is explicitly declared optional.

## Detailed specification

## Architectural stance

AWG is an event-driven simulation platform with a deterministic authoritative core and replaceable adapters around it.

## Core engines

```text
World Runtime
├── World Graph / Domain State
├── Time and Scheduling Engine
├── Geospatial Engine
├── Navigation and Mobility Engine
├── Simulation / Physics / Constraint Engine
├── Agent Runtime
├── Human Systems Engine
├── Information / Epistemic Engine
├── Trust and Reputation Engine
├── Social / Information Platform Engine
├── Organization / Institution Engine
├── Economy / Resource Engine
├── Scenario / Intervention Engine
├── Event Firehose / Replay Engine
└── Projection / Query Engine
```

## Adapter boundary

```text
Core contracts
├── AIProviderAdapter
├── EmbeddingAdapter
├── GazetteerAdapter
├── RoutingAdapter
├── MobilityAdapter
├── LocalNavigationAdapter
├── PhysicsAdapter
├── StorageAdapter
├── EventBusAdapter
├── SocialPlatformAdapter
├── WeatherAdapter
├── AnalyticsAdapter
└── VisualizationAdapter
```

Adapters may be replaced without changing core domain semantics.

## Four data planes

### World truth plane
Authoritative positions, physical/object state, ownership, resources, infrastructure, validated actions, scenario conditions, and simulation clock.

### Agent epistemic plane
Observations, memories, claims, beliefs, trust, uncertainty, contradictions, and information-access history.

### Projection plane
Maps, PMTiles, dashboards, timelines, social feeds, search indexes, clusters, heatmaps, and analytical graph projections.

### Software telemetry plane
CPU/GPU, queue depth, token counts, latency, errors, traces, health, and infrastructure metrics.

Do not merge telemetry with simulation domain events.

## Execution loop

The platform need not use one global high-frequency tick. It can combine event scheduling, fixed-step local systems, and wake-up triggers.

```text
scheduled event / external intervention / agent wake-up
        -> observation/state preparation
        -> decision policy or current action
        -> typed command
        -> validation
        -> deterministic execution
        -> domain events
        -> state reducers
        -> new observations/triggers/projections
```

## Separation of concerns

- AI proposes or interprets within bounded schemas.
- Geospatial/routing systems answer traversability and journey questions.
- Physics/constraint systems resolve physical validity.
- Domain services own state transitions.
- Event service records history.
- Projection services optimize reads and UI.
- Scenario service injects declared interventions but cannot rewrite agent decisions silently.

## Failure model

A failed adapter call cannot partially mutate authoritative state. Commands either fail before commit, emit explicit partial/failure events according to domain rules, or use an approved compensation workflow.

## Offline posture

Core dependencies have local deployment paths. Remote AI providers and external data feeds are optional adapters, not mandatory assumptions.

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
