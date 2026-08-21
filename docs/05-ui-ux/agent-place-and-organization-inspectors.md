---
title: Agent, Place, and Organization Inspectors
document_id: AWG-UX-004
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
- AWG-DOM-001
- AWG-DOM-003
- AWG-DOM-005
- AWG-UX-001
linear_issue: null
supersedes: []
---

# Agent, Place, and Organization Inspectors

## Purpose

Define structured inspection of current state, history, beliefs, provenance, relationships, occupancy, ownership, and causal explanations.

## Status and authority

This document is normative. Its current status is **draft**. Where this document conflicts with the Simulation Constitution, the Constitution takes precedence.

## Scope

- Define structured inspection of current state, history, beliefs, provenance, relationships, occupancy, ownership, and causal explanations.

## Non-goals

- This document does not authorize bypassing the simulation kernel, provenance model, security boundary, or event history.
- It does not claim that a plausible simulation output is an empirically validated forecast.
- It does not make a specific vendor, model, database, or rendering engine part of the core domain contract unless explicitly stated.

## Normative requirements

- The implementation must conform to the rules defined in this specification for agent, place, and organization inspectors.
- All state-changing operations must use typed commands, validation, and append-only domain events where applicable.
- Any uncertainty, approximation, generated data, or external dependency must be explicitly identified and traceable.
- Implementations must preserve offline operation and provider replaceability unless a capability is explicitly declared optional.

## Detailed specification

## Agent Inspector sections

1. Identity and provenance
2. Current world state
3. Location/journey
4. Schedule/current action
5. Needs/goals/obligations
6. Relationships/groups/organizations
7. Knowledge/beliefs/claims/evidence
8. Communications/social activity
9. Resources/ownership
10. Recent causal event chain
11. Simulation/model fidelity
12. Model calls relevant to recent decisions

Do not show simulator truth as if the agent knows it. Use separate tabs/labels for `World truth` and `Agent perspective`.

## Place/Building Inspector

- geometry/source/provenance;
- entrances/access;
- occupancy count and exact/aggregate status;
- floors/rooms where available;
- smart objects/affordances;
- organizations/owners/operators;
- resources/capacity;
- active events/incidents;
- movement flows;
- local firehose.

## Organization Inspector

- members/roles;
- leadership/governance;
- resources/property;
- places/territory;
- objectives/policies;
- relationships;
- organizational knowledge vs member knowledge;
- communications;
- current decisions/actions;
- relevant events.

## Cross-selection

Clicking an entity reference should preserve context and allow back-navigation. Selecting a claim from an agent should open the provenance chain; selecting a place should reveal occupants; selecting an organization should reveal members/locations without losing the current simulation time/branch.

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

- AWG-DOM-001
- AWG-DOM-003
- AWG-DOM-005
- AWG-UX-001
