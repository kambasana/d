---
title: Plugin and Adapter SDK Compatibility Contracts
document_id: AWG-PLAT-003
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
- AWG-PLAT-001
- AWG-PLAT-002
linear_issue: ELE-142
supersedes: []
---

# Plugin and Adapter SDK Compatibility Contracts

## Purpose

Define swappable adapters for AI providers, embeddings, maps, gazetteers, routing, mobility, physics, storage, social platforms, analytics, and visualization.

## Status and authority

This document is normative. Its current status is **draft**. Where this document conflicts with the Simulation Constitution, the Constitution takes precedence.

## Scope

- Define swappable adapters for AI providers, embeddings, maps, gazetteers, routing, mobility, physics, storage, social platforms, analytics, and visualization.

## Non-goals

- This document does not authorize bypassing the simulation kernel, provenance model, security boundary, or event history.
- It does not claim that a plausible simulation output is an empirically validated forecast.
- It does not make a specific vendor, model, database, or rendering engine part of the core domain contract unless explicitly stated.

## Normative requirements

- The implementation must conform to the rules defined in this specification for plugin and adapter sdk compatibility contracts.
- All state-changing operations must use typed commands, validation, and append-only domain events where applicable.
- Any uncertainty, approximation, generated data, or external dependency must be explicitly identified and traceable.
- Implementations must preserve offline operation and provider replaceability unless a capability is explicitly declared optional.

## Detailed specification

## Goal

Major infrastructure and AI implementations are replaceable without breaking core world behavior or schema meaning.

## Adapter families

```text
AIProviderAdapter
EmbeddingAdapter
MapProjectionAdapter
GazetteerAdapter
RoutingAdapter
MobilityAdapter
LocalNavigationAdapter
PhysicsAdapter
StorageAdapter
EventBusAdapter
SocialPlatformAdapter
EconomyAdapter
WeatherAdapter
AnalyticsAdapter
VisualizationAdapter
AuthenticationAdapter
```

## Contract requirements

Every adapter declares:

- adapter_id and semantic version;
- interface version;
- capabilities;
- configuration schema;
- supported offline/online modes;
- data ownership and persistence behavior;
- timeout/retry semantics;
- deterministic guarantees or lack thereof;
- health/status method;
- error taxonomy;
- resource requirements;
- security/capability permissions;
- licence/provenance metadata;
- compatibility tests.

## Capability negotiation

The core should ask what an adapter can do rather than inspecting vendor names.

Example:

```text
AI capabilities:
- text_generation
- structured_output
- tool_calling
- embeddings
- streaming
- deterministic_seed_support
```

## AI provider boundary

Ollama and OpenRouter implement the same core AI provider interface for relevant capabilities. Agent/runtime code should request functions such as:

```text
propose_intent(...)
rank_options(...)
realize_dialogue(...)
summarize_memories(...)
extract_claims(...)
```

The provider adapter handles API/runtime specifics. Structured outputs are validated before use.

## Spatial adapters

Routing and gazetteer are separate contracts. A place lookup result cannot be assumed traversable without routing/access validation.

## Social platform adapters

Platform adapters define actions, visibility, recommendation/feed behavior, privacy, moderation, and network mechanics. The core information model retains platform-independent claim/message/provenance semantics.

## Plugin lifecycle

```text
discovered -> validated -> enabled -> healthy/degraded -> disabled -> upgraded/rolled back
```

Changing a plugin during a controlled experiment creates explicit configuration/version history.

## Failure rules

- Adapters cannot mutate domain stores outside their granted interface.
- Malformed output fails closed.
- Retries must be idempotent or explicitly correlated.
- Fallbacks are logged.
- No adapter may bypass the simulation constitution.

## Compatibility suite

Each adapter family should ship contract tests that can be run against every implementation. Provider swap is a first-class acceptance test.

## MVP 3 bounded reference

The `awg_mvp3` reference implements the provider-neutral methods above for
Ollama and OpenRouter candidate adapters using an injected transport. The
default runner uses recorded outputs only and performs no network call.

- Model output is an immutable proposal artifact, never a domain event or
  WorldState update.
- Every artifact records adapter, provider, model, prompt-policy, interface,
  output-schema, request, and outcome provenance.
- Timeout, provider error, malformed JSON, schema mismatch, capability
  mismatch, and invalid proposal shape return an explicit rejected result.
- Recorded transports key outputs by request ID and support deterministic
  offline replay.
- The executable contract is
  `contracts/plugins/model-output-artifact.schema.json`.

This reference demonstrates boundary isolation and schema compatibility. It
does not approve either candidate dependency, validate model quality, or
authorize a production provider endpoint.

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
- AWG-PLAT-001
- AWG-PLAT-002
