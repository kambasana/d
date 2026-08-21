# Verification role

Run evidence in increasing scope:

1. Targeted unit, invariant, and contract tests.
2. Integration and deterministic replay tests.
3. Offline, security, failure, and performance checks required by the stage.
4. The stage runner.
5. `make validate`.
6. `make test`.

Record failures without hiding them. A failed invariant blocks closeout. Regenerate reports through scripts; never edit `generated/` by hand.
