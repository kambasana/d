---
title: Organization, Group, and Institution Model
document_id: AWG-DOM-005
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
linear_issue: null
supersedes: []
---

# Organization, Group, and Institution Model

## Purpose

Define persistent households, teams, communities, factions, organizations, institutions, governments, membership, authority, and collective action.

## Status and authority

This document is normative. Its current status is **draft**. Where this document conflicts with the Simulation Constitution, the Constitution takes precedence.

## Scope

- Define persistent households, teams, communities, factions, organizations, institutions, governments, membership, authority, and collective action.

## Non-goals

- This document does not authorize bypassing the simulation kernel, provenance model, security boundary, or event history.
- It does not claim that a plausible simulation output is an empirically validated forecast.
- It does not make a specific vendor, model, database, or rendering engine part of the core domain contract unless explicitly stated.

## Normative requirements

- The implementation must conform to the rules defined in this specification for organization, group, and institution model.
- All state-changing operations must use typed commands, validation, and append-only domain events where applicable.
- Any uncertainty, approximation, generated data, or external dependency must be explicitly identified and traceable.
- Implementations must preserve offline operation and provider replaceability unless a capability is explicitly declared optional.

## Detailed specification

## Social hierarchy

AWG supports overlapping structures rather than one rigid tree:

```text
Civilization / society
Government / institution
Organization
Faction / community
Household
Group / team
Individual
```

An agent can belong to multiple structures simultaneously.

## Organization state

An organization may have:

- identity/type;
- members and roles;
- leadership/governance;
- resources and property;
- territory/places;
- policies/rules;
- objectives;
- internal/external relationships;
- reputation/trust by observers;
- communication channels;
- decision mechanisms;
- schedules/operations;
- history and events.

## Group actions

Organizations/groups can create commands through explicit governance mechanisms rather than being treated as a single giant LLM personality. Examples include leader authority, voting, delegated roles, policy rules, committees, market mechanisms, or bounded organization-level planners.

## Membership

Join, leave, expel, hire, fire, appoint, elect, and transfer actions generate persistent relationship events.

## Knowledge

Organization knowledge is not automatically identical to every member's knowledge. Access depends on role, communication, records, classification, and propagation.

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
