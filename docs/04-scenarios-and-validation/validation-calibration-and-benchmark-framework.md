---
title: Validation, Calibration, and Benchmark Framework
document_id: AWG-SCN-002
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
- AWG-SCN-001
linear_issue: ELE-145
supersedes: []
---

# Validation, Calibration, and Benchmark Framework

## Purpose

Separate software verification, model validation, empirical calibration, human comparison, uncertainty analysis, and use-specific accreditation.

## Status and authority

This document is normative. Its current status is **draft**. Where this document conflicts with the Simulation Constitution, the Constitution takes precedence.

## Scope

- Separate software verification, model validation, empirical calibration, human comparison, uncertainty analysis, and use-specific accreditation.

## Non-goals

- This document does not authorize bypassing the simulation kernel, provenance model, security boundary, or event history.
- It does not claim that a plausible simulation output is an empirically validated forecast.
- It does not make a specific vendor, model, database, or rendering engine part of the core domain contract unless explicitly stated.

## Normative requirements

- The implementation must conform to the rules defined in this specification for validation, calibration, and benchmark framework.
- All state-changing operations must use typed commands, validation, and append-only domain events where applicable.
- Any uncertainty, approximation, generated data, or external dependency must be explicitly identified and traceable.
- Implementations must preserve offline operation and provider replaceability unless a capability is explicitly declared optional.

## Detailed specification

## Principle

AWG must distinguish software correctness from model validity. A coherent story is not evidence that the simulation is empirically credible.

## Validation layers

### 1. Software verification
Does the implementation obey its declared rules, schemas, invariants, and deterministic transitions?

### 2. Structural/model validation
Are the mechanisms appropriate for the phenomenon and correctly connected?

### 3. Empirical calibration
Do selected distributions/outcomes match relevant observed data within declared tolerance?

### 4. Out-of-sample validation
Can calibrated models reproduce withheld locations, time periods, or scenarios?

### 5. Human comparison
Where human behavior is claimed, compare with human data/baselines rather than only LLM judges.

### 6. Sensitivity/uncertainty
How much do results change under seeds, model/provider, prompt, parameters, data assumptions, activation rates, and structural choices?

## Domain validation

### Geography/mobility
- route validity;
- distance/time distributions;
- mode constraints;
- entrance/barrier compliance;
- congestion/rerouting behavior;
- indoor/outdoor continuity.

### Human activity
- sleep/work/time-use distributions;
- household/activity patterns;
- trip/activity duration;
- resource use;
- response to schedule disruptions.

### Information diffusion
- exposure mechanics;
- transmission probability/model;
- mutation/correction;
- source trust;
- repost/comment behavior;
- fact-check pathways;
- cascade size/speed when empirical references exist.

### Agent cognition
- goal/action consistency;
- precondition compliance;
- memory provenance;
- belief/truth separation;
- response stability;
- failure/fallback behavior.

### Organizations/economy
- membership/governance rules;
- resource conservation;
- transaction validity;
- market/institution behavior for selected scenarios.

## Research benchmarks

Use existing systems/papers as targeted benchmarks, not as blanket validation. Examples from the research pack include Generative Agents, SOTOPIA, 360CityArena, OASIS, Concordia, AgentSociety, AgentTorch/Large Population Models, CityBehavEx, and established NPC/game architectures.

## Reporting

Every serious scenario result should publish:

- model scope;
- calibration data;
- validation metrics;
- failed tests/gaps;
- sensitivity results;
- uncertainty intervals/distributions;
- model/provider versions;
- known limitations;
- whether output is descriptive, exploratory, or predictive.

## Prohibited validation shortcut

LLM-as-judge may be supplementary. It cannot be the sole evidence for physical, behavioral, social, or predictive validity.

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
- AWG-SCN-001
