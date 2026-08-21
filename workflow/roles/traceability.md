# Traceability role

Before implementation:

1. Identify affected document, requirement, test, risk, assumption, data-source, component, schema, and ADR IDs.
2. Add stable requirement and acceptance-test mappings for every new normative rule.
3. Confirm all dependencies lead back to the Constitution.
4. Run `python3 scripts/validate_traceability.py`.

Do not mark the step complete if a rule has no test, a test has no requirement, or a licensing/security decision is being assumed.
