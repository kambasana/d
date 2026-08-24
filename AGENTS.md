# AGENTS.md

## Cursor Cloud specific instructions

This repository ships the project as a single archive, `agentic-world-graph-v0.2.0.zip`,
at the repo root. The actual project (a Python documentation/contracts validation pack
named `agentic-world-graph-docpack`) lives inside that archive.

- The Cloud Agent update script extracts the archive to `./agentic-world-graph/` (only
  when it is not already extracted) and installs the Python dev dependencies. Run all
  project commands from inside `agentic-world-graph/`.
- The extracted `agentic-world-graph/` directory is not tracked on `main`; edits made
  there are outside git history. Unzipping is idempotent: re-running the update script
  will not overwrite an already-extracted tree, so local edits survive re-runs.
- Python 3.12 with pip user installs (`~/.local`) is used; there is no virtualenv.
  Plain `python3` and `pytest` pick up the installed packages, so no activation is needed.
- There are no services, databases, network calls, or secrets. `docker-compose.yml`
  even runs with `network_mode: none`; the whole pack validates fully offline.

### Common commands (run from `agentic-world-graph/`)

- Regenerate `generated/` reports: `python3 scripts/build_generated.py` (or `make generate`)
- Primary validation ("run" the product): `python3 scripts/validate_all.py` (or `make validate`)
- Tests: `python3 -m pytest -q` (or `make test`)
- Build/audit release archives into `dist/`: `python3 scripts/build_release.py` (or `make release`)
- Docs site (optional UI): `python3 -m mkdocs serve -a 127.0.0.1:8000` (build with `mkdocs build`)

### Notes

- No linter is configured (only `.editorconfig`); there is no lint command to run.
- `scripts/validate_all.py` regenerates reports and validates structure, traceability,
  JSON Schemas/fixtures, and internal links. It is the authoritative check and mirrors CI
  (`.github/workflows/documentation-quality.yml`).
- Never hand-edit files under `generated/`; regenerate them with `build_generated.py`.
