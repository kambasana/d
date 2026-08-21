---
title: Spatial World, Mobility, and Building Specification
document_id: AWG-DOM-002
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
- AWG-DOM-001
linear_issue: ELE-138
supersedes: []
---

# Spatial World, Mobility, and Building Specification

## Purpose

Define authoritative geography, OSM-derived topology, gazetteer semantics, routing, journeys, buildings, interiors, occupancy, and synthetic-world spatial rules.

## Status and authority

This document is normative. Its current status is **draft**. Where this document conflicts with the Simulation Constitution, the Constitution takes precedence.

## Scope

- Define authoritative geography, OSM-derived topology, gazetteer semantics, routing, journeys, buildings, interiors, occupancy, and synthetic-world spatial rules.

## Non-goals

- This document does not authorize bypassing the simulation kernel, provenance model, security boundary, or event history.
- It does not claim that a plausible simulation output is an empirically validated forecast.
- It does not make a specific vendor, model, database, or rendering engine part of the core domain contract unless explicitly stated.

## Normative requirements

- The implementation must conform to the rules defined in this specification for spatial world, mobility, and building specification.
- All state-changing operations must use typed commands, validation, and append-only domain events where applicable.
- Any uncertainty, approximation, generated data, or external dependency must be explicitly identified and traceable.
- Implementations must preserve offline operation and provider replaceability unless a capability is explicitly declared optional.

## Detailed specification

## Spatial authority

For real-world scenarios, authoritative spatial state is built from versioned OSM-derived geometry/topology plus approved supplemental datasets. PostGIS is the default candidate for queryable spatial truth. Routing/navigation systems derive traversable networks from approved sources.

PMTiles/Protomaps is a first-class offline presentation/distribution option, not authoritative topology.

Nominatim is a gazetteer for place/address resolution, not a physical traversal engine.

## Required spatial concepts

```text
Planet -> Region -> City -> District -> Place -> Building -> Floor -> Room/Area -> Object
```

The hierarchy is semantic, not always strictly administrative. An agent should be able to answer both coordinate and place-context questions.

## OSM provenance

Preserve where available:

- node/way/relation IDs;
- extract timestamp/version;
- original tags;
- original and derived geometry references;
- transformation pipeline/version;
- access/routing interpretation;
- synthetic/observed status.

## Synthetic geography

A synthetic world must still provide coherent:

- roads and paths;
- intersections/topology;
- buildings and entrances;
- addresses/places or equivalent naming system;
- administrative/spatial containment;
- transport networks;
- barriers and crossings;
- traversable indoor/outdoor transitions.

Synthetic agents must not treat invented place names as teleport destinations.

## Journey state machine

```text
Planned
  -> Preparing
  -> Departed
  -> InTransit
  -> Rerouting / Waiting / Interrupted (optional)
  -> Arrived
  -> Completed

or
  -> Failed / Cancelled
```

A journey records origin, destination, mode, route/legs, departure, estimated/actual times, route changes, interruptions, and arrival.

## Layered mobility engines

Candidate architecture:

```text
Regional/multimodal route: Valhalla-like adapter
Activity plans/replanning: MATSim-like patterns/adapter
Microscopic traffic: SUMO-like adapter
Local/building navigation: Recast/Detour-like navmesh
Immediate movement/collision: local controller/physics
```

No single engine is assumed to solve every scale.

## Movement constraints

An agent cannot:

- travel three miles in one second;
- pass through inaccessible geometry;
- cross a river without a valid crossing/mode;
- enter a building without a valid entrance/transition unless an explicit exceptional rule exists;
- use a transport mode without access/capability;
- occupy exclusive capacity already reserved by another entity;
- appear at a destination without journey/intervention history.

## Buildings

Buildings support:

- shell/footprint;
- entrances and access rules;
- floors/levels;
- rooms/areas;
- stairs/lifts/transitions;
- occupancy/capacity;
- smart objects/affordances;
- local navigation;
- queues and reservations;
- optional visibility/hearing models.

At street scale, a building may be represented by an occupancy count. At interior scale, the same occupants can resolve into floor/room/individual views.

## Co-location

Co-location is a world-state concept. UI radial expansion is only a selection projection. An expanded marker does not change physical position.

## Mobility events

Minimum event family:

```text
JourneyPlanned
JourneyStarted
RouteSelected
JourneyProgressed
JourneyDelayed
JourneyRerouted
JourneyInterrupted
JourneyArrived
JourneyCancelled
LocationEntered
LocationExited
AccessDenied
```

## Offline requirement

A packaged city scenario should be able to operate using local OSM extract, local spatial database, local gazetteer, local routing data, local PMTiles, and local model provider where configured.

## MVP 1 reference district

`examples/mvp1-district/bundle.json` is the bounded, generated spatial input for the MVP 1 acceptance profile. It contains no real-person or externally sourced geography. The bundle includes:

- an OSM 0.6 XML extract with generated nodes, ways, access tags, and entrances;
- a PostGIS migration for places, buildings, entrances, route nodes, and route edges;
- a Nominatim-compatible local gazetteer projection;
- a deterministic, mode-aware local routing graph;
- a standards-valid PMTiles v3 presentation archive;
- checksums and explicit generated-data provenance.

The reference kernel MUST route through accessible graph edges, MUST consume time using the configured mode speed, and MUST terminate building journeys at a declared entrance. The PMTiles archive remains presentation-only and MUST NOT be used to reconstruct routing or authoritative positions.

Production adoption or redistribution of PostgreSQL, PostGIS, Nominatim, Protomaps, or Valhalla remains subject to the component approvals in `registers/open-source-components.yaml`. The reference runtime does not import or redistribute those candidate implementations.

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
- AWG-DOM-001
