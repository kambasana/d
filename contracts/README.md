# Machine-Readable Contracts

These JSON Schemas are the executable boundary corresponding to the normative Markdown specifications. They are versioned, validated, and exercised by valid and invalid fixtures.

A schema validates structural admissibility. World-specific feasibility such as route reachability, ownership, capacity, elapsed time, knowledge access, or causal consistency remains the responsibility of deterministic validators and invariant tests.

Breaking schema changes require migration guidance and an ADR.

## Engine ownership

Core simulation engines own the contract groups listed in AWG-PLAT-001. Command, event, agent, world-entity, claim, social, scenario, firehose, and plugin families MUST remain validatable without calling an AI provider.
