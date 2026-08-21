# Platform Architecture

Kernel, events, plugins, storage, scaling, APIs, configuration, and deployment.

## Documents

- [AWG-PLAT-001 — System Architecture](system-architecture.md) — Normative; Define the service boundaries and data planes for the world kernel, geospatial systems, agents, information space, scenarios, event history, AI adapters, and projections.
- [AWG-PLAT-002 — Command, Event, Firehose, and Replay Specification](command-event-firehose-and-replay-specification.md) — Normative; Define typed intentions and commands, validation, immutable domain events, causal links, snapshots, replay, branches, subscriptions, and model-call provenance.
- [AWG-PLAT-003 — Plugin and Adapter SDK Compatibility Contracts](plugin-adapter-sdk-and-compatibility-contracts.md) — Normative; Define swappable adapters for AI providers, embeddings, maps, gazetteers, routing, mobility, physics, storage, social platforms, analytics, and visualization.
- [AWG-PLAT-004 — Storage, Indexing, and Projection Architecture](storage-indexing-and-projection-architecture.md) — Normative; Define fit-for-purpose persistence for authoritative state, spatial data, events, analytics, graph projections, search, embeddings, media, and caches.
- [AWG-PLAT-005 — Multi-Resolution Simulation and Scaling Architecture](multi-resolution-simulation-and-scaling-architecture.md) — Normative; Define aggregate, cohort, scheduled, cognitive, and embodied simulation levels independently from visualization levels.
- [AWG-PLAT-006 — Deployment Topologies and Offline Operation](deployment-topologies-and-offline-operation.md) — Normative; Define developer, single-machine offline, LAN, air-gapped, hybrid, distributed, and read-only analyst deployment modes.
- [AWG-PLAT-007 — Simulation Kernel, Scheduler, and Action Execution](simulation-kernel-scheduler-and-action-execution.md) — Normative; Define the deterministic world loop, event calendar, activation rules, command validation, action channels, interruption, completion, and failure semantics.
- [AWG-PLAT-008 — API, Service, and Boundary Contracts](api-service-and-boundary-contracts.md) — Normative; Define public, internal, streaming, administrative, plugin, and data-import interfaces without leaking storage implementation into domain contracts.
- [AWG-PLAT-009 — Configuration, Secrets, and Feature Flags](configuration-secrets-and-feature-flags.md) — Normative; Define configuration layering, secrets isolation, scenario parameters, plugin settings, model routing, feature flags, and reproducible run capture.
- [AWG-PLAT-010 — Identity, Access, Tenancy, and Authorization](identity-access-tenancy-and-authorization.md) — Normative; Define users, service identities, agents, simulation actors, operators, tenants, roles, permissions, and delegation boundaries.
- [AWG-PLAT-011 — World Partitioning, Region Ownership, and Handoff](world-partitioning-region-ownership-and-handoff.md) — Normative; Define spatial partitions, authoritative region ownership, border events, journeys across partitions, rebalance, recovery, and consistency guarantees.

## Reading rule

Read the Simulation Constitution and controlled vocabulary before treating any document in this area as implementation authority.
