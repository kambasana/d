import type { LoadedReviewBundle } from '../api/types'
import { formatSimulationTime } from '../utils/mapProjection'

interface TopBarProps {
  data: LoadedReviewBundle
  zoomLabel: string
  selectionLabel: string
}

export function TopBar({ data, zoomLabel, selectionLabel }: TopBarProps) {
  const { bundle, meta } = data
  const { world, map_projection: projection } = bundle

  return (
    <div className="top-bar">
      <div className="top-bar__brand">
        <h1 className="top-bar__title">World Explorer</h1>
        <span className="badge badge--read-only" title="Read-only review interface">
          Read-only
        </span>
      </div>
      <dl className="top-bar__context">
        <div>
          <dt>World</dt>
          <dd>{world.world_id}</dd>
        </div>
        <div>
          <dt>Scenario</dt>
          <dd>{world.scenario_id}</dd>
        </div>
        <div>
          <dt>Branch</dt>
          <dd>{world.branch_id}</dd>
        </div>
        <div>
          <dt>Simulation time</dt>
          <dd>
            <time dateTime={world.simulation_time}>{formatSimulationTime(world.simulation_time)}</time>
          </dd>
        </div>
        <div>
          <dt>Run state</dt>
          <dd>
            <span className={`status-pill status-pill--${world.run_state}`}>{world.run_state}</span>
          </dd>
        </div>
        <div>
          <dt>Zoom</dt>
          <dd>{zoomLabel}</dd>
        </div>
        <div>
          <dt>Selection</dt>
          <dd>{selectionLabel}</dd>
        </div>
      </dl>
      <div className="top-bar__meta">
        <p className="projection-notice" role="note">
          {projection.notice}
        </p>
        <p className="data-source" aria-live="polite">
          Data: <strong>{meta.source === 'api' ? 'GET /api/review-bundle' : 'synthetic fixture fallback'}</strong>
          {' · '}
          {world.source_classification}
        </p>
      </div>
    </div>
  )
}
