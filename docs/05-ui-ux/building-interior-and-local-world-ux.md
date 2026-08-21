---
title: Building, Interior, and Local World UX
document_id: AWG-UX-009
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
- AWG-DOM-002
- AWG-DOM-010
- AWG-UX-001
- AWG-UX-002
linear_issue: null
supersedes: []
---

# Building, Interior, and Local World UX

## Purpose

Define entry from map to building, floors, rooms, entrances, corridors, lifts, stairs, objects, occupants, activities, and local routes.

## Status and authority

This document is normative. Its current status is **draft**. Where this document conflicts with the Simulation Constitution, the Constitution takes precedence.

## Scope

- Define entry from map to building, floors, rooms, entrances, corridors, lifts, stairs, objects, occupants, activities, and local routes.

## Non-goals

- This document does not authorize bypassing the simulation kernel, provenance model, security boundary, or event history.
- It does not claim that a plausible simulation output is an empirically validated forecast.
- It does not make a specific vendor, model, database, or rendering engine part of the core domain contract unless explicitly stated.

## Normative requirements

- The UI preserves continuity from geographic location to entrance, floor, room, object, and agent.
- Exact, estimated, room-level, building-level, and aggregate positions are visually distinguished.
- Large occupancy is summarized by building, floor, zone, or room before individual rendering.
- Radial expansion is used only as a selection aid and never implies physical movement.

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

- AWG-DOM-002
- AWG-DOM-010
- AWG-UX-001
- AWG-UX-002
