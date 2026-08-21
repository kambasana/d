---
title: Command, Event, Firehose, and Replay Specification
document_id: AWG-PLAT-002
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
- AWG-PLAT-001
linear_issue: ELE-141
supersedes: []
---

# Command, Event, Firehose, and Replay Specification

## Purpose

Define typed intentions and commands, validation, immutable domain events, causal links, snapshots, replay, branches, subscriptions, and model-call provenance.

## Status and authority

This document is normative. Its current status is **draft**. Where this document conflicts with the Simulation Constitution, the Constitution takes precedence.

## Scope

- Define typed intentions and commands, validation, immutable domain events, causal links, snapshots, replay, branches, subscriptions, and model-call provenance.

## Non-goals

- This document does not authorize bypassing the simulation kernel, provenance model, security boundary, or event history.
- It does not claim that a plausible simulation output is an empirically validated forecast.
- It does not make a specific vendor, model, database, or rendering engine part of the core domain contract unless explicitly stated.

## Normative requirements

- The implementation must conform to the rules defined in this specification for command, event, firehose, and replay specification.
- All state-changing operations must use typed commands, validation, and append-only domain events where applicable.
- Any uncertainty, approximation, generated data, or external dependency must be explicitly identified and traceable.
- Implementations must preserve offline operation and provider replaceability unless a capability is explicitly declared optional.

## Detailed specification

## Concepts

```text
Intent -> Command -> Validation -> Execution -> Domain Event -> State/Observation/Projection
```

An intent is not proof that an action occurred. A command is not proof of success. Domain events record outcomes.

## Command requirements

Every command has:

- command_id;
- schema_version;
- world_id;
- scenario_id;
- branch_id;
- actor/authority;
- command_type;
- typed arguments;
- issued_at simulation time;
- causal/input references;
- source class (agent, scenario, operator, system);
- optional model provenance;
- idempotency/correlation information where required.

Validation checks schema, authority, preconditions, current state, resource/capacity/access constraints, and relevant domain rules.

## Event envelope

Minimum conceptual envelope:

```yaml
event_id: EVT-...
schema_version: 1
world_id: ...
scenario_id: ...
branch_id: ...
simulation_time: ...
wall_clock_time: ...
sequence: ...
event_type: JourneyStarted
actor_id: ...
target_ids: []
command_id: ...
parent_event_ids: []
caused_by_event_ids: []
location_ref: ...
observation_scope: ...
plugin_ref: ...
random_stream_ref: ...
model_call_ref: ...
provenance: ...
payload: {}
```

## Event families

```text
world.*
agent.*
movement.*
place.*
perception.*
memory.*
belief.*
claim.*
communication.*
social.*
relationship.*
organization.*
economy.*
resource.*
infrastructure.*
scenario.*
model.*
validation.*
```

Infrastructure/software telemetry uses a separate telemetry namespace/plane.

## Firehose

The firehose supports filtered subscription by world, branch, time, event type, actor, place, claim, organization, and other indexed references.

Use cases:

- live UI updates;
- analytics;
- debugging;
- agent/world inspection;
- replay;
- audit;
- scenario comparison;
- future virtual social media clients;
- export to downstream systems.

## Ordering

The platform must define deterministic ordering within a partition/authority scope and explicit causal links across distributed regions. Wall-clock arrival order is not automatically simulation order.

## Snapshots

Snapshots accelerate restore but do not replace the event history needed for causal analysis. A snapshot records:

- event/sequence boundary;
- world/branch;
- schema versions;
- plugin/model configuration references;
- state checksum or equivalent integrity metadata.

## Replay

Replay modes:

### Deterministic core replay
Re-run reducers/systems from recorded commands/events using the same schemas, versions, inputs, and random streams.

### Recorded-AI replay
Use previously recorded model outputs instead of calling Ollama/OpenRouter/other provider again.

### Live-model re-simulation
Explicitly create a new run/branch when a model is re-called. Do not call it the same deterministic replay if outputs can differ.

## Branching

A counterfactual branch:

1. identifies a snapshot/event boundary;
2. reuses immutable prior history;
3. receives a new branch_id;
4. applies one or more declared intervention differences;
5. records all divergent events independently.

## Corrections

Use explicit events such as:

```text
ClaimCorrected
ClaimRetracted
RecordSuperseded
OwnershipTransferred
```

Never delete history merely because current truth/state changed.

## Backpressure and consumers

Firehose consumers must not block the authoritative simulation loop indefinitely. Use buffered/partitioned delivery, replayable offsets, and consumer-specific degradation policies.

## Model calls as provenance

When a model influences an intent, plan, summary, claim extraction, or dialogue, record a model-call reference with provider/model/prompt-policy/schema/fallback metadata.

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
- AWG-PLAT-001
