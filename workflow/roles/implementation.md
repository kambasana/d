# Implementation role

Implement the smallest vertical slice that satisfies the current stage's accepted requirements.

- The deterministic kernel remains authoritative.
- Models, plugins, projections, and UI never write world state directly.
- Use typed commands, validated transitions, append-only events, deterministic fallback, and explicit provenance.
- Preserve earlier MVP functionality and tests.
- Do not adopt an unapproved dependency or external dataset.

Run the stage runner before handing work to contracts and verification.
