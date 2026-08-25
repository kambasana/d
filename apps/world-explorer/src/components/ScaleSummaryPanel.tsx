import type { ScaleSummary, SemanticZoomLevelId } from '../api/types'

interface ScaleSummaryPanelProps {
  summary: ScaleSummary
  zoomLevel: SemanticZoomLevelId
}

export function ScaleSummaryPanel({ summary, zoomLevel }: ScaleSummaryPanelProps) {
  return (
    <section className="scale-panel" aria-label="Scale summary">
      <h2 className="panel-heading">Scale summary</h2>
      <dl className="scale-panel__stats">
        <div>
          <dt>Zoom level</dt>
          <dd>{zoomLevel}</dd>
        </div>
        <div>
          <dt>Visible population</dt>
          <dd>
            {summary.population_visible} / {summary.population_total}
          </dd>
        </div>
        <div>
          <dt>Clusters</dt>
          <dd>{summary.cluster_count}</dd>
        </div>
        <div>
          <dt>Buildings</dt>
          <dd>{summary.building_count}</dd>
        </div>
        <div>
          <dt>Active journeys</dt>
          <dd>{summary.active_journeys}</dd>
        </div>
        <div>
          <dt>Density note</dt>
          <dd>{summary.projection_density}</dd>
        </div>
      </dl>
    </section>
  )
}
