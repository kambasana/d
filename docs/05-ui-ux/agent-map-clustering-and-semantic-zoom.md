---
title: Agent Map Clustering, Semantic Zoom, and Co-Location Interaction
document_id: AWG-UX-002
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
linear_issue: ELE-146
supersedes: []
---

# Agent Map Clustering, Semantic Zoom, and Co-Location Interaction

## Purpose

Define count clusters, geographic versus co-location versus analytical clusters, zoom-to-bounds, radial expansion, building drill-down, and selected-agent persistence.

## Status and authority

This document is normative. Its current status is **draft**. Where this document conflicts with the Simulation Constitution, the Constitution takes precedence.

## Scope

- Define count clusters, geographic versus co-location versus analytical clusters, zoom-to-bounds, radial expansion, building drill-down, and selected-agent persistence.

## Non-goals

- This document does not authorize bypassing the simulation kernel, provenance model, security boundary, or event history.
- It does not claim that a plausible simulation output is an empirically validated forecast.
- It does not make a specific vendor, model, database, or rendering engine part of the core domain contract unless explicitly stated.

## Normative requirements

- The implementation must conform to the rules defined in this specification for agent map clustering, semantic zoom, and co-location interaction.
- All state-changing operations must use typed commands, validation, and append-only domain events where applicable.
- Any uncertainty, approximation, generated data, or external dependency must be explicitly identified and traceable.
- Implementations must preserve offline operation and provider replaceability unless a capability is explicitly declared optional.

## Detailed specification

## Purpose

This document defines how large populations of simulated agents should be represented and explored on a map without rendering thousands of unreadable markers.

The interface must preserve the distinction between:

- the agent's authoritative physical position in the simulation;
- the visual representation used at the current zoom level;
- a geographic cluster containing agents spread across an area;
- a co-location cluster containing agents at the same place or nearly identical coordinates;
- an analytical grouping created by filters rather than physical proximity.

The central principle is:

> The simulation determines where agents actually are. The visualization determines how those agents are summarized, clustered, expanded, and selected at the current viewing scale.

Clustering is therefore a presentation technique. It must never silently change agent positions or imply movement that did not occur.

---

## 1. Core Interaction Model

At distant zoom levels, the map should not draw every agent as an individual marker. It should show count-based cluster indicators representing the agents contained in a visible area.

For example:

```text
       248
```

As the user zooms in, the cluster progressively divides:

```text
248 agents
    ↓
83     94     71
    ↓
18  22  14  29  11
    ↓
individual agent indicators
```

This provides a continuous path from population-scale understanding to individual inspection.

The expected interaction sequence is:

```text
Planet or region
    ↓
Large population clusters
    ↓
City and district clusters
    ↓
Street-level groups
    ↓
Building or place occupancy
    ↓
Floor or room occupancy
    ↓
Individual agent
```

---

## 2. Semantic Zoom

The map should use semantic zoom rather than simply making the same markers larger or smaller.

Different zoom levels should display different kinds of information.

### 2.1 Planet and country scale

Show:

- aggregate population density;
- regional counts;
- major movement flows;
- migration patterns;
- incident areas;
- infrastructure disruptions;
- high-level information diffusion;
- organization or faction influence.

Do not attempt to display individual agents at this scale.

### 2.2 Regional and city scale

Show:

- count-based geographic clusters;
- density cells or heatmaps;
- important buildings and places;
- selected or scenario-critical agents;
- movement corridors;
- active events;
- filtered analytical groups.

### 2.3 District and street scale

Show:

- smaller agent clusters;
- individual agents where markers no longer overlap;
- vehicles;
- routes;
- queues;
- building occupancy indicators;
- nearby communication or incident indicators.

### 2.4 Building and interior scale

Show:

- entrances;
- floors;
- rooms;
- corridors;
- lifts and stairs;
- objects and affordances;
- occupants;
- local routes;
- conversations and activities;
- local visibility or hearing relationships where enabled.

### 2.5 Selected-agent scale

Show:

- authoritative position;
- current activity;
- route and destination;
- physical state;
- current plan;
- known information;
- beliefs and confidence;
- relationships;
- recent causal history;
- relevant firehose events.

---

## 3. Separate Simulation and Visualization Levels of Detail

Simulation fidelity and display fidelity must be independent.

