---
title: Backup, Restore, and Disaster Recovery
document_id: AWG-OPS-008
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
- AWG-GOV-004
- AWG-PLAT-004
- AWG-OPS-004
linear_issue: null
supersedes: []
---

# Backup, Restore, and Disaster Recovery

## Purpose

Define backup scopes, recovery point and time objectives, snapshot consistency, restore testing, offline media, and corruption recovery.

## Status and authority

This document is normative. Its current status is **draft**. Where this document conflicts with the Simulation Constitution, the Constitution takes precedence.

## Scope

- Define backup scopes, recovery point and time objectives, snapshot consistency, restore testing, offline media, and corruption recovery.

## Non-goals

- This document does not authorize bypassing the simulation kernel, provenance model, security boundary, or event history.
- It does not claim that a plausible simulation output is an empirically validated forecast.
- It does not make a specific vendor, model, database, or rendering engine part of the core domain contract unless explicitly stated.

## Normative requirements

- Backups cover authoritative state, event history, scenario packages, registers, configuration digests, and required external-data manifests.
- Restore procedures are tested and record achieved recovery objectives.
- Encrypted or sensitive backups follow access and retention controls.
- A restore never silently merges incompatible branches or world identities.

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

- AWG-GOV-004
- AWG-PLAT-004
- AWG-OPS-004
