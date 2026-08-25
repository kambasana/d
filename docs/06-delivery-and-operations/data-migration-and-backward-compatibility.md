---
title: Data Migration and Backward Compatibility
document_id: AWG-OPS-007
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
- AWG-PLAT-002
- AWG-PLAT-003
- AWG-PLAT-004
- AWG-OPS-005
linear_issue: null
supersedes: []
---

# Data Migration and Backward Compatibility

## Purpose

Define migrations for schemas, events, snapshots, scenarios, plugins, projections, datasets, and model records.

## Status and authority

This document is normative. Its current status is **draft**. Where this document conflicts with the Simulation Constitution, the Constitution takes precedence.

## Scope

- Define migrations for schemas, events, snapshots, scenarios, plugins, projections, datasets, and model records.

## Non-goals

- This document does not authorize bypassing the simulation kernel, provenance model, security boundary, or event history.
- It does not claim that a plausible simulation output is an empirically validated forecast.
- It does not make a specific vendor, model, database, or rendering engine part of the core domain contract unless explicitly stated.

## Normative requirements

- Breaking schema changes provide migration or explicit unsupported-version handling.
- Historical events remain readable and are not rewritten merely to match a new schema.
- Projection rebuilds are distinguished from authoritative data migrations.
- Migration execution is idempotent or safely resumable and produces audit evidence.

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

- AWG-PLAT-002
- AWG-PLAT-003
- AWG-PLAT-004
- AWG-OPS-005
