---
title: Canonical World Model and Ontology
document_id: AWG-DOM-001
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
linear_issue: ELE-137
supersedes: []
---

# Canonical World Model and Ontology

## Purpose

Define stable identities, entities, relationships, lifecycles, temporal semantics, spatial semantics, and provenance classes.

## Status and authority

This document is normative. Its current status is **draft**. Where this document conflicts with the Simulation Constitution, the Constitution takes precedence.

## Scope

- Define stable identities, entities, relationships, lifecycles, temporal semantics, spatial semantics, and provenance classes.

## Non-goals

- This document does not authorize bypassing the simulation kernel, provenance model, security boundary, or event history.
- It does not claim that a plausible simulation output is an empirically validated forecast.
- It does not make a specific vendor, model, database, or rendering engine part of the core domain contract unless explicitly stated.

## Normative requirements

- The implementation must conform to the rules defined in this specification for canonical world model and ontology.
- All state-changing operations must use typed commands, validation, and append-only domain events where applicable.
- Any uncertainty, approximation, generated data, or external dependency must be explicitly identified and traceable.
- Implementations must preserve offline operation and provider replaceability unless a capability is explicitly declared optional.

## Detailed specification

## Purpose

Define stable semantic entities independent of storage technology and provider implementations.

## Top-level world hierarchy

```text
World
├── Scenario state and branch history
├── Time
├── Geography
│   ├── Region
│   ├── Administrative area
│   ├── Place
│   ├── Street/path/network edge
│   ├── Building
│   ├── Floor
│   ├── Room/area
│   └── Object/affordance
├── Population
│   ├── Cohort
│   ├── Agent
│   ├── Household
│   ├── Group
│   └── Organization/institution
├── Mobility
│   ├── Route
│   ├── Journey
│   ├── Leg
│   └── Vehicle
├── Resources/economy
├── Information space
│   ├── Observation
│   ├── Claim
│   ├── Evidence
│   ├── Message
│   ├── Post/comment/reaction
│   └── Belief
└── Event history
```

## Core entities

### World
Persistent simulation namespace with authoritative clock, spatial model, enabled systems, scenario lineage, and branch identity.

### Scenario
Versioned configuration of initial conditions, external data, population synthesis, model/plugin versions, random seeds, scheduled events, interventions, measurements, and stop conditions.

### Branch
Counterfactual continuation from a known snapshot/event point. Branches share immutable history before the branch point.

### Agent
Persistent simulated actor. An agent has identity, body/state, location, roles, relationships, goals, schedule, knowledge/beliefs, action capabilities, and event history. The agent is not the LLM used by one of its reasoning components.

### Cohort
Aggregate population representation used when individual instantiation is unnecessary. Cohorts carry distributions, counts, constraints, and aggregate history.

### Place
Spatially identified entity with geometry or spatial reference, semantic type, containment, access, nearby relationships, and possible entrances/affordances.

### Building / floor / room
Nested occupiable places with explicit entrance/transition relationships. A building is not represented only by its centroid.

### Object
World entity with state, ownership/access, location, capacity, and optionally typed affordances.

### Smart affordance
Typed interaction such as sit, enter, queue, buy, use, open, sleep, work, or charge. Affordances define preconditions, duration, resource locks, effects, observations, and failures.

### Intent
Proposed goal/action before validation.

### Command
Typed request submitted to authoritative systems. Commands do not imply success.

### Event
Immutable record of occurrence/state transition. Events may reference causation, parent events, location, actor, target, scenario, branch, and provenance.

### Observation
Agent-specific representation of something available through a valid sensory, communication, media, or record-access path.

### Claim
Proposition asserted or communicated, with source and lineage. A claim may be true, false, uncertain, disputed, or unknown to the simulator.

### Belief
Agent-specific stance toward a proposition, including confidence, evidence, contradictions, and update history.

### Relationship
Typed relationship between entities. Examples: knows, follows, works_for, member_of, lives_with, owns, controls, trusts_in_domain, supplies, located_at.

## Temporal semantics

Important relationships and states should support valid time. Examples:

- Agent A worked for Organization X from t1 to t2.
- Building entrance E was closed from t3 to t4.
- Agent B believed Claim C with confidence 0.7 at t5 and later changed to 0.2.

History is append-preserving; current state is a projection over events/state transitions.

## Spatial semantics

Entities can have:

- exact geometry;
- point/area reference;
- containment;
- route/network position;
- building/floor/room context;
- mobility state;
- uncertainty/precision.

Map display coordinates are not automatically authoritative coordinates.

## Provenance classes

Every externally or synthetically populated property should support one of:

```text
observed
imported
transformed
derived
statistically_sampled
scenario_assumption
synthetic_generated
model_inferred
human_entered
```

## Persistence principle

The world graph is a semantic API/model. It may be physically implemented using multiple stores. Storage choice must not change entity meaning.

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
