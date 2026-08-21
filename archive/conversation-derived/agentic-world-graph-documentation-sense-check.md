# Agentic World Graph Documentation Sense Check

## Executive Assessment

The documentation set is already strong on:

- Product vision.
- Research and prior art.
- UI and UX.
- Map visualization.
- Agent clustering and semantic zoom.
- Agent cognition.
- Information diffusion.
- Geospatial grounding.
- Modular architecture.

The main remaining risk is that the project could still read as an ambitious system concept rather than a platform that can be built, tested, validated, governed, and maintained.

The next documentation should convert the vision into enforceable contracts.

---

## 1. Simulation Constitution and Non-Negotiable Invariants

This is the most important missing document.

It should define rules that no plugin, LLM, scenario, operator, or UI component can bypass.

### Core invariants

- Agents cannot teleport.
- Information cannot teleport.
- LLMs cannot directly mutate authoritative world state.
- Every state change must result from a validated command or an explicit scenario intervention.
- Agent belief must remain separate from world truth.
- Every important fact must have provenance.
- Every movement must have a valid path, movement mode, and elapsed time.
- Every resource, object, and location must support capacity and access constraints.
- Replay must preserve history rather than overwrite it.
- Randomness must be seeded, typed, and attributable.
- Model changes must be recorded.
- Visual clustering must never alter authoritative spatial state.
- Aggregate populations must not be presented as fully simulated individuals.
- Generated assumptions must not be presented as observed facts.
- Social actions such as likes, reposts, and comments must not automatically be interpreted as belief or endorsement.
- Scenario controllers may introduce conditions but must not secretly force agent outcomes.
- Plugins may extend capabilities but must not bypass validation, provenance, or event recording.

This document should become the architectural constitution against which all future designs are reviewed.

**Suggested filename:**

```text
simulation-constitution-and-invariants.md
```

---

## 2. Canonical Domain Model and World Ontology

The platform includes people, organizations, claims, places, buildings, routes, events, objects, and social interactions. These concepts need a canonical vocabulary and lifecycle model.

### Primary entities

```text
World
Scenario
Branch
Agent
Population Cohort
Group
Household
Organization
Place
Geographic Feature
Building
Floor
Room
Entrance
Route
Journey
Vehicle
Object
Resource
Action
Intent
Command
Validation Result
Event
Observation
Memory
Claim
Belief
Message
Post
Relationship
Intervention
Projection
```

For every entity, define:

- Identity.
- Required properties.
- Optional properties.
- Relationships.
- Temporal behaviour.
- Spatial behaviour.
- Provenance.
- Ownership.
- Lifecycle.
- Versioning.
- Whether it belongs to world truth, agent belief, or a user-interface projection.
- Whether it is observed, inferred, generated, or simulated.

The document should also clarify that the **world graph is a semantic model and API**, not necessarily one physical graph database.

Different storage technologies may be used for different workloads:

- PostGIS for authoritative geometry.
- Relational storage for transactions and ownership.
- Append-only storage for events.
- Columnar storage for analytics.
- Search indexes for retrieval.
- Graph projections for relationships and provenance.
- Blob storage for media.

**Suggested filename:**

```text
canonical-world-model-and-ontology.md
```

---

## 3. Command, Event, Firehose, and Replay Specification

The firehose is central enough to require its own formal contract.

The document should define the difference between:

```text
Intent
Command
Validation Result
Domain Event
Observation
Projection
Telemetry
```

### Expected execution flow

```text
Agent, scenario, or operator proposes an intention
        ↓
Intention becomes a typed command
        ↓
Command is validated
        ↓
Simulation executes or rejects the command
        ↓
Domain events are emitted
        ↓
Authoritative world state changes
        ↓
Eligible agents receive observations
        ↓
Beliefs and memories may change
        ↓
UI and analytics projections update
```

### Event envelope requirements

The specification should define:

- Event identifier.
- Schema version.
- World identifier.
- Scenario identifier.
- Branch identifier.
- Simulation time.
- Wall-clock time.
- Tick or sequence number.
- Event type.
- Actor.
- Targets.
- Command reference.
- Parent events.
- Causal events.
- Location reference.
- Observation scope.
- Plugin identifier and version.
- Random stream metadata.
- Model provenance.
- Payload.
- Result.
- Uncertainty.
- Data provenance.
- Retention class.

### Replay requirements

- Replay without calling an LLM again by using recorded model outputs.
- Deterministic replay of non-LLM systems.
- Snapshot and restore.
- Branching at a selected point.
- Counterfactual intervention.
- Branch comparison.
- Corrections and retractions without deleting history.
- Causal tracing from outcome back to command, observation, belief, and source.
- Export to machine-readable formats.
- Subscription filters and backpressure rules.

