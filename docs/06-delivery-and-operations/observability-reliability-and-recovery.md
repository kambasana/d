---
title: Observability, Reliability, and Recovery
document_id: AWG-OPS-004
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
- AWG-PLAT-001
- AWG-PLAT-002
linear_issue: null
supersedes: []
---

# Observability, Reliability, and Recovery

## Purpose

Define service telemetry separately from simulation events, health indicators, failure isolation, degraded modes, recovery, and auditability.

## Status and authority

This document is normative. Its current status is **draft**. Where this document conflicts with the Simulation Constitution, the Constitution takes precedence.

## Scope

- Define service telemetry separately from simulation events, health indicators, failure isolation, degraded modes, recovery, and auditability.

## Non-goals

- This document does not authorize bypassing the simulation kernel, provenance model, security boundary, or event history.
- It does not claim that a plausible simulation output is an empirically validated forecast.
- It does not make a specific vendor, model, database, or rendering engine part of the core domain contract unless explicitly stated.

## Normative requirements

- The implementation must conform to the rules defined in this specification for observability, reliability, and recovery.
- All state-changing operations must use typed commands, validation, and append-only domain events where applicable.
- Any uncertainty, approximation, generated data, or external dependency must be explicitly identified and traceable.
- Implementations must preserve offline operation and provider replaceability unless a capability is explicitly declared optional.

## Detailed specification

## Separate observability planes

### Simulation firehose
Domain events describing the world and agents.

### Software telemetry
Infrastructure metrics/traces/logs such as CPU, GPU, queue depth, model latency, errors, and health.

Do not conflate them.

## Health model

Each service/adapter exposes healthy, degraded, unavailable, and configuration/version status where applicable.

## Reliability principles

- authoritative writes are atomic/idempotent or have explicit compensation;
- projection failures cannot corrupt world truth;
- consumers maintain offsets/checkpoints;
- AI/routing failures produce bounded explicit outcomes;
- snapshots are validated before relying on them;
- restore includes event continuity/integrity checks.

## Recovery

Define per deployment:

- event-store backup/durability;
- snapshot schedule;
- spatial database backup;
- scenario/data/model package checksums;
- restore test cadence;
- RPO/RTO targets when productionized.

## Debugging

A developer should be able to trace:

```text
observation -> belief/goal -> decision policy/model call -> command -> validation -> events -> state projection
```

for selected important agent actions.

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

- AWG-PLAT-001
- AWG-PLAT-002
