---
title: UI/UX Research and Proven Interaction Patterns
document_id: AWG-UX-008
status: draft
version: 0.2.0
last_updated: '2026-08-20'
normative: false
owners:
- AWG design research
audience:
- design
- research
- engineering
depends_on: []
linear_issue: null
supersedes: []
---

# UI/UX Research and Proven Interaction Patterns

## 16. UI/UX research foundation

### Treat the product as a visual analytics environment

This is not primarily a chat application, a game HUD or a conventional business dashboard. It is a **visual analytics and simulation-control environment** combining:

- Geographic data.
- Temporal data.
- Networks and graphs.
- Event streams.
- Agent state.
- Scenario configuration.
- Uncertainty.
- Provenance.
- System operations.

The interface must help users move from overview to explanation without losing spatial, temporal or causal context.

### Apply the Visual Information-Seeking Mantra

Ben Shneiderman’s established pattern is directly applicable:

> **Overview first, zoom and filter, then details on demand.**

The original taxonomy also includes relating items, preserving history and extracting subsets. That maps closely to this product:

```text
Overview
    World, region, population and event state

Zoom
    Region → city → street → building → room → agent

Filter
    Time, entity type, event type, scenario, confidence and source

Details on demand
    Entity inspector, event record, claim provenance and route

Relate
    Who knew whom, which event caused what, and what occupied the same place

History
    Replay, undo, branches, saved views and investigation history

Extract
    Export a cohort, event chain, route, region or scenario result
```

