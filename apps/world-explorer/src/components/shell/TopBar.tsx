import type { LoadedReviewBundle, WorkspaceId } from '../../api/types'
import { formatSimulationTime } from '../../utils/mapProjection'

interface TopBarProps {
  data: LoadedReviewBundle
  workspace: WorkspaceId
  onWorkspaceChange: (workspace: WorkspaceId) => void
  zoomLabel: string
  selectionLabel: string
  firehoseOpen: boolean
  onToggleFirehose: () => void
}

const WORKSPACES: { id: WorkspaceId; label: string }[] = [
  { id: 'world_explorer', label: 'World Explorer' },
  { id: 'information_space', label: 'Information Space' },
  { id: 'firehose', label: 'Firehose Explorer' },
]

export function TopBar({
  data,
  workspace,
  onWorkspaceChange,
  zoomLabel,
  selectionLabel,
  firehoseOpen,
  onToggleFirehose,
}: TopBarProps) {
  const { bundle, meta } = data
  const { world } = bundle

  return (
    <div className="top-bar">
      <div className="top-bar__brand">
        <p className="top-bar__product">Agentic World Graph</p>
        <h1 className="top-bar__title">World Explorer</h1>
        <span className="badge badge--read-only" title="Read-only review interface">
          Read-only
        </span>
      </div>

      <nav className="workspace-nav" aria-label="Core workspaces">
        {WORKSPACES.map((item) => (
          <button
            key={item.id}
            type="button"
            className={`workspace-nav__button ${workspace === item.id ? 'is-active' : ''}`}
            aria-current={workspace === item.id ? 'page' : undefined}
            onClick={() => onWorkspaceChange(item.id)}
          >
            {item.label}
          </button>
        ))}
      </nav>

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

      <div className="top-bar__actions">
        {workspace === 'world_explorer' ? (
          <button
            type="button"
            className="ghost-button"
            aria-pressed={firehoseOpen}
            onClick={onToggleFirehose}
          >
            {firehoseOpen ? 'Hide firehose panel' : 'Show firehose panel'}
          </button>
        ) : null}
        <p className="data-source" aria-live="polite">
          Source:{' '}
          <strong>
            {meta.source === 'api' ? 'GET /api/review-bundle' : 'synthetic fixture fallback'}
          </strong>
        </p>
      </div>
    </div>
  )
}
