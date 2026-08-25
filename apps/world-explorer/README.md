# World Explorer (read-only)

Human-reviewable, **read-only** frontend for exploring synthetic district review projections from the Agentic World Graph documentation pack.

This build is **not** authoritative geography, **not** MapLibre/PMTiles world authority, and **not** empirical validation of simulated outcomes.

## Prerequisites

- Node.js 20+
- npm 10+

## Commands

From this directory (`apps/world-explorer`):

```bash
# Install dependencies
npm install

# Development server (serves GET /api/review-bundle from public/api/review-bundle.json)
npm run dev

# Unit tests
npm run test

# Lint
npm run lint

# Production build
npm run build

# Preview production build (includes /api/review-bundle middleware)
npm run preview

# Lint + test + build
npm run check
```

## API contract

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/api/review-bundle` | Returns a read-only JSON review bundle for the current world/scenario projection. |

When the API is unavailable (static hosting, offline review), the client falls back to `src/fixtures/review-bundle.synthetic.json` without mutating simulation state.

The bundled fixture mirrors the MVP 1 synthetic reference district (`world:mvp1-reference-district`).

## UI regions

- **Top bar** — world, scenario, branch, simulation time, run state, projection notices
- **Left rail** — semantic zoom levels and projection layer toggles (clusters/PMTiles labeled projection-only)
- **Center** — SVG synthetic district map with selectable clusters, agents, and buildings
- **Right inspector** — world truth vs agent perspective (clearly separated)
- **Bottom** — timeline scrubber with historical projection badge; collapsible, filterable firehose table
- **Info panels** — information-space and scale summary

## Accessibility

- Keyboard navigation on the map (arrow keys, Escape)
- `prefers-reduced-motion` respected
- Text labels for confidence and cluster kinds (not color-only)
- Responsive layout for narrower viewports

## Non-goals

- No command forms or state mutation controls
- No claims of PMTiles/display cluster authority
- No network writes
