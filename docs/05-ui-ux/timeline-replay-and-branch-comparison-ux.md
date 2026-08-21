---
title: Timeline, Replay, and Branch Comparison UX
document_id: AWG-UX-005
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
- AWG-SCN-004
- AWG-UX-001
linear_issue: null
supersedes: []
---

# Timeline, Replay, and Branch Comparison UX

## Purpose

Define time navigation, causal event inspection, replay controls, branch creation, synchronized comparison, and investigation history.

## Status and authority

This document is normative. Its current status is **draft**. Where this document conflicts with the Simulation Constitution, the Constitution takes precedence.

## Scope

- Define time navigation, causal event inspection, replay controls, branch creation, synchronized comparison, and investigation history.

## Non-goals

- This document does not authorize bypassing the simulation kernel, provenance model, security boundary, or event history.
- It does not claim that a plausible simulation output is an empirically validated forecast.
- It does not make a specific vendor, model, database, or rendering engine part of the core domain contract unless explicitly stated.

## Normative requirements

- The implementation must conform to the rules defined in this specification for timeline, replay, and branch comparison ux.
- All state-changing operations must use typed commands, validation, and append-only domain events where applicable.
- Any uncertainty, approximation, generated data, or external dependency must be explicitly identified and traceable.
- Implementations must preserve offline operation and provider replaceability unless a capability is explicitly declared optional.

## Detailed specification

## Timeline

Display:

- simulation time;
- run start/end;
- important domain events;
- interventions;
- snapshots;
- branch points;
- selected-agent/place events;
- communication/claim events when filtered.

## Replay modes

Users should understand whether they are:

- viewing current live state;
- viewing a historical projection;
- replaying recorded events;
- simulating a new branch;
- running with live AI calls.

## Branching interaction

A branch action requires:

1. select time/event boundary;
2. name/describe intervention difference;
3. confirm inherited scenario/configuration;
4. explicitly show changed parameters/plugins/models/seeds;
5. create new branch identity.

## Comparison

Support synchronized map/time, delta metrics, selected-agent comparison, claim diffusion comparison, and side-by-side event timelines.

Avoid suggesting that divergence is caused only by the intervention if random/model configuration also differs.

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
- AWG-SCN-004
- AWG-UX-001
