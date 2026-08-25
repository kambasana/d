---
title: Scenario Cards, Model Cards, and Limitations
document_id: AWG-SCN-008
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
- AWG-GOV-006
- AWG-SCN-001
- AWG-SCN-002
- AWG-SCN-006
linear_issue: null
supersedes: []
---

# Scenario Cards, Model Cards, and Limitations

## Purpose

Define concise disclosure artifacts for scenarios, agent policies, AI models, datasets, validation scope, risks, and prohibited interpretations.

## Status and authority

This document is normative. Its current status is **draft**. Where this document conflicts with the Simulation Constitution, the Constitution takes precedence.

## Scope

- Define concise disclosure artifacts for scenarios, agent policies, AI models, datasets, validation scope, risks, and prohibited interpretations.

## Non-goals

- This document does not authorize bypassing the simulation kernel, provenance model, security boundary, or event history.
- It does not claim that a plausible simulation output is an empirically validated forecast.
- It does not make a specific vendor, model, database, or rendering engine part of the core domain contract unless explicitly stated.

## Normative requirements

- Every released scenario has a scenario card describing purpose, population, geography, interventions, assumptions, validation, limitations, and intended use.
- Every AI or learned component has a model record describing provider, version, role, input/output bounds, fallback, and evaluation.
- Limitations are carried into exports and stakeholder reports.

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

- AWG-GOV-006
- AWG-SCN-001
- AWG-SCN-002
- AWG-SCN-006