### 3.1 Simulation levels

```text
L0 — Aggregate population
L1 — Statistical or archetype cohort
L2 — Scheduled individual
L3 — Cognitive individual
L4 — Fully embodied local agent
```

### 3.2 Visualization levels

```text
V0 — Not individually rendered
V1 — Included in density or heatmap layer
V2 — Included in count-based cluster
V3 — Shown as an individual map indicator
V4 — Shown as a detailed avatar or local character
```

An agent may be simulated as an individual while appearing only inside a cluster because the user is zoomed out.

Similarly, an individual marker does not mean that the agent is currently running a high-cost LLM reasoning loop.

---

## 4. Three Different Cluster Types

The interface should not use one generic cluster concept for every situation.

### 4.1 Geographic cluster

A geographic cluster contains agents distributed across an area of the map.

Example meaning:

```text
248 agents within the displayed area
```

The agents may occupy different streets, buildings, or routes.

Primary action:

```text
Click cluster
    ↓
Zoom to the geographic bounds of its members
    ↓
Cluster divides into smaller clusters
```

Secondary actions may include:

- show summary;
- open agent list;
- follow the cluster;
- filter by state or group;
- inspect movement flows.

A geographic cluster should not normally explode all agents around one artificial centre because doing so would hide their real spatial distribution.

### 4.2 Co-location cluster

A co-location cluster contains agents occupying the same place, room, vehicle, entrance, object interaction point, or nearly identical coordinate.

Example meaning:

```text
18 agents at Café Orion
```

Primary actions may include:

- expand agents radially;
- enter the place or building;
- open occupant list;
- inspect activities;
- view room, floor, or vehicle occupancy.

### 4.3 Analytical cluster

An analytical cluster groups agents because of an active query or filter rather than because they occupy the same physical point.

Examples:

- agents affected by an incident;
- agents who believe a particular claim;
- agents exposed to a specific social post;
- members of an organization;
- agents currently travelling;
- agents sharing a risk state;
- agents participating in the same information cascade.

Analytical clusters must use a visually distinct treatment so users do not confuse them with physical co-location.

---

## 5. Cluster Indicator Design

A cluster marker should communicate at least:

- number of represented agents;
- cluster type;
- selection state;
- alert or incident status where relevant;
- whether the count is exact, sampled, or estimated;
- whether one or more selected agents are inside it.

A basic cluster may appear as:

```text
   ┌─────┐
   │ 248 │
   └─────┘
```

A tooltip or accessible label should state the meaning precisely:

```text
248 agents within this displayed area
```

or:

```text
18 agents at Café Orion
```

The wording must distinguish aggregation from actual shared location.

### 5.1 Optional encoded attributes

A cluster may also communicate limited secondary information, such as:

- dominant activity;
- movement direction;
- incident involvement;
- information exposure;
- selected-agent presence;
- proportion travelling;
- proportion inside buildings.

These encodings should remain restrained. A cluster marker must not become an unreadable dashboard.

---

## 6. Default Click Behaviour

Different cluster types should have different default actions.

### Geographic cluster

Default:

```text
Zoom to member bounds
```

Context menu:

```text
248 agents

[Zoom to agents]
[Show summary]
[Open agent list]
[Follow this cluster]
[Filter members]
```

### Co-location cluster

Default:

```text
Open co-location interaction
```

Context menu:

```text
18 agents at Café Orion

[Expand agents]
[Enter building]
[Open occupant list]
[Show activities]
```

### Analytical cluster

Default:

```text
Open analytical summary
```

Context menu:

```text
76 agents exposed to Claim-482

[Show members]
[Show information path]
[Compare beliefs]
[View geographic spread]
```

---

## 7. Radial Expansion for Overlapping Agents

When several agents remain visually overlapped at the maximum useful zoom level, selecting the combined marker may open an anchored radial expansion.

Example:

```text
              A3

       A2             A4

A1             10             A5

       A8             A6

              A7
```

The centre represents the real shared location. The outer indicators are temporary selection controls.

Thin connector lines may make the relationship explicit:

```text
              ● A3
               │
       ● A2 ─── ● ─── ● A4
               │
              ● A5
```

### 7.1 Non-negotiable rule

> Radial expansion is a visual selection aid. It must never imply that agents physically moved away from the shared location.

