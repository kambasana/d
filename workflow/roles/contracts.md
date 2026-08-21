# Contracts role

Align executable contracts with the implementation:

1. Update versioned JSON Schemas when semantics change.
2. Add at least one valid and one invalid indexed fixture for new contract behavior.
3. Update the schema catalogue and migrations.
4. Preserve historical readability or document explicit rejection.
5. Run `python3 scripts/validate_contracts.py`.

Never weaken a schema merely to make an invalid implementation pass.
