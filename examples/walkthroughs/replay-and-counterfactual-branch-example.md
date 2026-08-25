# Replay and Counterfactual Branch Example

Baseline and Branch B share immutable history through event 50,000.

At event 50,001:

- Baseline continues normally.
- Branch B applies a bridge-closure intervention.

Recorded LLM outputs before the branch are reused when replaying history. New post-branch model calls receive Branch B provenance. Comparison reports travel delays, information reach, missed appointments, and organization effects with seed/model sensitivity notes.