The original coordinate, building, room, vehicle, or object interaction point remains authoritative.

### 7.2 Appropriate uses

Use radial expansion when:

- agents share the same coordinate;
- agents occupy the same point-like place;
- markers remain overlapped at close zoom;
- the group is small enough to inspect;
- the user explicitly asks to expand the occupants.

### 7.3 Inappropriate uses

Do not use radial expansion when:

- the agents are spread across multiple streets;
- a normal zoom-to-bounds action would reveal their real positions;
- the cluster contains too many agents;
- the expansion would cover unrelated map features;
- the user needs an accurate geographic comparison.

---

## 8. Maximum Radial Size

Radial expansion should be limited to a modest number of agents.

A practical design target is approximately 8 to 12 directly visible agents, although the exact value should depend on:

- viewport size;
- input method;
- marker size;
- accessibility settings;
- interior versus exterior context;
- device performance.

For larger co-located groups, use a structured occupant browser.

Example:

```text
Central Station
Occupants: 246

By area:
- Main concourse: 104
- Platforms: 83
- Shops: 31
- Offices: 18
- Entrances: 10
```

The user can then descend into a smaller place or sub-area before selecting individuals.

---

## 9. Building-Level Occupancy Navigation

Buildings should provide a hierarchical occupancy model rather than exposing hundreds of overlapping agent markers at the building centroid.

Example:

```text
Central Hospital
├── Public areas: 362
├── Patient rooms: 418
├── Clinical areas: 271
├── Staff areas: 183
└── External grounds: 50
```

Entering the building may expose floors:

```text
Floor 4: 146 agents
Floor 3: 219 agents
Floor 2: 184 agents
Floor 1: 301 agents
Ground: 274 agents
Basement: 160 agents
```

Selecting a floor exposes zones or rooms:

```text
Floor 2
├── Ward A: 61
├── Ward B: 48
├── Treatment area: 29
├── Corridor: 18
├── Waiting room: 21
└── Staff room: 7
```

Only when the chosen place is sufficiently small should individual indicators appear.

This creates a consistent navigation hierarchy:

```text
Map region
    ↓
District cluster
    ↓
Street cluster
    ↓
Building occupancy
    ↓
Floor occupancy
    ↓
Room or zone cluster
    ↓
Individual agent
```

---

## 10. Screen-Space Clustering

Clusters should generally be computed according to screen-space overlap at the current viewport and zoom level, not only from one fixed geographic radius.

For example:

- at country scale, agents kilometres apart may need to share a cluster;
- at city scale, agents on different blocks may separate;
- at street scale, agents 20 metres apart should normally appear individually;
- inside a room, agents one metre apart may still require overlap handling.

Clustering may depend on:

- zoom level;
- viewport dimensions;
- marker dimensions;
- device pixel density;
- current map pitch and bearing;
- exterior or interior mode;
- active filters;
- visualization layer;
- selected-agent exceptions.

The simulation coordinates remain unchanged throughout this process.

---

## 11. Cluster Stability and Continuity

Clusters should not jump, flicker, or reorganize unpredictably during small map movements.

The clustering system should provide:

- stable cluster identifiers where possible;
- deterministic membership for the same viewport state;
- controlled thresholds for splitting and merging;
- limited hysteresis to prevent rapid toggling;
- smooth transitions when zooming;
- preserved selection when a cluster changes form.

When zooming in, the parent cluster should visibly divide into child clusters:

```text
       248
        ↓
    83  94  71
```

When zooming out, individuals and child clusters should converge into the parent cluster.

These transitions help users understand continuity and prevent agents from appearing to blink in and out of existence.

Reduced-motion settings must disable or simplify these transitions.

---

## 12. Selected and Important Agents

A selected agent should remain discoverable even when contained inside a cluster.

Possible representation:

```text
Cluster: 247 agents
Selected: Agent A-10482
```

The selected agent may be drawn above the cluster, beside it, or through a linked callout while remaining associated with the cluster's actual geography.

Exceptions may also apply to:

- scenario-critical agents;
- agents with active alerts;
- agents currently compared by the user;
- user-controlled agents;
- agents followed across time;
- agents involved in a selected causal chain.

These exceptions must be limited. Rendering too many priority agents independently would recreate the original clutter problem.

---

## 13. Agent Selection Within a Radial Expansion

