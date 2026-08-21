---
title: Simulation Constitution and Invariants
document_id: AWG-GOV-001
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
depends_on: []
linear_issue: ELE-136
supersedes: []
---

# Simulation Constitution and Invariants

## Purpose

Define the non-negotiable laws that no model, plugin, scenario, operator, projection, or user interface may bypass.

## Status and authority

This document is normative. Its current status is **draft**. Where this document conflicts with the Simulation Constitution, the Constitution takes precedence.

## Scope

- Define the non-negotiable laws that no model, plugin, scenario, operator, projection, or user interface may bypass.

## Non-goals

- This document does not authorize bypassing the simulation kernel, provenance model, security boundary, or event history.
- It does not claim that a plausible simulation output is an empirically validated forecast.
- It does not make a specific vendor, model, database, or rendering engine part of the core domain contract unless explicitly stated.

## Normative requirements

- Authoritative state is owned by deterministic simulation systems, not by LLM output.
- People, objects, consequences, and information must have valid paths through space, time, ownership, or communication networks.
- World truth, agent belief, and user-interface projections must remain separate data planes.
- History is append-preserving; corrections and retractions are new events.
- Randomness is typed, seeded, recorded, and replayable.
- Every plugin must obey validation, provenance, security, and event-recording boundaries.

## Detailed specification

## Authority

The deterministic simulation kernel and validated domain systems own authoritative world state.

### INV-001 - No direct LLM state mutation
An LLM may propose typed intents or command arguments. It may not directly write authoritative positions, ownership, resources, event truth, physical state, or completed actions.

### INV-002 - No unexplained physical relocation
After scenario initialization, every position change requires valid movement, transport, or an explicit logged intervention with authority and reason.

### INV-003 - Time is causal
Travel, actions, queues, communication, work, sleep, and other processes consume simulation time according to their rules.

### INV-004 - Geography constrains behavior
Routes, barriers, entrances, access rights, modes, capacities, and topology constrain movement.

### INV-005 - Information requires a path
An agent only knows information through direct perception, communication, accessible records/media, prior memory, or explicit inference from available evidence.

### INV-006 - Truth and belief are separate
The world may know an event cause while agents hold different, uncertain, incorrect, manipulated, or contradictory beliefs.

### INV-007 - Social actions do not imply belief
Viewing, understanding, believing, endorsing, liking, commenting, reposting, and forwarding are distinct states/actions.

### INV-008 - History is append-preserving
Corrections, retractions, reversals, and updated beliefs create new records/events. Do not silently erase causal history.

### INV-009 - State transitions are observable
Important accepted commands and domain transitions emit versioned machine-readable events to the world firehose.

### INV-010 - Randomness is reproducible
Stochastic behavior uses named random streams/seeds and is recorded sufficiently for experiment comparison and replay.

### INV-011 - Simulation and visualization fidelity are independent
Rendering an individual marker does not imply full cognition. Aggregating an individual into a map cluster does not remove their authoritative state.

### INV-012 - Aggregates are not fake individuals
When promoting cohorts to individuals, generated detail must be marked synthetic/instantiated and constrained by aggregate history; it must not be presented as previously observed personal history.

### INV-013 - Scenario controllers cannot secretly force conclusions
Interventions change declared world conditions. Agents react according to their own state, information, constraints, and decision systems.

### INV-014 - Plugins cannot bypass the constitution
Every adapter must preserve validation, provenance, eventing, access, and safety boundaries.

### INV-015 - Provider changes are experiment-visible
Model/provider/version/prompt-policy/fallback changes are recorded and cannot silently alter a controlled run.

### INV-016 - Authoritative geography is not reconstructed from display tiles
PMTiles/Protomaps can present offline maps but do not replace OSM/PostGIS/routing topology as simulation authority.

### INV-017 - Human realism claims require evidence
Believable output, LLM judge scores, or visual plausibility alone are insufficient validation.

### INV-018 - Data provenance is explicit
Observed, imported, inferred, statistically sampled, scenario-assumed, and AI-generated data must be distinguishable.

### INV-019 - Trust is contextual
Trust is evaluated in context such as source, domain, channel, situation, and history rather than a universal number alone.

### INV-020 - Core operation can degrade safely without AI
Loss or failure of an AI provider must not corrupt authoritative simulation state. Systems must fail closed, use deterministic fallback where specified, or leave agents inactive/deferred.

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

- Invariant tests prove that agents cannot teleport, become omniscient, duplicate exclusive resources, or bypass command validation.
- A recorded run can be replayed without re-calling external model providers.
- All normative documents declare dependency on this Constitution or inherit it through another normative document.
- The requirements registry contains a stable requirement ID for every constitutional rule.

## Related documents

- None beyond the stated scope.
