# ADR-0002: Deterministic kernel authority

## Status

Accepted for the v0.2.0 baseline.

## Decision

AI models may propose bounded intentions, rankings, interpretations, summaries, and language. Only validated deterministic systems may create authoritative state transitions and domain events.

## Consequences

Model output is untrusted input. Direct model database writes and narrator-declared success are prohibited. Recorded model outputs may be replayed without inference.
