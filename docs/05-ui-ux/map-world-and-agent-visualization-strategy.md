---
title: Map, World, and Agent Visualization Strategy
document_id: AWG-UX-007
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
- AWG-PLAT-005
- AWG-UX-001
- AWG-UX-002
linear_issue: null
supersedes: []
---

# Map, World, and Agent Visualization Strategy

## Purpose

Define the balance between aggregate world views, thousands of agent dots, clusters, flows, building occupancy, local embodied views, and selected-agent continuity.

## Status and authority

This document is normative. Its current status is **draft**. Where this document conflicts with the Simulation Constitution, the Constitution takes precedence.

## Scope

- Define the balance between aggregate world views, thousands of agent dots, clusters, flows, building occupancy, local embodied views, and selected-agent continuity.

## Non-goals

- This document does not authorize bypassing the simulation kernel, provenance model, security boundary, or event history.
- It does not claim that a plausible simulation output is an empirically validated forecast.
- It does not make a specific vendor, model, database, or rendering engine part of the core domain contract unless explicitly stated.

## Normative requirements

- The implementation must conform to the rules defined in this specification for map, world, and agent visualization strategy.
- All state-changing operations must use typed commands, validation, and append-only domain events where applicable.
- Any uncertainty, approximation, generated data, or external dependency must be explicitly identified and traceable.
- Implementations must preserve offline operation and provider replaceability unless a capability is explicitly declared optional.

## Detailed specification

## 14. Map, world and agent visualization strategy

### Verdict on the “thousands of dots” question

The instinct is correct, with one essential architectural separation:

> **The number of agents being simulated must not determine how many agents are rendered individually.**

Thousands of dots are useful in a raw operational or debugging view. They can reveal congestion, evacuation, crowd formation, migration, route choice and local activity. However, thousands of overlapping markers are usually poor as the default analytical interface because they hide density, overlap, uncertainty and movement patterns.

The system should therefore support **both**:

1. A raw individual-agent layer for debugging, inspection and demonstrations.
2. Scale-dependent aggregated representations for normal analysis.

The detailed “world” or embodied view is best used for a selected local area, street, building, floor, room or followed agent. A planet-scale 3D world containing every fully rendered person would be expensive, visually noisy and analytically weak.

### Separate simulation level of detail from visualization level of detail

These are independent systems.

#### Simulation level of detail

```text
S0 — Aggregate population
S1 — Statistical cohort or archetype
S2 — Persistent scheduled individual
S3 — Cognitive individual
S4 — Fully embodied local agent
```

#### Visualization level of detail

```text
V0 — Not individually rendered
V1 — Included in density, flow or aggregate cell
V2 — Included in a cluster
V3 — Rendered as an individual point or icon
V4 — Rendered as a detailed character or local embodied entity
```

An agent can be simulated as a persistent individual while being displayed only as part of an H3 cell or cluster. Conversely, a decorative point should never imply that a full LLM cognition loop is running behind it.

### Recommended spatial display hierarchy

| Geographic scale | Default visual representation | Optional detail |
|---|---|---|
| Planet | Regional aggregates, major flows, event zones and scenario boundaries | Selected countries, organizations or global routes |
| Country or large region | H3/grid aggregates, migration and transport flows, major incidents | Cohorts, selected agents and administrative comparisons |
| City or district | Clusters, density surfaces, activity areas, selected routes and active incidents | Individual agents, vehicles and buildings where useful |
| Street or neighbourhood | Individual agents, vehicles, queues, routes, entrances and local events | Perception ranges, conversations and object interactions |
| Building exterior | Entrances, exits, occupancy, queues, access state and selected occupants | Floor selector and internal route preview |
| Building interior | Floors, rooms, doors, stairs, lifts, objects, occupants and affordances | Fully embodied movement and interaction |
| Selected agent | Continuous location, route, activity, knowledge, goals and history | Agent-perspective view and causal explanation |

The exact map zoom thresholds should be configurable by world type, display size and density. They should not be hard-coded into the simulation model.

### Raw-dot mode should remain available

A raw-dot layer is valuable for:

- Simulation debugging.
- Verifying movement continuity.
- Detecting teleportation or route errors.
- Inspecting crowd behaviour.
- Demonstrating exact population positions.
- Following selected cohorts.
- Comparing simulated and observed mobility.

It should clearly state whether points represent:

- Exact positions.
- Interpolated positions.
- Last-known positions.
- Sampled agents.
- Synthetic positions within an aggregate.
- Privacy-preserving or deliberately coarsened locations.

### Do not use random movement to make the map look alive

A quiet residential street at 03:00 may correctly contain little or no movement. Adding artificial movement for visual excitement damages realism.

The map should be allowed to look:

- Quiet.
- Uneven.
- Concentrated.
- Repetitive.
- Temporarily inactive.
- Highly active only around specific events.

A serious simulation should optimize for **truthful state communication**, not permanent visual spectacle.

### Recommended view modes

The product should offer explicit view modes rather than one overloaded map:

```text
Operational Map
    2D geographic analysis, layers, events, routes and density

Local World
    Detailed street, site or neighbourhood scene

Building / Indoor
    Floors, rooms, indoor topology, occupants and affordances

Agent Follow
    Continuous selected-agent journey and state

Information Space
    Posts, messages, claims, exposure and diffusion

Debug / Omniscient
    Ground truth, raw events, invariants and exact state
```

Changing mode must preserve:

- Selected world and scenario.
- Simulation time.
- Selected entities.
- Filters.
- Branch.
- Camera context where possible.

The user should feel that they are changing the lens on one world, not opening unrelated applications.

---

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
- AWG-PLAT-005
- AWG-UX-001
- AWG-UX-002