Each expanded agent indicator should display only enough information to distinguish and select the agent.

Possible elements:

- avatar or initials;
- agent state icon;
- selection ring;
- alert indicator;
- role or group marker where relevant.

Hover, keyboard focus, or touch selection may reveal:

```text
Agent A-10482
Current activity: waiting
Location: Café Orion entrance
Group: Household H-282
Information state: aware of Incident-41
```

Selecting the agent opens the Agent Inspector.

The interface should also provide a list view:

```text
Agents at Café Orion entrance

1. A-10482 — waiting
2. A-19321 — speaking
3. A-22019 — ordering
4. A-38210 — leaving
```

This list is essential for accessibility, keyboard navigation, touch devices, and larger co-location groups.

---

## 14. Density, Heatmap, and Flow Alternatives

Count markers are not always the most informative representation.

The map should support switching between:

- count clusters;
- density heatmaps;
- hexagonal or grid aggregation;
- movement flows;
- origin-destination arcs;
- building occupancy;
- route congestion;
- information diffusion;
- social or organizational overlays.

Use count clusters when users need discrete quantities and progressive drill-down.

Use density or grid aggregation when the distribution pattern matters more than selecting individual agents.

Use flows when direction and movement volume matter.

Use building occupancy when agents are concentrated in places rather than open space.

The user should be able to choose the representation appropriate to the analytical question.

---

## 15. Interior and Exterior Representation

Exterior and interior worlds should share the same conceptual interaction model but may use different rendering techniques.

### Exterior map

- geographic clustering;
- building occupancy indicators;
- street-level individual markers;
- routes and vehicles;
- geographic zoom-to-bounds.

### Interior view

- floor and room clustering;
- occupancy by zone;
- object interaction points;
- path and doorway constraints;
- local radial expansion;
- detailed agent avatars where useful.

The transition from exterior building marker to interior view should preserve context:

```text
Selected building on map
    ↓
Building overview
    ↓
Selected floor
    ↓
Selected room
    ↓
Selected agent
```

Breadcrumbs should make this hierarchy visible and reversible.

---

## 16. Data and Architecture Requirements

The visual cluster must not become a simulation entity unless the domain explicitly requires an aggregate population object.

A display cluster should be treated as a projection with fields such as:

```text
cluster_id
cluster_type
viewport_id
zoom_level
member_count
member_agent_ids or query reference
screen_position
geographic_bounds
representative_location
place_id, if co-located
selected_member_ids
aggregate_summary
projection_timestamp
```

The authoritative agent record remains separate:

```text
agent_id
world_id
simulation_time
position
place_id
building_id
floor_id
room_id
movement_state
simulation_fidelity
```

### 16.1 Recommended frontend flow

```text
Authoritative agent positions
        ↓
Spatial query or streamed viewport subset
        ↓
Visualization projection
        ↓
Screen-space cluster engine
        ↓
Map markers, heatmap, flows, or occupancy UI
```

### 16.2 Cluster queries

The client or map service may request:

```text
viewport bounds
zoom level
active time
active filters
cluster mode
minimum marker spacing
selected agent IDs
interior or exterior context
```

The result should return either:

- aggregate cluster records;
- individual agent projections;
- place occupancy projections;
- analytical group projections.

### 16.3 Server versus client clustering

Use server-side clustering when:

- the population is very large;
- the viewport query spans large regions;
- access control affects visible agents;
- filtering depends on server-side world state;
- consistent results are required across clients.

Use client-side clustering when:

- the server already returned a manageable viewport subset;
- rapid local interaction is important;
- temporary visual filters should not trigger server recomputation;
- interior views contain a small number of agents.

A hybrid approach is usually best.

---

## 17. Time and Replay Behaviour

Cluster membership is time-dependent.

When the timeline moves or a replay runs, the map must show clusters based on agent positions at the selected simulation time.

The interface should support:

- live time;
- paused inspection;
- historical replay;
- branch comparison;
- before-and-after intervention views;
- animated movement with controlled sampling.

A cluster count should always be associated with a clear simulation timestamp.

When comparing two scenario branches, avoid blending their agents into one unexplained count. Use distinct layers, split views, difference maps, or explicitly labelled comparison clusters.

---

## 18. Accessibility Requirements

Map clustering must not be the only way to access agents.

