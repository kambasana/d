---
title: Research Method and Evidence Quality
document_id: AWG-VIS-005
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
- AWG-VIS-004
- AWG-GOV-001
linear_issue: null
supersedes: []
---

# Research Method and Evidence Quality

## Purpose

Define how papers, repositories, game-AI patterns, standards, datasets, and empirical claims are collected, graded, cited, and revisited.

## Status and authority

This document is normative. Its current status is **draft**. Where this document conflicts with the Simulation Constitution, the Constitution takes precedence.

## Scope

- Evidence intake and source classification.
- Distinguishing architectural inspiration from validated mechanisms.
- Recording dates, versions, licences, limitations, and conflicting evidence.
- Rules for claims about human realism, prediction, and scale.

## Non-goals

- This document does not authorize bypassing the simulation kernel, provenance model, security boundary, or event history.
- It does not claim that a plausible simulation output is an empirically validated forecast.
- It does not make a specific vendor, model, database, or rendering engine part of the core domain contract unless explicitly stated.

## Normative requirements

- Primary sources and official repositories are preferred for technical claims.
- A repository demonstration is not treated as scientific validation.
- Claims about human behaviour must identify the population, task, benchmark, and uncertainty.
- Evidence entries record retrieval date, source type, quality level, relevance, and limitations.
- Contradictory evidence is retained rather than silently resolved.

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

- Every cited reusable component has an evidence entry and licensing review status.
- Every major design principle identifies its evidence basis or is explicitly marked as a design choice.
- The pack does not use star counts, demos, or fluent transcripts as substitutes for validation.

## Related documents

- AWG-VIS-004
- AWG-GOV-001
