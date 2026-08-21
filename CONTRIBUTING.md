# Contributing

All changes follow a specification-first workflow.

1. Read `AGENTS.md` and the Simulation Constitution.
2. Work from a Linear issue or documented local work item.
3. Use stable document, requirement, test, schema, and ADR identifiers.
4. Update authored specifications before generated reports.
5. Add or update machine-readable contracts and fixtures when behaviour changes.
6. Run the full validator and test suite (`make validate` and `make test`).
7. Describe compatibility, security, offline, performance, data, licensing, and migration effects in the pull request.

Direct edits to `generated/` and `dist/` are rejected by validation.