**Suggested filename:**

```text
command-event-firehose-and-replay-specification.md
```

---

## 4. Agent Runtime, Cognition, and Action Model

The agent itself needs a formal, implementation-facing architecture.

### Proposed agent structure

```text
Agent
├── Identity
├── Body and physical condition
├── Location
├── Roles
├── Responsibilities and obligations
├── Needs and drives
├── Schedule
├── Goals
├── Perception
├── Working memory
├── Episodic memory
├── Semantic knowledge
├── Beliefs
├── Claims and evidence
├── Relationships
├── Trust
├── Utility evaluation
├── Planning
├── Action execution
├── Communication policy
└── Dialogue realization
```

### Decision hierarchy

The architecture should use the cheapest reliable mechanism first:

```text
1. Hard rule or safety invariant
2. Existing action execution
3. Schedule
4. State machine
5. Utility AI
6. GOAP or HTN planning
7. Cached or compiled policy
8. Small-model bounded reasoning
9. Larger-model novel reasoning
10. Human or operator escalation where configured
```

The document should define:

- When an LLM may be called.
- When an LLM must not be called.
- Allowed action schemas.
- Preconditions and effects.
- Interruptions.
- Failure states.
- Action channels.
- Memory writes.
- Belief updates.
- Trust updates.
- Perception filters.
- Conversation constraints.
- Fallback behaviour.
- Degraded operation when model providers fail.

**Suggested filename:**

```text
agent-runtime-cognition-and-action-model.md
```

---

## 5. Spatial World, Mobility, and Building Specification

The OSM and movement requirements deserve a dedicated technical specification.

### Scope

- Authoritative coordinate systems.
- OSM identifiers and provenance.
- Gazetteer role.
- Routing graph role.
- PMTiles role.
- Building geometry.
- Entrances and exits.
- Floors and rooms.
- Indoor and outdoor transitions.
- Vehicles and transport modes.
- Accessibility.
- Barriers.
- Restricted areas.
- Route interruption.
- Journey state.
- Travel-time calculation.
- Local movement and collision.
- Synthetic geography.
- Co-location and occupancy.
- Spatial simulation levels of detail.
- Map and interior visualization levels of detail.

### Required principle

```text
PMTiles renders the world.

PostGIS, OSM-derived topology, and routing data define the world.

Simulation state records who and what is currently where.
```

The document should distinguish:

- Named place.
- Place geometry.
- Entrance.
- Traversable path.
- Occupancy area.
- Building shell.
- Interior model.
- Route segment.
- Journey.
- Transport leg.
- Local physical movement.

**Suggested filename:**

```text
spatial-world-mobility-and-building-specification.md
```

---

## 6. Scenario Definition and Experiment Protocol

A scenario must become more than a collection of prompts.

It should be a versioned, reproducible package containing:

- Base world.
- Geographic extent.
- Start time.
- Population.
- Population-generation method.
- Agent distributions.
- Organizations.
- Infrastructure.
- Resources.
- Social networks.
- Communication networks.
- Behavioural parameters.
- Random seeds.
- Enabled plugins.
- Model configuration.
- Initial conditions.
- Scheduled events.
- Interventions.
- Measurement definitions.
- Stop conditions.
- Expected invariants.
- Validation targets.
- Known assumptions.
- Known limitations.

### Branching model

```text
Baseline branch
        ├── Intervention A
        ├── Intervention B
        └── Intervention C
```

The protocol should define:

- Reproducibility.
- Baseline establishment.
- Intervention timing.
- Branch identity.
- Comparison metrics.
- Seed management.
- Model version control.
- Scenario packaging.
- Export and sharing.
- Experimental notes.
- Outcome uncertainty.

**Suggested filename:**

```text
scenario-definition-and-experiment-protocol.md
```

---

## 7. Validation, Calibration, and Benchmark Framework

Without this document, the project could still become an impressive-looking but untrustworthy simulation.

### Geography validation

- Route validity.
- Travel distance.
- Travel time.
- Entrance usage.
- Barrier compliance.
- Transport mode compliance.
- Indoor and outdoor continuity.

### Human activity validation

- Time-use distributions.
- Work and sleep schedules.
- Household behaviour.
- Mobility patterns.
- Resource usage.
- Activity duration.
- Response to interruptions.

### Information diffusion validation

- Exposure.
- Transmission.
- Mutation.
- Belief change.
- Reposting.
- Fact-checking.
- Source trust.
- Correction and retraction.
- Bad-actor influence.

### Agent cognition validation

- Goal consistency.
- Constraint compliance.
- Memory provenance.
- Behaviour stability.
- Response to interventions.
- LLM failure handling.
- Action feasibility.
- Belief and truth separation.

### System validation

