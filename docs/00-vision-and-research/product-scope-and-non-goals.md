---
title: Product Scope and Non-Goals
document_id: AWG-VIS-002
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
- AWG-VIS-001
- AWG-GOV-001
linear_issue: null
supersedes: []
---

# Product Scope and Non-Goals

## Purpose

Bound the platform so that it is not mistaken for a chatbot village, omniscient digital twin, or guaranteed prediction engine.

## Status and authority

This document is normative. Its current status is **draft**. Where this document conflicts with the Simulation Constitution, the Constitution takes precedence.

## Scope

- Bound the platform so that it is not mistaken for a chatbot village, omniscient digital twin, or guaranteed prediction engine.

## Non-goals

- This document does not authorize bypassing the simulation kernel, provenance model, security boundary, or event history.
- It does not claim that a plausible simulation output is an empirically validated forecast.
- It does not make a specific vendor, model, database, or rendering engine part of the core domain contract unless explicitly stated.

## Normative requirements

- The implementation must conform to the rules defined in this specification for product scope and non-goals.
- All state-changing operations must use typed commands, validation, and append-only domain events where applicable.
- Any uncertainty, approximation, generated data, or external dependency must be explicitly identified and traceable.
- Implementations must preserve offline operation and provider replaceability unless a capability is explicitly declared optional.

## Detailed specification

## In scope

- Persistent geographically grounded world simulation.
- Real and synthetic OSM-like worlds.
- Multi-agent lives, groups, institutions, economies, and information networks.
- Offline-first operation where configured.
- Scenario interventions and counterfactual branches.
- World/agent firehose and replay.
- Modular AI and infrastructure adapters.
- Multiple levels of simulation and visualization fidelity.
- Evidence-based validation and explicit uncertainty.

## Non-goals

AWG is not:

- a guaranteed future prediction engine;
- a replacement for validated specialist scientific models;
- an always-on LLM for every simulated person;
- a claim to perfectly model human psychology;
- a chatbot town with decorative map markers;
- a system where natural-language narration directly edits authoritative state;
- a single graph database containing all workloads;
- dependent on one AI vendor, map provider, routing engine, or database;
- dependent on permanent internet access;
- a visual system that renders every agent individually at every map scale;
- a platform where demographic labels become personality stereotypes.

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

- AWG-VIS-001
- AWG-GOV-001
