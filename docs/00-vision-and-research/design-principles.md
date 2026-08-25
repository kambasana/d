---
title: Design Principles
document_id: AWG-VIS-003
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

# Design Principles

## Purpose

Set the cross-cutting design principles used by architecture, product, simulation, research, and UI work.

## Status and authority

This document is normative. Its current status is **draft**. Where this document conflicts with the Simulation Constitution, the Constitution takes precedence.

## Scope

- Set the cross-cutting design principles used by architecture, product, simulation, research, and UI work.

## Non-goals

- This document does not authorize bypassing the simulation kernel, provenance model, security boundary, or event history.
- It does not claim that a plausible simulation output is an empirically validated forecast.
- It does not make a specific vendor, model, database, or rendering engine part of the core domain contract unless explicitly stated.

## Normative requirements

- The implementation must conform to the rules defined in this specification for design principles.
- All state-changing operations must use typed commands, validation, and append-only domain events where applicable.
- Any uncertainty, approximation, generated data, or external dependency must be explicitly identified and traceable.
- Implementations must preserve offline operation and provider replaceability unless a capability is explicitly declared optional.

## Detailed specification

1. **Simulation first, AI second.** AI augments bounded reasoning and language; it does not replace world mechanics.
2. **Nothing teleports.** People, objects, consequences, and information require valid paths through space, time, systems, or communication networks.
3. **World truth is separate from belief.** Agents act on what they know or believe, not privileged simulator truth.
4. **Established mechanics before invention.** Prefer proven game/NPC/ABM patterns for perception, planning, action, navigation, scheduling, concurrency, and debugging.
5. **Typed actions over prose.** Natural language can propose; typed commands and deterministic systems execute.
6. **Event-sourced observability.** Important actions and state transitions are machine-readable and replayable.
7. **Multi-resolution by design.** Distant populations can be aggregated; selected/local agents can become highly detailed.
8. **Visualization is a projection.** Clusters, heatmaps, radial expansions, and semantic zoom do not change simulation state.
9. **Offline is architectural.** Core scenarios can be packaged with local geography, routing, maps, models, and storage.
10. **Adapters protect the core.** Providers are replaceable implementations, not domain concepts.
11. **Randomness is controlled.** Noise represents uncertainty and variation within constraints, never unexplained rule-breaking.
12. **Validation beats believability.** Attractive conversations and animations are not evidence of model correctness.

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
