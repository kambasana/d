---
title: Map Layer and Visualization Semantics
document_id: AWG-UX-003
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
- AWG-UX-001
- AWG-UX-002
linear_issue: null
supersedes: []
---

# Map Layer and Visualization Semantics

## Purpose

Define the meaning, precedence, legends, uncertainty encoding, and truth-versus-projection boundaries of map layers.

## Status and authority

This document is normative. Its current status is **draft**. Where this document conflicts with the Simulation Constitution, the Constitution takes precedence.

## Scope

- Define the meaning, precedence, legends, uncertainty encoding, and truth-versus-projection boundaries of map layers.

## Non-goals

- This document does not authorize bypassing the simulation kernel, provenance model, security boundary, or event history.
- It does not claim that a plausible simulation output is an empirically validated forecast.
- It does not make a specific vendor, model, database, or rendering engine part of the core domain contract unless explicitly stated.

## Normative requirements

- The implementation must conform to the rules defined in this specification for map layer and visualization semantics.
- All state-changing operations must use typed commands, validation, and append-only domain events where applicable.
- Any uncertainty, approximation, generated data, or external dependency must be explicitly identified and traceable.
- Implementations must preserve offline operation and provider replaceability unless a capability is explicitly declared optional.

## Detailed specification

## Layer classes

### Base/context
- OSM/PMTiles vector map;
- labels/place names;
- terrain/elevation where packaged;
- administrative boundaries.

### Authoritative world-state projections
- agent positions;
- vehicles;
- journeys/routes;
- building occupancy;
- infrastructure state;
- incidents/interventions.

### Aggregate layers
- population density;
- movement flows;
- congestion;
- resource demand;
- organization influence.

### Information layers
- claim exposure;
- social cascades;
- message paths;
- belief distribution;
- fact-check/correction propagation.

### Analytical layers
- selected cohorts;
- risk states;
- scenario metrics;
- comparison deltas.

## Truth semantics

A layer must state whether it represents:

- exact authoritative state;
- aggregate estimate;
- agent belief;
- inferred analytics;
- scenario assumption;
- historical snapshot.

Do not render agent belief as objective world state without a clear visual distinction.

## Marker rules

- Geographic clusters summarize agents spread across screen-space/geographic bounds.
- Co-location markers represent genuine shared/near-identical place/coordinate occupancy.
- Analytical clusters represent filters and must look distinct from physical clusters.
- Selected/scenario-critical agents may remain individually visible through aggregation, but exceptions must be limited.

## Transition continuity

When zooming, clusters should visually divide/merge in a stable manner so users can follow continuity. Avoid unrelated marker blinking when possible.

## Building transition

At building selection/close zoom, allow transition from map footprint/occupancy to interior hierarchy if interior data exists. Never fabricate detailed interior geometry when unavailable; show level of detail/provenance.

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
- AWG-UX-001
- AWG-UX-002
