---
title: UI Application Architecture and Design System
document_id: AWG-UX-001
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
- AWG-PLAT-001
linear_issue: ELE-146
supersedes: []
---

# UI Application Architecture and Design System

## Purpose

Define the World Explorer, Scenario Studio, inspectors, information space, timeline, firehose, design system, offline client state, and rendering boundaries.

## Status and authority

This document is normative. Its current status is **draft**. Where this document conflicts with the Simulation Constitution, the Constitution takes precedence.

## Scope

- Define the World Explorer, Scenario Studio, inspectors, information space, timeline, firehose, design system, offline client state, and rendering boundaries.

## Non-goals

- This document does not authorize bypassing the simulation kernel, provenance model, security boundary, or event history.
- It does not claim that a plausible simulation output is an empirically validated forecast.
- It does not make a specific vendor, model, database, or rendering engine part of the core domain contract unless explicitly stated.

## Normative requirements

- The implementation must conform to the rules defined in this specification for ui application architecture and design system.
- All state-changing operations must use typed commands, validation, and append-only domain events where applicable.
- Any uncertainty, approximation, generated data, or external dependency must be explicitly identified and traceable.
- Implementations must preserve offline operation and provider replaceability unless a capability is explicitly declared optional.

## Detailed specification

## UX principle

The interface should let users move continuously between:

```text
society -> region -> city -> district -> street -> building -> room -> group -> individual
```

without forcing the renderer to draw every simulated person at every scale.

## Primary application shell

Recommended persistent regions:

```text
Top bar: world / scenario / branch / time / run state
Left rail: map layers, filters, scenario tools
Center: world/map/interior/graph visualization
Right inspector: selected entity/context
Bottom timeline: time, replay, branch markers, events
Optional lower panel: firehose / diagnostics / validation
```

## Core workspaces

### World Explorer
Map-first navigation, semantic zoom, clusters, density, flows, routes, events, buildings, selected entities.

### Scenario Studio
Scenario definition, interventions, assumptions, seeds, plugin/model versions, measurements, run/branch controls.

### Agent Inspector
Identity, current state, location/journey, schedule, goals, needs, relationships, beliefs, claims/evidence, recent events, source provenance, simulation fidelity.

### Place/Building Inspector
Geometry, entrances, access, occupancy, floors/rooms, resources, smart objects, queues, local routes, incidents, organizations.

### Information Space
Social/feed views, messages, claims, source lineage, exposure network, belief states, fact-check actions, bad-actor/campaign views where scenario permits.

### Timeline/Replay
Scrub simulation time, jump to events, compare current vs historical state, show branch point, follow causal chains.

### Firehose Explorer
Filter domain events by type, actor, place, claim, organization, scenario, branch, and causal parents.

### Comparison Workspace
Side-by-side or synchronized branch comparison with shared metrics and selected entities.

## Semantic zoom

Do not merely scale the same marker. Change displayed semantics by zoom/context:

- planet/country: density, aggregate flows, incidents, regional totals;
- city/district: clusters, important places, selected agents, movement corridors;
- street: smaller clusters, individual markers, vehicles, building occupancy;
- building: floors/rooms/occupants/objects/local routes;
- selected agent: detailed state, history, beliefs, plan, route, causal trace.

## Design system

### Token groups

Use semantic tokens rather than hard-coded component styling:

```text
color.background.*
color.surface.*
color.text.*
color.border.*
color.status.*
color.data.*
space.*
radius.*
elevation.*
typography.*
motion.*
z.*
```

Map/data colors should be assigned semantically (for example world-truth, belief, warning, intervention, uncertainty, selection) and tested in light/dark/high-contrast modes.

### Component families

- entity chips/identity badges;
- cluster markers;
- selected-agent marker;
- occupancy badges;
- timeline events;
- branch markers;
- provenance chain nodes;
- claim/confidence indicators;
- uncertainty badges;
- status pills;
- inspectors/panels;
- data tables/virtualized lists;
- command/intervention forms;
- event cards;
- map layer controls;
- comparison cards;
- validation metric cards.

## State semantics

Every component that represents simulation data should distinguish where relevant:

```text
observed/imported
simulated world truth
agent belief
inferred
synthetic/generated
estimated/aggregate
selected
stale/historical
uncertain/disputed
```

## Performance architecture

- Map rendering uses clustering/tiling and GPU-friendly layers where appropriate.
- Large tables/lists are virtualized.
- Firehose consumers use bounded buffers and pagination/streaming.
- Inspector queries fetch selected detail on demand.
- Historical scrubbing reads snapshots/projections rather than replaying the full world in the browser.
- Heavy spatial/graph aggregation belongs server-side or in workers, not the main UI thread.

## Offline UX

Show data/package availability explicitly. Do not display features that silently require internet. Local map/model/routing availability and package version should be inspectable.

## Explainability

Users should be able to answer:

- Where is this agent actually located?
- Why is this marker clustered?
- What does this agent know and why?
- Why did this action occur?
- What changed between branches?
- Which plugin/model/data source influenced this result?
- Is this number exact, sampled, estimated, or synthetic?

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
- AWG-PLAT-001