Source: [The Eyes Have It: A Task by Data Type Taxonomy for Information Visualizations](https://www.cs.umd.edu/~ben/papers/Shneiderman1996eyes.pdf)

### Use Munzner’s nested model for design and validation

Visualization decisions should be evaluated at four separate levels:

1. **Domain problem:** What real task is the analyst, world builder or operator trying to complete?
2. **Data and task abstraction:** Which entities, attributes, relationships and actions represent that task?
3. **Visual encoding and interaction:** Which map, timeline, graph, table or control best supports it?
4. **Algorithm:** Can the interface calculate and render the result correctly and efficiently?

An attractive visualisation cannot repair the wrong task abstraction. A fast renderer cannot repair misleading encodings.

Source: [A Nested Model for Visualization Design and Validation](https://www.cs.ubc.ca/labs/imager/tr/2009/NestedModel/)

### Use coordinated multiple views

Map, timeline, event table, charts and graph views should be linked through one selection model.

For example:

```text
Brush time range on timeline
        ↓
Map shows only matching movement and events
        ↓
Event table filters to the same interval
        ↓
Selecting a claim highlights its social path
        ↓
Agent inspector shows belief state at that exact time
```

Brushing and linking is an established visual-analysis interaction for exploring relationships across views.

Source: [Vega brushing and linking example](https://vega.github.io/vega/examples/brushing-scatter-plots/)

### Use progressive disclosure, not feature removal

The platform will be inherently complex. The solution is not to hide all power or place every control on one screen.

Use three interface levels:

```text
Standard
    Common world exploration, agent inspection and scenario playback

Advanced
    Layer configuration, uncertainty, branches, parameter controls and provenance

Developer / Research
    Raw events, schemas, model calls, seeds, plugin state and invariants
```

Critical risk, uncertainty and assumptions must never be hidden merely to make the interface look simple.

### Preserve the user’s mental map

When users zoom, open a building, select an agent or switch to a graph, preserve orientation through:

- Stable selection.
- Breadcrumbs.
- Visible parent context.
- Consistent spatial anchors.
- Smooth but restrained transitions.
- Back and forward navigation.
- Saved investigation history.

The user should always be able to answer:

- Where am I?
- At what simulation time?
- In which scenario and branch?
- What filters are active?
- Am I seeing ground truth, an agent’s belief or an aggregate projection?

---

## 17. Product information architecture

### Primary user roles

The interface should be role-aware without creating separate incompatible products.

| Role | Primary tasks |
|---|---|
| World builder | Import or generate geography, define entities, configure systems and validate world structure |
| Scenario author | Establish conditions, interventions, variables, seeds, metrics and experiment branches |
| Analyst | Explore patterns, compare outcomes, inspect cohorts and explain anomalies |
| Investigator | Trace claims, actions, provenance, causality and bad-actor behaviour |
| Simulation operator | Start, pause, monitor, recover and manage long-running simulations |
| Researcher | Calibrate, validate, run ensembles and examine sensitivity |
| Developer | Inspect events, plugins, model calls, schemas, performance and invariants |

### Recommended workspaces

1. **World Explorer** — map, local world, layers, entities and live state.
2. **Scenario Studio** — scenario creation, assumptions, interventions and run configuration.
3. **Agent and Group Inspector** — lives, plans, state, relationships, knowledge and history.
4. **Information Space** — messages, claims, feeds, diffusion, trust and moderation.
5. **Timeline and Replay** — playback, branching, comparison and causal navigation.
6. **Event Firehose** — structured event investigation and export.
7. **Validation Lab** — calibration, metrics, ensembles, sensitivity and observed-data comparison.
8. **System Console** — plugins, adapters, model providers, queues, health and storage.

### Recommended desktop layout

This should be a desktop-first analysis environment. Mobile can support monitoring and lightweight inspection, but complex world authoring should not be forced into a phone-first layout.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ World / Scenario / Branch / Time       Search      Run state      Commands │
├──────────────┬───────────────────────────────────────┬──────────────────────┤
│ Workspace    │                                       │ Inspector            │
│ navigation   │              Main canvas              │                      │
│              │       Map / world / graph / chart     │ Entity / event /     │
│ Layers       │                                       │ claim / route /      │
│ Filters      │                                       │ configuration        │
│ Saved views  │                                       │                      │
├──────────────┴───────────────────────────────────────┴──────────────────────┤
│ Timeline / playback / event density / branch markers / annotations         │
└─────────────────────────────────────────────────────────────────────────────┘
```

Panels should be:

- Resizable.
- Dockable where practical.
- Collapsible.
- Restorable to a known layout.
- Saved by workspace.
- Keyboard reachable.

Map camera padding must respond to panel dimensions so opening the inspector does not hide the selected entity. MapLibre exposes viewport edge insets specifically to shift the apparent map centre around floating or resized UI.

Source: [MapLibre EdgeInsets](https://maplibre.org/maplibre-gl-js/docs/API/classes/EdgeInsets/)

### Global context strip

A persistent context strip should always show:

```text
World: London Baseline
Scenario: Transport Disruption
Branch: Intervention B
Simulation time: 2026-09-02 08:42:12
Playback: Paused
Truth mode: Analyst ground truth
Seed: 1042
Active filters: 4
```

This prevents screenshots, exports and decisions from losing essential context.

---

## 18. World Explorer and multiscale map UX

### Use semantic zoom

Zoom should change **meaning**, not simply make the same symbols larger.

An illustrative default policy is:

| View band | Display policy |
|---|---|
| Globe or planet | Regions, macro flows, major events and aggregate indicators |
| Continental or country | H3/grid aggregates, administrative comparisons and transport corridors |
| Regional or city | Density, clusters, origin-destination flows, buildings and selected individuals |
| Neighbourhood or street | Individual agents, vehicles, routes, entrances, queues and local events |
| Site or building | Access points, occupancy, floors, indoor links and selected activities |
| Room or immediate local area | Embodied agents, objects, affordances, perception and exact movement |

MapLibre’s own performance guidance recommends clustering large point sets, controlling zoom ranges and simplifying styles. deck.gl provides heatmap, grid, hexagon and cluster layers for aggregated views. H3 supplies a hierarchical spatial index that can move between parent and child resolutions efficiently, but its hierarchy has exact logical containment and approximate geometric containment, so exact boundary decisions still require proper geometry tests.

Sources:

- [MapLibre guidance for large datasets](https://maplibre.org/maplibre-gl-js/docs/guides/large-data/)
- [deck.gl layer catalogue](https://deck.gl/docs/api-reference/layers)
- [deck.gl aggregation layers](https://deck.gl/docs/api-reference/aggregation-layers/overview)
- [H3 hierarchical indexing](https://h3geo.org/docs/highlights/indexing/)

### Recommended rendering split

```text
MapLibre GL JS
    Basemap, vector tiles, labels, roads, buildings, terrain and map camera

PMTiles / Protomaps
    Offline tile packaging and delivery

deck.gl
    Large agent layers, paths, trips, flows, grids, H3 cells and analytical overlays

DOM / accessible UI
    Controls, inspector, legends, textual summaries and keyboard alternatives
```

Do not render thousands of agents as individual DOM markers. Use GPU layers or tile-based projections.

### Layer manager

Every visual layer should declare:

- Name and purpose.
- Data source.
- Time coverage.
- Spatial resolution.
- Aggregation method.
- Whether it represents truth, belief, observation or estimate.
- Whether locations are exact, sampled or coarsened.
- Legend.
- Visible zoom range.
- Performance cost.
- Export rules.

Users should be able to reorder, hide, pin and save layer presets. However, the interface should limit simultaneous high-salience overlays so the map does not become an unreadable collection of colours and symbols.

### Default map presets

```text
Population
Mobility
Incidents
Information diffusion
Organizations and influence
Infrastructure
Resources and economy
Scenario interventions
Validation comparison
Debug geometry
```

A preset changes several coordinated layers and legends, not the underlying simulation.

### Selection patterns

Support more than clicking tiny points:

- Click to inspect.
- Hover for lightweight preview where pointer input exists.
- Lasso or box selection.
- Radius selection.
- Route corridor selection.
- Select all occupants of a building.
- Select all agents exposed to a claim.
- Select a cohort from a chart and highlight it on the map.
- Search by agent, organization, place, event or OSM identifier.

Every map selection should have a table or list equivalent.

### Selected-agent focus

Selecting an agent should create a persistent focus state rather than a temporary popup.

```text
Agent A-10482
Current location: Bus 22, segment 18
Destination: Workplace
Journey progress: 63%
Current action: Travelling
Next decision point: Stop 14
Known disruption: Neighbour report, medium confidence
Simulation fidelity: S3 Cognitive individual
Display fidelity: V3 Individual marker
```

The user can:

- Follow.
- Pin without following.
- Compare with another agent.
- Open agent perspective.
- Open history.
- Trace why the current plan was selected.

### Ground-truth and perspective modes

The product must visibly distinguish:

```text
Analyst truth mode
    Shows authoritative simulation state

Agent perspective mode
    Shows only what the selected agent can perceive, remember or infer

Public information mode
    Shows information available through public channels

Scenario author mode
    Shows interventions and hidden experimental configuration
```

When ground truth is visible, use a persistent mode label or watermark. Otherwise users may accidentally interpret privileged simulator state as something agents knew.

---

## 19. Building and interior world UX

### Use the map for orientation and the local world for embodiment

The recommended default is:

- 2D map for regional and operational work.
- Optional 3D city view for height, terrain and local context.
- Detailed local scene for selected sites and streets.
- Floor-based indoor view for buildings.

A global 3D globe should be a context view, not the primary analytical surface. Three-dimensional views introduce occlusion, orientation and performance problems. They are justified when vertical relationships, line of sight, floors, terrain or embodied movement matter.

### Indoor model

A building should expose:

```text
Building
├── Site boundary
├── Entrances and exits
├── Floors and levels
├── Rooms and zones
├── Corridors
├── Doors and access restrictions
├── Stairs, lifts and ramps
├── Indoor navigation graph
├── Objects and affordances
├── Occupancy and capacity
├── Utilities and hazards
└── Current events
```

OGC IndoorGML is specifically designed around indoor spaces, topology and navigation relationships. It is a useful conceptual model even if the runtime uses a different encoding.

Source: [OGC IndoorGML](https://www.ogc.org/standards/indoorgml/)

### Building interaction pattern

```text
Select building on map
        ↓
Inspector shows occupancy, access and active events
        ↓
Open building
        ↓
Choose floor or follow selected agent automatically
        ↓
Display rooms, routes, doors and occupants
        ↓
Inspect object, activity or conversation
```

The transition should preserve the selected building and simulation time. Users must be able to return to the city view without losing their investigation.

### Floor and room controls

Provide:

- Floor stack with occupancy and alert counts.
- “Follow selected agent” floor switching.
- Ghosted adjacent-floor context where useful.
- Indoor route preview.
- Accessibility route option.
- Entrance and exit state.
- Capacity and reservation overlays.
- Hazard and visibility overlays.
- Textual room list as an accessible alternative.

### Exact versus aggregate indoor position

At lower fidelity, the system may know that an agent is “inside Building X” or “on Floor 2” without an exact room coordinate. The UI must not fabricate a precise dot.

Use explicit position quality:

```text
Exact
Route-interpolated
Room-level
Floor-level
Building-level
Area estimate
Unknown
```

---

## 20. Agent, group and organization inspector

### Inspector structure

The inspector should use stable tabs or sections:

```text
Overview
Current state
Location and movement
Schedule and plans
Needs and resources
Knowledge and beliefs
Memory
Relationships and trust
Groups and organizations
Communications
Actions and decisions
Timeline
Provenance and debug
```

The overview should remain compact. Advanced and developer details can be progressively disclosed.

### Structured “Why?” explanations

Do not expose or fabricate hidden chain-of-thought. Provide a structured causal explanation derived from recorded state and events.

Example:

```text
Why did A leave work early?

Observed:
- Message M-883 from school at 14:02
- Child pickup was required before 15:00

Believed:
- Normal route would be delayed by road closure
- Confidence: 0.81

Goal selected:
- Reach school before 15:00

Plan:
- Leave work → walk to station → take train → walk to school

Constraints:
- Car unavailable
- Bus route affected

Result:
- Departed at 14:08
```

Every row should link to the supporting event, claim, route or state record.

### Truth-versus-belief comparison

For analysts, provide a comparison view:

| Topic | World truth | Agent belief | Evidence available to agent |
|---|---|---|---|
| Bridge status | Closed | Probably closed | Neighbour message and delayed bus |
| Cause | Structural damage | Possible accident | No direct evidence |
| Reopening time | Unknown | Believes 17:00 | Unverified social post |

This makes epistemic differences understandable without merging them.

### Group and organization inspection

Groups should have their own state, not just a member list:

- Purpose.
- Membership and roles.
- Leadership.
- Rules and decision process.
- Resources and assets.
- Territory and locations.
- Internal communication channels.
- External relationships.
- Current objectives.
- Decisions and history.

Selecting an organization should highlight relevant sites, members, supply relationships and information channels across linked views.

---

## 21. Information-space and virtual social-media UX

### Separate participant experience from analyst experience

The virtual platform should support two distinct interfaces:

#### Participant platform view

What an in-world user or bot experiences:

- Feed.
- Search.
- Posts.
- Replies.
- Likes.
- Reposts.
- Messages.
- Groups.
- Moderation actions.

#### Analyst information-space view

What a researcher or investigator needs:

- Exposure graph.
- Claim lineage.
- Source provenance.
- Belief change.
- Trust context.
- Recommendation causes.
- Coordination patterns.
- Bot or bad-actor indicators.
- Ground-truth comparison.

Do not put privileged analytical overlays into the participant feed unless the scenario explicitly models such tools.

### Distinguish actions and interpretations

The interface must not equate:

```text
Viewed
Understood
Believed
Endorsed
Liked
Reposted
Commented
Acted upon
```

A repost may represent endorsement, criticism, mockery, warning, archiving or coordinated amplification. Store observable actions separately from inferred motives.

### Claim provenance view

A selected claim should show:

```text
World event E-142
    ↓ directly observed by A
Claim C-1 created by A
    ↓ told face-to-face to B
Claim C-2 paraphrased by B
    ↓ sent to C
Post P-9 created by C
    ├── viewed by D
    ├── reposted by E
    └── challenged by F
            ↓
        F messages A for verification
```

The user should be able to switch between:

- Timeline.
- Sankey/flow view.
- Ego network.
- Geographic diffusion.
- Claim version comparison.
- Tabular provenance.

Avoid displaying the entire social network as one node-link “hairball.” Default to a selected claim, actor, community or time window.

### Recommendation transparency

For a simulated platform, the analyst should be able to inspect why a post was eligible for a feed:

```text
Follow relationship
Community membership
Recency
Topic affinity
Engagement score
Paid or promoted status
Moderation state
Experiment treatment
```

The participant-facing platform does not necessarily expose all of this, but the simulation firehose should.

---

## 22. Scenario Studio UX

### Scenario creation workflow

A scenario should be assembled through a validated sequence:

```text
1. Choose or create world
2. Define geographic and temporal scope
3. Select population and fidelity policy
4. Configure systems and adapters
5. Define baseline conditions
6. Add interventions and triggers
7. Define uncertainty and seeds
8. Choose metrics and stopping conditions
9. Validate assumptions and invariants
10. Run baseline, branches or ensemble
```

### Scenario Studio layout

Use coordinated surfaces:

- Map for geographic scope and interventions.
- Timeline for scheduled events and triggers.
- Form/editor for parameters.
- Dependency panel for affected systems.
- Assumption register.
- Validation panel.
- Cost and performance estimate.
- Diff against previous version.

### Interventions should be typed

Examples:

```text
CloseRoad
ChangePrice
RemovePower
IssuePublicAlert
ChangePolicy
AddWeatherEvent
IntroduceClaim
ChangeLeadership
ModifyTransportSchedule
DisableCommunicationChannel
```

The interface should explain:

- Preconditions.
- Target scope.
- Start and end.
- Direct effects.
- Systems that may propagate consequences.
- Whether agents can know about it immediately.
- Whether it is a ground-truth event or information-only injection.

### Advanced authoring

Support three synchronized authoring modes:

1. Guided forms for common scenarios.
2. Visual timeline/map authoring.
3. Versioned JSON or YAML for advanced users.

All three must compile to the same typed scenario schema. Editing source should update the visual representation after validation, and visual edits should produce a reviewable source diff.

### Assumption register

Every scenario should display assumptions such as:

```text
Population generated from census distribution 2025-Q4
Public transport timetable source dated 2026-07-01
Weather model: synthetic baseline profile
Agent trust model: experimental v2
LLM provider: local Ollama model X
No mobile-network outage unless explicitly introduced
```

Assumptions are part of the scenario result, not hidden configuration.

### Pre-run validation

Block or warn on:

- Missing geography.
- Unreachable required locations.
- Invalid dates.
- Impossible capacities.
- Undefined plugins.
- Incompatible adapter versions.
- Missing seed policy.
- No recorded outcome metrics.
- Information injected without a channel.
- Intervention that silently reveals ground truth to agents.

---

## 23. Timeline, replay, branching and comparison UX

### Timeline is a first-class navigation surface

The timeline should show:

- Current simulation time.
- Playback state.
- Event density.
- Scenario interventions.
- Agent or group milestones.
- Claim propagation.
- Infrastructure incidents.
- Snapshots.
- Branch points.
- User annotations.

Users should be able to zoom from years to seconds while keeping the same selected entities and filters.

### Separate simulation time from rendering time

A simulation may run faster than the interface can animate. The UI should:

- Consume authoritative timestamps.
- Interpolate position only for presentation.
- Batch updates when necessary.
- Never imply that skipped visual frames were skipped simulation events.
- Clearly indicate live, buffered, paused and replay modes.

### Branching model

```text
Baseline
    ├── Branch A: Bridge remains open
    ├── Branch B: Bridge closes at 08:20
    │       └── Branch B2: Public alert at 08:24
    └── Branch C: Bus capacity increased
```

A branch comparison should show:

- Shared history before the branch point.
- Exact intervention difference.
- Divergence over time.
- Outcome metrics.
- Difference maps.
- Different affected cohorts.
- Causal paths leading to major divergence.

### Comparison patterns

Use the appropriate pattern for the task:

- Side-by-side small multiples for spatial comparison.
- Swipe or synchronized cameras for local map comparison.
- Difference layers for quantitative change.
- Aligned timelines for event sequence comparison.
- Distribution plots for ensembles.
- Cohort tables for who changed outcome.
- Causal explanation for why branches diverged.

Avoid rapidly toggling two maps as the only comparison method; it burdens memory and can conceal small differences.

### Investigation history

Shneiderman’s original taxonomy emphasizes history for undo, replay and progressive refinement. Preserve:

- Map extents.
- Filters.
- Selections.
- Queries.
- Opened entities.
- Branch changes.
- Annotations.

Users should be able to save an investigation as a shareable view without changing the world state.

---

## 24. Event firehose and causal explorer UX

### The firehose must not become an unreadable terminal

The underlying event stream can be enormous. The interface should provide:

- Live tail with pause.
- Virtualized event table.
- Time and sequence filters.
- Event-type facets.
- Actor, target, place and claim filters.
- Full-text and structured query.
- Saved queries.
- Sampling only for display, never for canonical storage.
- Aggregation by time, type, location or actor.
- Export of the exact matching event set.

### Event detail

Each event detail should include:

```text
Event identity and schema version
World, scenario and branch
Simulation time and sequence
Actor and targets
Location
Command that produced the event
Parent and causal events
Validation result
Plugin and version
Random stream reference
Model-call reference where applicable
Payload
State changes
Who could observe it
Derived projections
```

### Causal navigation

Users should be able to move both directions:

```text
Why did this happen?
    Event ← command ← selected plan ← goal ← belief ← observation ← source event

What did this cause?
    Event → observations → claims → actions → later world changes
```

### Raw and human-readable views

Provide:

- Human summary.
- Structured fields.
- Raw JSON or binary-decoded payload.
- Schema documentation.
- Related events.

The human summary is a projection. The structured record remains authoritative.

---

## 25. Design system

### Design principles

The design system should encode these principles:

1. **Evidence over spectacle.** Visual polish must not hide uncertainty or assumptions.
2. **Context is persistent.** World, scenario, branch, time and truth mode remain visible.
3. **Details on demand.** Do not expose every control at once.
4. **Truth, belief and claim are visually distinct.** Never merge their semantics.
5. **Actions are reversible where possible.** Exploration does not mutate the simulation.
6. **Writes are explicit.** Scenario or world changes require a clear command and validation result.
7. **State is never communicated by colour alone.** Use text, shape, icon or pattern as well.
8. **Dense does not mean chaotic.** Support compact expert workflows with hierarchy and alignment.
9. **Motion communicates state change, not decoration.**
10. **Every visualization has a table, summary or query alternative.**

### Token architecture

Use the Design Tokens Community Group format as the interchange format for design decisions. The 2025.10 format is the first stable community specification and supports vendor-neutral exchange across tools and platforms.

Sources:

- [Design Tokens Community Group](https://www.designtokens.org/)
- [Design Tokens Format Module 2025.10](https://www.designtokens.org/tr/2025.10/format/)

Recommended token layers:

```text
Primitive tokens
    Raw colour ramps, font families, type scales, spacing, radii and durations

Semantic UI tokens
    Surface, text, border, focus, selected, disabled, warning and danger

Domain tokens
    World truth, observation, belief, inference, claim status, intervention and uncertainty

Visualization tokens
    Map layers, density, flow, route, comparison, selection and confidence

Component tokens
    Inspector, timeline, layer panel, event grid, scenario editor and map controls
```

Example conceptual token structure:

```json
{
  "domain": {
    "truth": {
      "observed": {
        "$type": "color",
        "$value": "{color.semantic.verified}"
      }
    },
    "claim": {
      "unverified": {
        "$type": "color",
        "$value": "{color.semantic.caution}"
      },
      "disputed": {
        "$type": "color",
        "$value": "{color.semantic.conflict}"
      }
    },
    "selection": {
      "primary": {
        "$type": "color",
        "$value": "{color.semantic.accent}"
      }
    }
  }
}
```

Do not hard-code map colours separately from the application design system. Compile the same token source into:

- CSS custom properties.
- TypeScript token definitions.
- MapLibre style fragments and expressions.
- deck.gl layer themes.
- Chart themes.
- Documentation examples.

### Domain visual language

The visual system needs explicit semantic roles for:

- Authoritative world truth.
- Direct observation.
- Reported claim.
- Agent belief.
- Inference.
- Unknown state.
- Disputed state.
- Corroborated state.
- Scenario intervention.
- Simulation warning.
- Validation failure.
- Selected entity.
- Followed entity.
- Comparison branch A and B.

Each role needs:

- Colour role.
- Icon or marker shape.
- Text label.
- Pattern or line style where relevant.
- Light, dark and high-contrast treatment.

For maps, use cartographic palette practices rather than arbitrary interface colours. ColorBrewer provides sequential, diverging and qualitative schemes with options for colour-blind, print and photocopy safety.

Source: [ColorBrewer 2.0](https://colorbrewer2.org/)

### Typography

Use a highly readable interface family and a separate monospaced family for:

- Identifiers.
- Event types.
- Times.
- Coordinates.
- JSON.
- Queries.

Define at least:

- Display or workspace title.
- Section heading.
- Panel heading.
- Body.
- Dense table.
- Caption and metadata.
- Code and event payload.

Long prose should not dominate the main map workspace. Use short summaries with expandable evidence.

### Density modes

Support:

```text
Comfortable
    General use and onboarding

Compact
    Analyst and operator workflows

Presentation
    Larger text and simplified controls for shared screens
```

Density changes spacing and row height, not the amount of evidence available.

### Motion system

Define motion tokens by purpose:

- State transition.
- Spatial navigation.
- Selection confirmation.
- Live update.
- Alert.

Avoid constant pulsing and moving markers. Respect `prefers-reduced-motion`; provide dissolve, instant or static alternatives for camera fly-throughs, animated paths and uncertainty animations.

Source: [MDN: prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/%40media/prefers-reduced-motion)

### Core component inventory

```text
AppShell
WorkspaceNavigation
ContextStrip
MapCanvas
LocalWorldCanvas
LayerManager
MapLegend
SimulationControls
Timeline
BranchTree
EntityInspector
AgentSummary
BeliefTruthComparison
ClaimProvenance
CausalTrail
EventGrid
EventDetail
ScenarioForm
InterventionEditor
AssumptionRegister
ValidationPanel
FilterBuilder
SavedView
CommandPalette
SearchOmnibox
StatusBadge
SplitPane
DockPanel
EmptyState
ErrorBoundary
OfflineStatus
```

### Design-system repository structure

```text
packages/
├── design-tokens/
│   ├── source/
│   ├── themes/
│   ├── map-themes/
│   └── build/
├── ui-primitives/
├── ui-components/
├── domain-components/
├── map-components/
├── chart-themes/
├── icons/
├── accessibility/
└── storybook/
```

Every domain component should have deterministic fixture stories based on recorded simulation events so design review does not depend on a live backend.

---

## 26. Frontend and application architecture

### Architectural principle

The interface is a client of the world. It must not become the world authority.

```text
User gesture
    ↓
Typed UI intent
    ↓
Command API
    ↓
Server validation and simulation kernel
    ↓
Authoritative event
    ↓
Read-model projection
    ↓
UI update
```

The UI must never mutate authoritative world state locally and then assume success.

### API boundaries

```text
World Query API
    Entity snapshots, relationships, read models and search

World Command API
    Explicit validated mutations and simulation controls

Event Stream API
    Ordered live or replayed domain events

Tile and Geometry API
    Vector tiles, PMTiles, terrain, indoor geometry and analytical tiles

Gazetteer API
    Place, street, address and OSM object search

Scenario API
    Versioned definitions, validation, branches and runs

Analytics API
    Aggregates, distributions, metrics and comparison results

Plugin Registry API
    Manifests, compatibility, capabilities and permissions
```

### Recommended data flow

```text
Authoritative event store
        ↓
Projection services
        ├── Entity read model
        ├── Spatial tiles and H3 aggregates
        ├── Timeline buckets
        ├── Social and claim graph projections
        ├── Metrics and validation projections
        └── Search indexes
                ↓
        Query and streaming gateway
                ↓
        Client caches and Web Workers
                ↓
        Map, timeline, graph, tables and inspector
```

The map should consume spatial projections designed for the current zoom and filters, not the entire event store.

### Client-state separation

Maintain separate stores for:

#### Authoritative server state

- Entity snapshots.
- Events.
- Scenario definitions.
- Branch state.
- Simulation run state.
- Read-model results.

#### Ephemeral interaction state

- Current viewport.
- Hover.
- Open panels.
- Unsaved filter edits.
- Selection rectangle.
- Inspector tab.

#### Persisted user workspace state

- Saved views.
- Panel layout.
- Layer presets.
- Query history.
- Density preference.
- Accessibility preferences.

#### Draft mutation state

- Scenario edits.
- World edits.
- Pending command.
- Validation errors.

Draft state must never be confused with accepted world state.

### Streaming architecture

The event gateway should support:

- Ordered sequence numbers.
- Resume after disconnect.
- Gap detection.
- Backpressure.
- Batch delivery.
- Subscription filters.
- Snapshot plus delta synchronization.
- Live and replay streams through the same envelope where practical.

The UI may batch visual updates, but it must retain the highest received sequence and clearly indicate when it is behind live time.

### Rendering pipeline

```text
Binary or tiled spatial data
        ↓
Web Worker decode and filter
        ↓
Typed arrays / GPU buffers
        ↓
MapLibre and deck.gl layers
        ↓
Accessible DOM summary and controls
```

Use workers for:

- Decoding.
- Aggregation.
- Filtering.
- Route interpolation.
- Geometry simplification.
- Event bucketing.

Avoid sending every raw event through the React component tree.

### UI plugin architecture

UI extensions should use versioned manifests and stable extension points.

```ts
interface WorldUiPluginManifest {
  id: string;
  version: string;
  compatibleCore: string;
  permissions: string[];
  routes?: UiRouteContribution[];
  panels?: PanelContribution[];
  mapLayers?: MapLayerContribution[];
  inspectors?: InspectorContribution[];
  eventRenderers?: EventRendererContribution[];
  scenarioEditors?: ScenarioEditorContribution[];
  commands?: CommandContribution[];
}
```

Rules:

- Plugins cannot write directly to the core store.
- World mutations go through typed commands.
- Plugins declare event schemas and permissions.
- UI contributions have lifecycle and disposal hooks.
- Compatibility is checked before loading.
- Untrusted plugins run in a restricted boundary where possible.
- One plugin failure cannot collapse the main world explorer.

### Suggested web stack

This is a candidate architecture, not a mandatory dependency list:

| Concern | Candidate |
|---|---|
| Application shell | React + TypeScript |
| Basemap and vector tiles | MapLibre GL JS |
| Offline tile archive | PMTiles / Protomaps |
| Large geospatial overlays | deck.gl |
| Spatial aggregation | Server projections plus H3 where suitable |
| Charts and linked views | Vega / Vega-Lite or another declarative chart layer |
| Accessible primitives | React Aria, Radix-style primitives or equivalent reviewed components |
| Event and data tables | Virtualized table/grid |
| Local processing | Web Workers and transferable typed arrays |
| Offline client storage | IndexedDB or Origin Private File System where supported |
| Component documentation | Storybook or equivalent |
| Token compilation | DTCG-compatible token pipeline |

The adapter architecture should allow the map, chart and component implementations to change without changing domain contracts.

### Offline architecture

Offline mode should package or locally serve:

- PMTiles.
- World and scenario metadata.
- Gazetteer.
- Routing data.
- Building and indoor geometry.
- Local model endpoints.
- Event and snapshot storage.
- Design-system assets.

The interface should display:

```text
Offline: fully available
Offline: map available, model unavailable
Offline: read-only replay
Online provider active
```

Never silently fall back from a local provider to a remote provider.

### AI assistant in the UI

A natural-language assistant can help users:

- Build a filter.
- Find an entity.
- Draft a scenario.
- Explain a selected event.
- Suggest a comparison.
- Translate a question into a query.

It must:

- Show the structured query or command it generated.
- Cite event and entity sources.
- Distinguish evidence from inference.
- Require explicit confirmation before mutation.
- Never directly alter scenario or world state.
- Remain optional; core tasks must be available through normal controls.

---

## 27. Performance architecture for the interface

### Use aggregation before sampling

For density and counts, aggregation generally preserves meaning better than arbitrary sampling. If sampling is used, the interface must state the method and sample size.

Recommended strategies:

- Server-generated vector tiles.
- H3 or grid aggregates.
- Zoom-dependent clustering.
- GPU aggregation.
- Time bucketing.
- Spatial and temporal query windows.
- Cohort summaries.
- Progressive loading.

### Avoid common rendering failures

Never:

- Render every agent as a DOM element.
- Send the whole world graph to the browser.
- Recalculate all aggregates on every pan.
- Let every event trigger a full application render.
- Keep invisible 3D building interiors loaded globally.
- Load full agent memories into list views.
- Animate at simulation-event frequency.

### Local fidelity activation

When a user enters a building or follows an agent, the UI can request a higher-detail projection for the local area.

```text
City projection
    ↓ select building
Building projection requested
    ↓ open floor
Indoor geometry and occupant state requested
    ↓ follow agent
Fine movement stream requested
```

Leaving the area should release high-detail resources after a controlled cache period.

### Degradation policy

When device or stream capacity is limited, degrade in a defined order:

1. Reduce decorative motion.
2. Reduce update frequency while preserving timestamps.
3. Reduce geometry detail.
4. Replace individual points with clusters.
5. Replace clusters with aggregate cells.
6. Disable optional 3D.

Do not silently drop authoritative event categories.

### Performance instrumentation

Measure separately:

- Initial shell load.
- Time to first usable map.
- Pan and zoom frame rate.
- Selection response.
- Inspector load.
- Stream lag.
- Event-table filtering.
- Building transition.
- Memory and GPU use.
- Offline startup.

Performance telemetry belongs to the software-observability plane, not the simulation firehose.

---

## 28. Accessibility and inclusive design

### Standard

Target WCAG 2.2 AA for the web application, with selected AAA practices where feasible. WCAG 2.2 includes requirements concerning focus visibility, focus not being obscured, dragging alternatives and minimum target size.

Sources:

- [WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- [What is new in WCAG 2.2](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/)

### The map cannot be the only interface

Provide equivalent access through:

- Search.
- Entity lists.
- Event tables.
- Place hierarchy.
- Route steps.
- Textual visible-area summaries.
- Keyboard selection.
- Saved queries.

A screen-reader user should be able to ask:

```text
Which incidents are visible in the current region?
Which selected agents are moving?
What building is selected?
What changed in this time range?
```

without interpreting a canvas.

### Keyboard interaction

MapLibre supports keyboard pan, zoom, rotation and pitch controls, but the application must also provide keyboard access to layers, visible entities and selections.

Source: [MapLibre KeyboardHandler](https://maplibre.org/maplibre-gl-js/docs/API/classes/KeyboardHandler/)

Use established WAI-ARIA patterns for grids, treegrids, tabs, dialogs and menus. Dense event tables and hierarchical entity lists require predictable arrow-key and focus behaviour.

Source: [WAI-ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/)

### Focus and target size

- Focus indicators must remain visible above maps and overlays.
- Docked panels must not cover the focused element.
- Controls should meet or exceed the WCAG minimum target-size rules or provide sufficient spacing.
- Drag-only operations need click, keyboard or form alternatives.

Sources:

- [Understanding Focus Appearance](https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance.html)
- [Understanding Target Size Minimum](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html)

### Colour and graphics

Meaningful map features and UI components need sufficient non-text contrast. Never encode claim state, scenario branch or alert severity by colour alone.

Source: [Understanding Non-text Contrast](https://www.w3.org/WAI/WCAG21/understanding/non-text-contrast.html)

### Motion and time

Provide:

- Reduced-motion mode.
- Pause for non-essential animation.
- Manual playback speed.
- Step-by-step replay.
- Static uncertainty alternatives.
- No flashing event markers.
- Ability to stop automatic camera following.

### Cognitive accessibility

- Keep world, branch and time visible.
- Use plain domain language alongside technical IDs.
- Preserve filters and explain why data disappeared.
- Make destructive or mutating actions explicit.
- Provide undo for workspace changes.
- Use consistent component placement.
- Avoid unexplained adaptive UI rearrangement.

---

## 29. UI/UX anti-patterns to avoid

1. **The wall of dots** — every person rendered individually at every scale.
2. **The impressive globe trap** — a cinematic 3D globe used where a 2D analytical map is clearer.
3. **Chat as the whole product** — forcing every task through a conversation instead of direct manipulation and structured controls.
4. **God mode without a warning** — showing simulator truth while implying it is participant knowledge.
5. **Map popups as inspectors** — placing complex agent state in transient tiny popups.
6. **One universal dashboard** — combining world building, live operation, validation and investigation into one overloaded screen.
7. **Colour-only truth states** — no textual or symbolic distinction between observed, believed and disputed.
8. **A single randomness slider** — concealing many distinct stochastic mechanisms.
9. **Animation as evidence** — assuming moving visuals prove simulation fidelity.
10. **Silent sampling** — dropping or sampling agents without labelling the projection.
11. **3D interiors with fabricated precision** — drawing an exact room position when only building-level location is known.
12. **Network hairballs** — rendering every social edge without a task-specific filter.
13. **Live/replay ambiguity** — users cannot tell whether they are watching current state or historical playback.
14. **Hidden filters** — screenshots and exports omit active filters or branch context.
15. **AI writes without review** — an assistant silently alters the world or scenario.
16. **Raw firehose only** — an infinite log without facets, lineage or causal navigation.
17. **UI state treated as world state** — optimistic local mutation becomes authoritative.
18. **Map tiles treated as exact topology** — presentation data used as simulation truth.
19. **Decorative agent emotion** — avatar animation presented as validated internal state.
20. **Uncertainty washed away** — displaying one run or one point estimate as the answer.

---

## 30. UI/UX validation and acceptance tests

### Research process

Use Munzner’s levels to structure evaluation:

| Level | Validation question | Method |
|---|---|---|
| Domain problem | Does the workspace support real analyst, builder and operator tasks? | Interviews, observation and task analysis |
| Data/task abstraction | Are truth, belief, claim, event, time and branch represented correctly? | Domain expert review and scenario walkthroughs |
| Encoding/interaction | Can users perceive, select, compare and explain correctly? | Usability tests and controlled visualization studies |
| Algorithm/performance | Does it render and query correctly at required scale? | Benchmarks, profiling and correctness tests |

### Critical usability tasks

Test whether representative users can:

1. Locate an agent and determine their current physical state.
2. Follow the agent into and through a building.
3. Explain why the agent performed an action using evidence.
4. Distinguish world truth from the agent’s belief.
5. Trace a claim from witness to repost and later action.
6. Build a road-closure scenario without creating impossible travel.
7. Replay the scenario and create a counterfactual branch.
8. Compare outcomes across seeds and understand uncertainty.
9. Find all events affecting a selected building and time range.
10. Determine whether a displayed density layer is exact, aggregated or sampled.
11. Use the main workflows without a mouse.
12. Recover from a disconnected event stream without losing investigation context.

### Acceptance criteria

#### Context integrity

- World, scenario, branch and time are visible in every analytical workspace.
- Exports include context and active filters.
- Ground-truth mode is persistently labelled.

#### Map integrity

- Zooming changes representation according to the semantic-zoom policy.
- Individual markers do not appear where only aggregate positions are known.
- Selection remains stable during zoom and view-mode changes.
- Map and table selections stay synchronized.

#### Causal integrity

- Every “why” explanation links to recorded evidence.
- The interface distinguishes recorded fact from generated summary.
- Claim lineage can be traversed without reading raw logs.

#### Randomness integrity

- The active seed policy is visible.
- A run can be reproduced with the same seed and versions.
- Ensemble results are not presented as one deterministic forecast.

#### Accessibility integrity

- Core workflows are keyboard operable.
- Map information has list or table alternatives.
- Focus remains visible and unobscured.
- Reduced-motion mode removes non-essential camera and data animation.
- State is not encoded by colour alone.

#### Performance integrity

- Large populations aggregate rather than freezing the interface.
- Stream lag is visible.
- Reconnection detects missing sequence ranges.
- High-detail building data loads only when needed.

#### Plugin integrity

- UI plugins cannot mutate authoritative state directly.
- Incompatible plugins are blocked with an explanation.
- Plugin failure is isolated from the core workspace.

---

## 31. Recommended UI implementation sequence

### UI Phase 0 — Design and data contracts

Define:

- User roles and critical tasks.
- Truth/belief/claim visual semantics.
- Command and query contracts.
- Selection model.
- Timeline model.
- Semantic zoom policy.
- Design tokens.
- Accessibility baseline.
- Performance test datasets.

### UI Phase 1 — Read-only World Explorer

Build:

- Application shell.
- Offline MapLibre/PMTiles basemap.
- Layer manager.
- Agent clusters and aggregate cells.
- Entity search.
- Inspector.
- Timeline playback.
- Event table.
- Saved views.

Use recorded events before connecting live simulation.

### UI Phase 2 — Agent and causal investigation

Add:

- Agent follow.
- Route history.
- Belief/truth comparison.
- Structured “why” explanations.
- Claim provenance.
- Coordinated map, timeline and table selection.

### UI Phase 3 — Building and local world

Add:

- Building selection.
- Floors and rooms.
- Indoor graph.
- Occupancy.
- Local high-fidelity movement.
- Object affordance inspection.

### UI Phase 4 — Scenario Studio

Add:

- Typed interventions.
- Map/timeline authoring.
- Assumption register.
- Validation.
- Source editor.
- Version diff.
- Run configuration.

### UI Phase 5 — Branches, ensembles and validation

Add:

- Branch tree.
- Side-by-side and difference comparison.
- Seed ensembles.
- Uncertainty visualizations.
- Observed-data comparison.
- Calibration and sensitivity views.

### UI Phase 6 — Plugin SDK and operational hardening

Add:

- UI plugin manifest.
- Map-layer extension points.
- Event renderers.
- Custom inspectors.
- Permission model.
- Performance budgets.
- Accessibility regression testing.
- Offline packaging and recovery.

---

## 32. Consolidated UI/UX recommendation

The best balance is:

```text
Far away
    Simulate at appropriate fidelity, aggregate heavily, show patterns.

Nearby
    Increase spatial and behavioural detail, show individuals selectively.

Inside a selected building
    Show rooms, routes, objects, affordances and embodied agents.

Selected or followed
    Expose full state, history, knowledge and causal explanation.

Across all levels
    Preserve time, selection, provenance, uncertainty and branch context.
```

The map should be the geographic backbone, not a screen filled permanently with dots. The local world and building views should provide embodiment where it has analytical value. Randomness should create controlled variation inside valid mechanisms, not unexplained motion. The design system should make truth, belief, provenance and uncertainty visually explicit. The frontend should consume event-sourced read models through stable contracts and remain replaceable, offline-capable and independent of the simulation kernel.

The core UI rule is:

> **Show the world at the level needed for the current task, preserve the path to detail, and never imply more precision, certainty or knowledge than the simulation actually contains.**

---

## Final recommendation

Do **not** build another “LLM society.”

Build a **deterministic, event-sourced simulation operating system** in which:

- Geography is authoritative.
- Time is authoritative.
- Movement is authoritative.
- Ownership and resources are authoritative.
- Knowledge has provenance.
- Belief is separate from truth.
- Every consequence has a causal path.
- Every important action is replayable.
- Every AI component is replaceable.
- Every model call is observable.
- Every scenario declares its assumptions.
- Every claim of realism has a validation measure.

Then allow LLMs to contribute where they are genuinely strong:

- Expressing language.
- Interpreting ambiguous information.
- Proposing bounded plans.
- Compressing experience.
- Handling unusual situations.
- Generating scenario drafts.
- Producing human-readable explanations.

The best summary is:

> **Games provide the world, rules, perception, planning, execution, navigation, affordances, scheduling, debugging and scale architecture. Classical agent-based modelling provides calibration, population mechanisms and scientific discipline. LLMs provide bounded language and reasoning. None of those three should be allowed to impersonate the other two.**
