# ADR-0003: Semantic world graph over fit-for-purpose stores

## Status

Accepted for the v0.2.0 baseline.

## Decision

The world graph is a semantic domain model and API, not a mandate to store every workload in one graph database.

## Consequences

Spatial truth may use PostGIS, events append-only storage, transactions relational tables, analytics columnar storage, relationships graph projections, and retrieval indexes. Authority and provenance remain explicit across stores.