- Replay determinism.
- Seed sensitivity.
- Model-provider sensitivity.
- Prompt-policy sensitivity.
- Plugin replacement.
- Scale testing.
- Failure recovery.
- Event ordering.
- Cross-region consistency.

### Validation categories

```text
Software verification
Model validation
Empirical calibration
Human evaluation
Sensitivity analysis
Uncertainty analysis
Accreditation for specific uses
```

**Suggested filename:**

```text
validation-calibration-and-benchmark-framework.md
```

---

## 8. Multi-Resolution Simulation and Scaling Architecture

Simulation fidelity and visualization fidelity should be formalized separately.

### Simulation levels

```text
S0 — Aggregate population
S1 — Cohort or archetype
S2 — Scheduled individual
S3 — Cognitive individual
S4 — Fully embodied local agent
```

### Visualization levels

```text
V0 — Hidden or aggregate
V1 — Heatmap
V2 — Cluster
V3 — Individual marker
V4 — Detailed avatar or interior representation
```

### Required topics

- Promotion and demotion.
- State compression.
- Population synthesis.
- Batch updates.
- Event-driven activation.
- Spatial partitioning.
- Cross-region movement.
- Distributed ownership.
- LLM call budgets.
- Caching.
- Model routing.
- Simulation-clock coordination.
- Performance targets.
- Cost controls.
- Failure isolation.
- Fidelity-transition provenance.
- Aggregate-to-individual continuity.
- Individual-to-aggregate compression.

**Suggested filename:**

```text
multi-resolution-simulation-and-scaling-architecture.md
```

---

## 9. Plugin and Adapter SDK Specification

The statement that everything is modular only becomes meaningful when the interfaces are explicit.

### Proposed adapter families

```text
AIProviderAdapter
EmbeddingAdapter
MapAdapter
GazetteerAdapter
RoutingAdapter
MobilityAdapter
PhysicsAdapter
StorageAdapter
EventBusAdapter
SocialPlatformAdapter
EconomyAdapter
WeatherAdapter
VisualizationAdapter
AnalyticsAdapter
AuthenticationAdapter
```

For each adapter, define:

- Inputs and outputs.
- Capabilities.
- Versioning.
- Error handling.
- Timeouts.
- Retry rules.
- Fallback behaviour.
- Health checks.
- Data ownership.
- Security boundaries.
- Offline compatibility.
- Determinism guarantees.
- Test contract.
- Plugin lifecycle.
- Migration strategy.
- Compatibility matrix.
- Capability discovery.

Also define how plugins are:

- Discovered.
- Enabled.
- Disabled.
- Replaced.
- Versioned.
- Sandboxed.
- Audited.
- Tested.
- Rolled back.

**Suggested filename:**

```text
plugin-adapter-sdk-and-compatibility-contracts.md
```

---

## 10. Security, Safety, Privacy, and Misuse Model

The platform may simulate populations, misinformation, crises, bad actors, and real geography. That creates serious governance requirements.

### Required topics

- Prompt injection through agent messages and social posts.
- Malicious plugins.
- Model-output validation.
- Secrets and provider credentials.
- Personal-data handling.
- Synthetic versus real-person representation.
- Re-identification risk.
- Sensitive geospatial data.
- Scenario authorization.
- Abuse monitoring.
- Export controls.
- Audit logs.
- Role-based access.
- Data retention.
- Content moderation.
- Misleading claims of predictive accuracy.
- Rules for high-consequence scenarios.
- Access to intervention controls.
- Dataset and model licensing.
- Security boundaries between plugins.
- Offline and air-gapped deployment.
- Incident response.

The document should explicitly prohibit presenting simulated outcomes as guaranteed forecasts.

**Suggested filename:**

```text
security-safety-privacy-and-misuse-model.md
```

---

## 11. UI Application Architecture and Design System Specification

The existing UI and UX work is substantial, but it should be extracted into an implementation-facing specification.

### Application areas

- World Explorer.
- Scenario Studio.
- Agent Inspector.
- Place Inspector.
- Organization Inspector.
- Information Space.
- Timeline and replay controls.
- Firehose Explorer.
- Comparison Workspace.
- Building and interior view.
- Map layer management.
- Cluster and semantic-zoom controls.
- Radial co-location expansion.
- Analytics dashboards.
- Plugin management.
- Experiment status.
- Validation results.

### Design-system requirements

- Design tokens.
- Typography.
- Spacing.
- Elevation.
- Iconography.
- Data-visualization tokens.
- Status semantics.
- Interaction states.
- Loading states.
- Empty states.
- Error states.
- Degraded states.
- Offline states.
- Accessibility.
- Keyboard navigation.
- Screen-reader labels.
- Focus management.
- Motion and reduced-motion handling.
- High-density information display.
- Responsive layout.
- Dark and light themes.
- Performance budgets.

