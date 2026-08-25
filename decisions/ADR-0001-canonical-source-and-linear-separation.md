# ADR-0001: Canonical repository and Linear separation

## Status

Accepted for the v0.2.0 baseline.

## Context

The project needs complete specifications and executable contracts without manually duplicating 74 documents into Linear.

## Decision

The disk or future Git repository is the canonical source of specifications, registers, schemas, examples, tests, and releases. Linear tracks milestones, ownership, review, dependencies, and delivery status.

## Consequences

Linear issues must link to canonical paths and document IDs. A Linear status cannot override failed repository validation. Generated ZIPs are immutable release projections.
