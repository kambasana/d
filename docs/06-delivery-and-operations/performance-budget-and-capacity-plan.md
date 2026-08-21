---
title: Performance Budget and Capacity Plan
document_id: AWG-OPS-003
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
- AWG-PLAT-005
- AWG-UX-001
linear_issue: null
supersedes: []
---

# Performance Budget and Capacity Plan

## Purpose

Define measurable budgets for agents, events, AI calls, map rendering, storage, replay, snapshots, recovery, and offline hardware profiles.

## Status and authority

This document is normative. Its current status is **draft**. Where this document conflicts with the Simulation Constitution, the Constitution takes precedence.

## Scope

- Define measurable budgets for agents, events, AI calls, map rendering, storage, replay, snapshots, recovery, and offline hardware profiles.

## Non-goals

- This document does not authorize bypassing the simulation kernel, provenance model, security boundary, or event history.
- It does not claim that a plausible simulation output is an empirically validated forecast.
- It does not make a specific vendor, model, database, or rendering engine part of the core domain contract unless explicitly stated.

## Normative requirements

- The implementation must conform to the rules defined in this specification for performance budget and capacity plan.
- All state-changing operations must use typed commands, validation, and append-only domain events where applicable.
- Any uncertainty, approximation, generated data, or external dependency must be explicitly identified and traceable.
- Implementations must preserve offline operation and provider replaceability unless a capability is explicitly declared optional.

## Detailed specification

## Principle

Use benchmark profiles rather than vague claims such as "supports millions of agents".

## Metrics

- population records loaded;
- S0/S1 updates per simulated hour;
- S2 scheduled agents active;
- S3 cognitive decisions per simulated hour;
- S4 embodied agents in local area;
- commands/events per second;
- spatial/routing queries per second;
- snapshot size/time;
- replay throughput;
- UI cluster query latency;
- map frame rate;
- inspector response latency;
- AI calls/tokens/latency per simulated hour;
- storage growth per simulated day.

## Budget strategy

Set different profiles for developer laptop, offline workstation, LAN cluster, and distributed deployment.

## AI cost control

- event-driven activation;
- novelty detection;
- deterministic/classical fallback;
- smaller model routing for simple tasks;
- cached/compiled policies;
- batchable inference where safe;
- explicit per-run token/call budgets.

## UI budget

- do not render all agents individually when clustered;
- use tile/cluster aggregation;
- virtualize long lists;
- avoid main-thread graph/layout work for large networks;
- stream only visible/selected detail.

Numeric targets are added only after baseline benchmarks are measured.

## MVP 1 baseline profile

The first executable baseline is `validation:mvp1-reference-district-v1`:

| Measure | Acceptance target |
| --- | ---: |
| Population records / S2 scheduled agents | 100 / 100 |
| Simulated duration | 24 hours |
| Scheduled journeys | 200 |
| Expected domain events | 1,400 |
| State-integrity failures | 0 |
| Replay state checksum | identical |
| External network dependencies | 0 |
| Wall-clock test budget | less than 5 seconds on the documentation-pack CI runner |

This target measures a small dependency-free correctness fixture, not PostGIS query throughput, map frame rate, or production capacity. Those budgets require measured adapter and UI baselines before they can gate a production deployment.

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

- AWG-PLAT-005
- AWG-UX-001
