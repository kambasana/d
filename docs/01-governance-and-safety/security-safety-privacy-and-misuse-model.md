---
title: Security, Safety, Privacy, and Misuse Model
document_id: AWG-GOV-002
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
linear_issue: null
supersedes: []
---

# Security, Safety, Privacy, and Misuse Model

## Purpose

Define threat boundaries, privacy controls, misuse protections, access rules, and high-consequence scenario restrictions.

## Status and authority

This document is normative. Its current status is **draft**. Where this document conflicts with the Simulation Constitution, the Constitution takes precedence.

## Scope

- Define threat boundaries, privacy controls, misuse protections, access rules, and high-consequence scenario restrictions.

## Non-goals

- This document does not authorize bypassing the simulation kernel, provenance model, security boundary, or event history.
- It does not claim that a plausible simulation output is an empirically validated forecast.
- It does not make a specific vendor, model, database, or rendering engine part of the core domain contract unless explicitly stated.

## Normative requirements

- The implementation must conform to the rules defined in this specification for security, safety, privacy, and misuse model.
- All state-changing operations must use typed commands, validation, and append-only domain events where applicable.
- Any uncertainty, approximation, generated data, or external dependency must be explicitly identified and traceable.
- Implementations must preserve offline operation and provider replaceability unless a capability is explicitly declared optional.

## Detailed specification

## Security boundaries

- LLM output is untrusted input until schema and domain validation pass.
- Agent-generated posts/messages can contain prompt-injection content and must never become privileged system instructions.
- Plugins run with least privilege and explicit capability declarations.
- Secrets and provider credentials stay outside scenario content and agent memory.
- Event exports, data sources, and plugins require access controls appropriate to deployment.

## Privacy

Real-person simulation requires explicit provenance, legal basis/permission where applicable, minimization, retention rules, and controls against re-identification. Synthetic personas must be labelled synthetic.

## Sensitive geography

The platform must support redaction, precision reduction, access restrictions, and export controls for sensitive locations or datasets.

## Misuse controls

High-consequence scenarios must state intended use, limitations, uncertainty, data quality, and model validation. Simulated outcomes must not be presented as guaranteed forecasts.

## Adversarial information

Bad actors may exist inside scenarios, but platform controls must distinguish simulated adversarial behavior from real platform abuse. Simulation content cannot gain code execution, credential access, or privileged control over the host.

## Audit

Record operator interventions, plugin/version changes, model configuration changes, privileged exports, and scenario branch creation.

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
