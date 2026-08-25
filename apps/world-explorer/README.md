# World Explorer

Human-reviewable, read-only HTTP projection service for the Agentic World Graph MVP reference kernels.

## Purpose

The World Explorer serves deterministic read projections derived from:

- **MVP 1** — spatial movement, semantic clusters, building occupancy, and firehose events
- **MVP 4** — information-world claims, exposure, beliefs, and social actions
- **MVP 5** — multi-resolution population records, active cognition, and branch comparison

This is a review and inspection surface, not a production application. It does not mutate authoritative kernel state, does not require a database, and operates fully offline.

## Run

```bash
make world-explorer
```

Or directly:

```bash
PYTHONPATH=. python3 scripts/run_world_explorer.py --host 127.0.0.1 --port 8765
```

Print bundle context without starting the server:

```bash
PYTHONPATH=. python3 scripts/run_world_explorer.py --print-context
```

## API (GET only)

| Endpoint | Description |
|----------|-------------|
| `GET /health` | Service health |
| `GET /api/v1/context` | Bundle metadata, preserved invariants, offline status |
| `GET /api/v1/status` | Checksums and event counts |
| `GET /api/v1/world?simulation_time=...&zoom=...&building_id=...` | Agents, clusters, optional building occupancy |
| `GET /api/v1/firehose?from_sequence=...&limit=...&world_id=...` | Combined timeline/firehose page |
| `GET /api/v1/timeline` | Timeline markers and event totals |
| `GET /api/v1/information?mode=participant\|analyst&agent_id=...` | Information summary |
| `GET /api/v1/scale` | Scale and branch-comparison summary |

`POST`, `PUT`, `PATCH`, and `DELETE` return **405 Method Not Allowed**.

## Static frontend

If a built frontend exists under `apps/world-explorer/dist`, it is served for non-API routes. PMTiles and map tiles remain presentation-only and are not authoritative geography (INV-016).

## Preserved invariants

- **INV-001** — no direct mutation of authoritative state via HTTP
- **INV-006** — world truth and agent belief remain separate in information projections
- **INV-007** — likes are not treated as belief
- **INV-011** — clusters are display projections; authoritative agent state is unchanged
- **INV-016** — PMTiles are presentation-only

## Contracts

Executable JSON Schemas live under `contracts/projections/` with valid fixtures in `examples/fixtures/projections/`.
