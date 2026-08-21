---
title: Economy, Resource, and Ownership Model
document_id: AWG-DOM-006
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
linear_issue: null
supersedes: []
---

# Economy, Resource, and Ownership Model

## Purpose

Define resources, inventories, transactions, assets, ownership, scarcity, markets, obligations, and economic event provenance.

## Status and authority

This document is normative. Its current status is **draft**. Where this document conflicts with the Simulation Constitution, the Constitution takes precedence.

## Scope

- Define resources, inventories, transactions, assets, ownership, scarcity, markets, obligations, and economic event provenance.

## Non-goals

- This document does not authorize bypassing the simulation kernel, provenance model, security boundary, or event history.
- It does not claim that a plausible simulation output is an empirically validated forecast.
- It does not make a specific vendor, model, database, or rendering engine part of the core domain contract unless explicitly stated.

## Normative requirements

- The implementation must conform to the rules defined in this specification for economy, resource, and ownership model.
- All state-changing operations must use typed commands, validation, and append-only domain events where applicable.
- Any uncertainty, approximation, generated data, or external dependency must be explicitly identified and traceable.
- Implementations must preserve offline operation and provider replaceability unless a capability is explicitly declared optional.

## Detailed specification

## Purpose

Economic/social scenarios require explicit resources and ownership rather than conversational claims that an agent "has" something.

## Core concepts

- resource type and quantity;
- asset/object identity;
- ownership/control/possession;
- money/accounting unit;
- price/cost;
- inventory;
- production/consumption;
- transaction;
- contract/obligation;
- capacity/scarcity;
- market/institution rules.

## Ownership

Ownership and possession are separate relationships. A rented car can be possessed by one agent while owned by another entity.

## Transactions

Transactions are typed, validated, time-stamped events. They check availability, permissions, quantities, payment/consideration where required, and update state atomically or through explicit failure/compensation events.

## Scarcity and behavior

Resources influence plans and feasible actions. Agents cannot consume or transfer resources that do not exist in their accessible inventory/state.

## Economic LOD

Large populations may use aggregate market/demand models while local/selected agents use individual transactions. Promotion/demotion must conserve quantities and avoid double counting.

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