Provide:

- keyboard-navigable cluster and agent lists;
- textual count and location labels;
- focus states;
- screen-reader descriptions;
- alternative table or list views;
- sufficient contrast;
- non-colour distinctions for cluster type;
- reduced-motion behaviour;
- touch-friendly targets;
- scalable marker and text sizes.

An accessible cluster label might be:

```text
Geographic cluster, 248 agents within central Manchester. Activate to zoom to members.
```

A co-location cluster label might be:

```text
Co-location cluster, 18 agents at Café Orion. Activate to inspect occupants.
```

---

## 19. Performance Requirements

The map must not create one DOM element for every agent at large scale.

Recommended techniques include:

- GPU or canvas-based rendering;
- vector-tile or binary viewport payloads;
- spatial indexing;
- server-side aggregation;
- incremental updates;
- level-of-detail filtering;
- view-frustum or viewport culling;
- Web Workers for client clustering;
- stable object reuse;
- throttled clustering during map movement;
- exact recomputation after interaction settles.

The map should remain responsive while:

- panning;
- zooming;
- filtering;
- receiving live firehose updates;
- replaying history;
- following a selected agent.

The interface may reduce update frequency for distant aggregate clusters while maintaining higher-frequency updates for selected or nearby agents.

---

## 20. Anti-Patterns

Do not:

- render every agent as a marker at every zoom level;
- place a geographic cluster's members around an artificial centre;
- imply that radial expansion changes physical position;
- use one cluster style for physical, co-located, and analytical groups;
- lose a selected agent when zooming out;
- make cluster membership flicker during minor map movements;
- use random marker movement to make the world appear active;
- treat a building centroid as the true position of all occupants;
- display a sampled count as exact without labelling it;
- depend solely on colour to distinguish states;
- make large co-located groups use an unreadable radial menu;
- let visualization aggregation alter authoritative world state;
- confuse simulation fidelity with display fidelity.

---

## 21. Acceptance Criteria

### Clustering

- At distant zoom levels, large populations are represented without thousands of overlapping markers.
- Geographic clusters divide progressively as the user zooms in.
- Cluster counts accurately match the current filter and simulation time.
- Small viewport changes do not cause excessive cluster flicker.

### Co-location

- Agents sharing a place can be inspected without implying that they moved.
- Small groups can use anchored radial expansion.
- Large groups open a building, place, room, vehicle, or occupant browser.
- The original location remains visible and authoritative.

### Selection

- A selected agent remains discoverable across zoom levels.
- Selecting an agent from a cluster opens the correct Agent Inspector.
- Cluster expansion and collapse preserve user context.

### Building navigation

- Building occupancy can be explored hierarchically by floor, zone, and room.
- The interface does not place all building occupants at one undifferentiated marker once the user enters the building.

### Accessibility

- Every cluster and agent can be accessed through a list or keyboard path.
- Cluster type and action are communicated without relying only on colour.
- Reduced-motion settings are respected.

### Integrity

- Clustering does not modify simulation state.
- Display positions used in radial expansion are never written back as agent locations.
- The UI clearly distinguishes agents within an area from agents at one place.

---

## 22. Recommended Specification Language

The product specification should include the following rule:

> Agent indicators use semantic zoom and screen-space clustering. At distant zoom levels, nearby agents are represented by count-based cluster markers. As users zoom in, clusters progressively divide into smaller clusters and ultimately into individual agent indicators at their authoritative positions. When multiple agents remain visually overlapped because they occupy the same or nearly identical location, selecting the marker may open an anchored radial expansion in which individual agents appear around the original point and remain connected to it. This expansion is a selection aid and must never imply that the agents have physically moved. Large co-located populations should instead open a structured place, building, floor, room, vehicle, or occupant browser.

---

## 23. Final Design Principle

The correct design is not simply "show all agents" or "hide all agents."

It is:

```text
Far away:
aggregate agents and show population patterns.

Closer:
split clusters and reveal meaningful places and groups.

At street level:
show individuals at their real positions where readable.

At shared locations:
use radial selection or structured occupancy navigation.

When selected:
preserve the agent across every level of zoom and context.
```

This creates a scalable map experience that supports planetary overview, city analysis, building exploration, and individual agent inspection without sacrificing geographic truth or overwhelming the user with thousands of markers.

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
