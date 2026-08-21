---
title: Accessibility and Inclusive Design
document_id: AWG-UX-006
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
- AWG-UX-001
linear_issue: null
supersedes: []
---

# Accessibility and Inclusive Design

## Purpose

Ensure maps, graphs, timelines, clusters, alerts, and controls remain operable without relying only on colour, motion, pointer input, or visual maps.

## Status and authority

This document is normative. Its current status is **draft**. Where this document conflicts with the Simulation Constitution, the Constitution takes precedence.

## Scope

- Ensure maps, graphs, timelines, clusters, alerts, and controls remain operable without relying only on colour, motion, pointer input, or visual maps.

## Non-goals

- This document does not authorize bypassing the simulation kernel, provenance model, security boundary, or event history.
- It does not claim that a plausible simulation output is an empirically validated forecast.
- It does not make a specific vendor, model, database, or rendering engine part of the core domain contract unless explicitly stated.

## Normative requirements

- The implementation must conform to the rules defined in this specification for accessibility and inclusive design.
- All state-changing operations must use typed commands, validation, and append-only domain events where applicable.
- Any uncertainty, approximation, generated data, or external dependency must be explicitly identified and traceable.
- Implementations must preserve offline operation and provider replaceability unless a capability is explicitly declared optional.

## Detailed specification

## Requirements

- Keyboard access to map-adjacent controls, lists, inspectors, timeline, and radial/cluster alternatives.
- Every cluster/marker has an accessible label containing count/type/location meaning.
- Provide list/table alternatives for spatial selections and radial expansions.
- Do not rely on color alone for world truth vs belief, warning, uncertainty, or selection.
- Respect reduced-motion settings; cluster merge/split animations must not be required for understanding.
- Support sufficient contrast and scalable text.
- Focus moves predictably when opening inspectors, cluster menus, and building browsers.
- Virtualized data grids retain screen-reader semantics where feasible.
- Map-only information should have textual summaries for selected region/entity.

## Cognitive clarity

Avoid anthropomorphic UI claims that imply sentience or certainty. Use precise labels such as `agent belief`, `simulated state`, `estimated population`, and `model-generated summary`.

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

- AWG-UX-001
