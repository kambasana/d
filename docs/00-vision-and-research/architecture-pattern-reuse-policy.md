---
title: Architecture Pattern Reuse Policy
document_id: AWG-VIS-006
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
- AWG-VIS-004
- AWG-GOV-001
linear_issue: null
supersedes: []
---

# Architecture Pattern Reuse Policy

## Purpose

Define how established game, simulation, geospatial, distributed-systems, and AI patterns are adopted without copying unsuitable implementations.

## Status and authority

This document is normative. Its current status is **draft**. Where this document conflicts with the Simulation Constitution, the Constitution takes precedence.

## Scope

- Define how established game, simulation, geospatial, distributed-systems, and AI patterns are adopted without copying unsuitable implementations.

## Non-goals

- This document does not authorize bypassing the simulation kernel, provenance model, security boundary, or event history.
- It does not claim that a plausible simulation output is an empirically validated forecast.
- It does not make a specific vendor, model, database, or rendering engine part of the core domain contract unless explicitly stated.

## Normative requirements

- Reuse proven concepts such as perception systems, blackboards, utility AI, behaviour trees, StateTree, GOAP/HTN, smart objects, reservations, event sourcing, and adaptive level of detail.
- Do not replace deterministic navigation, physics, ownership, or action execution with natural-language narration.
- Separate pattern reuse from source-code reuse and record licence implications independently.
- Prototype integrations behind adapters and require contract tests before adoption.

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

- AWG-VIS-004
- AWG-GOV-001
