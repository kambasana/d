---
title: Agent Runtime, Cognition, and Action Model
document_id: AWG-DOM-003
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
- AWG-DOM-002
linear_issue: ELE-139
supersedes: []
---

# Agent Runtime, Cognition, and Action Model

## Purpose

Define a proven NPC-style agent stack using perception, blackboards, needs, schedules, utility systems, planners, action executors, and bounded language models.

## Status and authority

This document is normative. Its current status is **draft**. Where this document conflicts with the Simulation Constitution, the Constitution takes precedence.

## Scope

- Define a proven NPC-style agent stack using perception, blackboards, needs, schedules, utility systems, planners, action executors, and bounded language models.

## Non-goals

- This document does not authorize bypassing the simulation kernel, provenance model, security boundary, or event history.
- It does not claim that a plausible simulation output is an empirically validated forecast.
- It does not make a specific vendor, model, database, or rendering engine part of the core domain contract unless explicitly stated.

## Normative requirements

- The implementation must conform to the rules defined in this specification for agent runtime, cognition, and action model.
- All state-changing operations must use typed commands, validation, and append-only domain events where applicable.
- Any uncertainty, approximation, generated data, or external dependency must be explicitly identified and traceable.
- Implementations must preserve offline operation and provider replaceability unless a capability is explicitly declared optional.

## Detailed specification

## Principle

Agents should live inside the simulation continuously, even when no LLM is being called. Their state persists through schedules, actions, relationships, obligations, memories, world events, and time.

## Agent composition

```text
Agent
├── Identity/provenance
├── Body/physical condition
├── Location/mobility state
├── Roles/obligations
├── Needs/drives
├── Schedule/routines
├── Goals
├── Perception filters
├── Working memory / blackboard
├── Episodic memory
├── Semantic knowledge
├── Claims/evidence/beliefs
├── Relationships/trust
├── Utility evaluation
├── Planner (GOAP/HTN/StateTree/other adapter)
├── Action executor
├── Communication policy
└── AI reasoning/dialogue adapters
```

## Decision hierarchy

Use the cheapest reliable mechanism first:

```text
1. hard rule / invariant
2. continue existing action
3. schedule/routine
4. state machine / StateTree / behavior tree
5. utility selection
6. GOAP/HTN planning
7. cached/compiled learned policy
8. bounded small-model reasoning
9. bounded larger-model reasoning
10. operator escalation if configured
```

LLM calls should occur at novelty boundaries, not every simulation tick.

## MVP 2 classical reference

`awg_mvp2.NpcKernel` is the executable classical stack for the bounded district:

- needs (`hunger`, `fatigue`) are explicit, event-sourced, and influence utility scores;
- schedules and routines remain event-driven; the cheapest applicable behaviour is selected each hour;
- utility scoring ranks `sleep`, `work`, `eat`, and `home`;
- a small GOAP-style plan sequences travel, exclusive smart-object reservation, and affordance use for eating;
- action channels `locomotion`, `hands`, `attention`, and `posture` reject impossible combinations such as sleep+travel or eat+work;
- households pair agents; organizations own places and unique assets;
- resource grants, transfers, consumption, and unique-asset ownership are conserved;
- perception records `AgentObserved` events only for the actor and physically co-located stationary witnesses.

This reference MUST NOT call an LLM. Dialogue adapters remain out of the MVP 2 state-transition path.

## Proven NPC patterns

Prefer established mechanisms before prompt reinvention:

- perception sensors/events;
- blackboard/typed working memory;
- utility AI;
- state machines/behavior trees/StateTree;
- GOAP/HTN preconditions/effects/costs;
- smart objects and reservations;
- action channels/concurrency;
- event-driven activation;
- context-aware dialogue;
- director/scenario separation;
- debugging/traceability.

## Actions

An executable action defines:

- action type;
- actor;
- arguments;
- preconditions;
- permissions;
- required resources/capabilities;
- resource locks/reservations;
- expected duration;
- effects on success;
- observations generated;
- cancellation/interruption rules;
- failure states;
- event outputs.

Example:

```text
TravelToPlace(destination, mode)

Preconditions:
- actor can move
- destination exists
- mode is available
- route is valid

Execution:
- mobility system creates and advances a journey

Completion:
- arrival event at valid destination transition/entrance
```

The LLM can propose the command. It cannot announce success and bypass execution.

## Action concurrency

Use explicit action channels such as:

```text
locomotion
posture
hands
attention
speech
digital_activity
long_running_obligation
```

Compatibility rules prevent impossible combinations while allowing realistic concurrent behavior such as sitting, eating, and conversing where constraints allow.

## Needs and goals

Humanistic systems must be explicit and configurable. They may include hunger, fatigue, safety, social obligations, work, money, care responsibilities, habits, commitments, preferences, and current emotional/physical state. Do not infer a complete psychology from demographics alone.

## Memory

Canonical memory is structured data with time and provenance. Embeddings are retrieval aids, not memory truth.

Memory types can include:

- episodic experiences;
- semantic knowledge;
- social/relationship history;
- procedures/skills;
- commitments/plans;
- claim/evidence references.

Memory decay/forgetting is a model rule with recorded parameters, not arbitrary deletion.

## Dialogue

Dialogue generation receives only permitted/available agent knowledge plus context and communication goals. It may express uncertainty and deception when the agent model permits it, but it must not invent unavailable factual knowledge merely to make text interesting.

## AI failure behavior

Malformed output, timeout, unavailable provider, or unsafe tool request cannot mutate world state. The runtime uses configured fallback, deterministic/default action, wait/defer behavior, or an explicit failure event.

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
- AWG-DOM-002
