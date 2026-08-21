---
title: Software Testing and Quality Strategy
document_id: AWG-OPS-002
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
- AWG-PLAT-002
linear_issue: null
supersedes: []
---

# Software Testing and Quality Strategy

## Purpose

Define unit, property, invariant, contract, integration, replay, performance, security, offline, migration, and accessibility testing.

## Status and authority

This document is normative. Its current status is **draft**. Where this document conflicts with the Simulation Constitution, the Constitution takes precedence.

## Scope

- Define unit, property, invariant, contract, integration, replay, performance, security, offline, migration, and accessibility testing.

## Non-goals

- This document does not authorize bypassing the simulation kernel, provenance model, security boundary, or event history.
- It does not claim that a plausible simulation output is an empirically validated forecast.
- It does not make a specific vendor, model, database, or rendering engine part of the core domain contract unless explicitly stated.

## Normative requirements

- The implementation must conform to the rules defined in this specification for software testing and quality strategy.
- All state-changing operations must use typed commands, validation, and append-only domain events where applicable.
- Any uncertainty, approximation, generated data, or external dependency must be explicitly identified and traceable.
- Implementations must preserve offline operation and provider replaceability unless a capability is explicitly declared optional.

## Detailed specification

## Test layers

### Unit tests
Pure domain calculations, reducers, validation rules, serializers, utility functions.

### Property/invariant tests
Examples:

- no location change without journey/intervention;
- resource quantities do not go negative unless model explicitly permits debt;
- exclusive capacity cannot exceed limit;
- belief updates never rewrite world truth;
- radial UI expansion cannot change position state.

### Contract tests
Every plugin implementation runs the same interface suite.

### Integration tests
OSM -> PostGIS -> routing -> journey -> event -> projection; social post -> exposure -> observation -> belief; scenario -> intervention -> branch -> comparison.

### Replay/determinism tests
Replay core events and recorded AI outputs to expected state checksums/projections.

### Load tests
Event throughput, active agents, cluster queries, spatial queries, replay speed, AI concurrency.

### Soak tests
Long simulated durations to expose event leaks, schedule drift, state growth, memory/queue leaks.

### Chaos/failure tests
Kill AI provider, routing adapter, projection consumer, or network service and verify authoritative state remains consistent/degrades safely.

### Security tests
Prompt injection, malformed plugin output, authorization, secret leakage, hostile social content, export permissions.

### Offline tests
Disable external networking and confirm configured offline scenario still works.

### UI tests
Accessibility, keyboard navigation, cluster semantics, branch/time state, visual regression, list alternatives, large-data virtualization.

## Quality gates

No MVP is done with known invariant failures. Failed validation is recorded, not hidden by changing the presentation.

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
- AWG-PLAT-002