### Architecture requirements

- Real-time event streaming.
- Projection APIs.
- Local caching.
- Offline map and scenario support.
- Web worker usage.
- Rendering boundaries.
- Map-layer plugin contracts.
- State synchronization.
- Time-travel and replay state.
- Selection persistence across zoom levels.
- Cluster continuity.
- Large-table virtualization.

**Suggested filename:**

```text
ui-application-architecture-and-design-system.md
```

The existing clustering document should become a focused child specification of this document.

---

## 12. MVP Roadmap and Definition of Done

The vision is large enough that it needs a delivery document preventing premature planetary scope.

### MVP 1 — One district, no LLM dependency

- Local OSM.
- PostGIS.
- Offline map.
- Gazetteer.
- Routing.
- Buildings and entrances.
- Scheduled agents.
- Valid movement.
- Event firehose.
- Replay.
- Agent clustering UI.
- Building occupancy view.

### MVP 2 — Classical NPC systems

- Needs.
- Utility AI.
- Schedules.
- Relationships.
- Smart objects.
- GOAP or HTN.
- Organizations.
- Resource constraints.
- Action channels.

### MVP 3 — Bounded LLM capabilities

- Dialogue realization.
- Claim extraction.
- Memory summarization.
- Novel-choice ranking.
- Ollama adapter.
- OpenRouter adapter.
- Structured outputs.
- Model-call provenance.
- Deterministic fallback.

### MVP 4 — Information environment

- Social network.
- Posts.
- Messages.
- Claims.
- Trust.
- Reposts.
- Fact-checking.
- Bad actors.
- Moderation.
- Information provenance graph.

### MVP 5 — Scaling

- Cohorts.
- Adaptive fidelity.
- Distributed regions.
- Large-scale scenarios.
- Population promotion and demotion.
- Event-driven activation.
- Performance benchmarking.

Every phase should have explicit:

- Entry criteria.
- Exit criteria.
- Acceptance tests.
- Performance targets.
- Known limitations.
- Required documentation.
- Required validation evidence.

**Suggested filename:**

```text
mvp-roadmap-and-definition-of-done.md
```

---

## Supporting Documents

These can remain smaller initially.

```text
glossary-and-controlled-vocabulary.md
architecture-decision-record-template.md
open-source-reuse-and-licensing-register.md
data-source-and-provenance-register.md
risk-and-assumption-register.md
model-and-prompt-version-register.md
plugin-compatibility-matrix.md
```

The licensing register is especially important because candidate systems and components may use Apache, AGPL, GPL, commercial, model-specific, data-specific, or OpenStreetMap-related licences.

---

## Recommended Documentation Structure

```text
docs/
├── 00-vision/
│   ├── product-vision.md
│   └── research-and-prior-art.md
│
├── 01-governance/
│   ├── simulation-constitution-and-invariants.md
│   ├── security-safety-privacy-and-misuse-model.md
│   └── risk-and-assumption-register.md
│
├── 02-domain/
│   ├── canonical-world-model-and-ontology.md
│   ├── agent-runtime-cognition-and-action-model.md
│   ├── information-trust-and-provenance-model.md
│   └── spatial-world-mobility-and-building-specification.md
│
├── 03-platform/
│   ├── system-architecture.md
│   ├── command-event-firehose-and-replay-specification.md
│   ├── plugin-adapter-sdk-and-compatibility-contracts.md
│   └── multi-resolution-simulation-and-scaling-architecture.md
│
├── 04-scenarios/
│   ├── scenario-definition-and-experiment-protocol.md
│   └── validation-calibration-and-benchmark-framework.md
│
├── 05-ui-ux/
│   ├── ui-application-architecture-and-design-system.md
│   └── agent-map-clustering-and-semantic-zoom.md
│
├── 06-delivery/
│   ├── mvp-roadmap-and-definition-of-done.md
│   ├── open-source-reuse-and-licensing-register.md
│   └── architecture-decision-records/
│
└── glossary-and-controlled-vocabulary.md
```

---

## Recommended Next Three Documents

The next three documents should be:

1. **Simulation Constitution and Invariants**
2. **Canonical World Model and Ontology**
3. **Command, Event, Firehose, and Replay Specification**

These three will expose contradictions early and prevent the platform from becoming a collection of loosely connected AI features.

---

## Final Sense Check

Another broad vision document is not needed at this stage.

The project now needs documents that convert the vision into enforceable contracts.

The strongest overall principle is:

> Build the rules, data contracts, provenance, replay, and validation framework before expanding the number of AI features.

That will preserve the difference between a serious simulation platform and a convincing but ungrounded agent demonstration.
