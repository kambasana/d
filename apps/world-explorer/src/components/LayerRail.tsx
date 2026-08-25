import type { ReviewBundle, SemanticZoomLevelId } from '../api/types'

interface LayerRailProps {
  bundle: ReviewBundle
  zoomLevel: SemanticZoomLevelId
  onZoomChange: (level: SemanticZoomLevelId) => void
  showClusters: boolean
  showAgents: boolean
  showBuildings: boolean
  showRoutes: boolean
  showPmtilesNotice: boolean
  onToggle: (layer: 'clusters' | 'agents' | 'buildings' | 'routes' | 'pmtiles') => void
}

export function LayerRail({
  bundle,
  zoomLevel,
  onZoomChange,
  showClusters,
  showAgents,
  showBuildings,
  showRoutes,
  showPmtilesNotice,
  onToggle,
}: LayerRailProps) {
  return (
    <nav className="layer-rail" aria-label="Map layers and semantic zoom">
      <section>
        <h2 className="panel-heading">Semantic zoom</h2>
        <div className="zoom-levels" role="radiogroup" aria-label="Semantic zoom level">
          {bundle.semantic_zoom.levels.map((level) => (
            <label key={level.id} className="zoom-level">
              <input
                type="radio"
                name="semantic-zoom"
                value={level.id}
                checked={zoomLevel === level.id}
                onChange={() => onZoomChange(level.id)}
              />
              <span className="zoom-level__label">{level.label}</span>
              <span className="zoom-level__desc">{level.description}</span>
            </label>
          ))}
        </div>
      </section>

      <section>
        <h2 className="panel-heading">Projection layers</h2>
        <ul className="layer-list">
          <li>
            <label>
              <input
                type="checkbox"
                checked={showClusters}
                onChange={() => onToggle('clusters')}
              />
              Clusters <span className="layer-tag">projection-only</span>
            </label>
          </li>
          <li>
            <label>
              <input type="checkbox" checked={showAgents} onChange={() => onToggle('agents')} />
              Agents
            </label>
          </li>
          <li>
            <label>
              <input
                type="checkbox"
                checked={showBuildings}
                onChange={() => onToggle('buildings')}
              />
              Buildings
            </label>
          </li>
          <li>
            <label>
              <input type="checkbox" checked={showRoutes} onChange={() => onToggle('routes')} />
              Route graph
            </label>
          </li>
          <li>
            <label>
              <input
                type="checkbox"
                checked={showPmtilesNotice}
                onChange={() => onToggle('pmtiles')}
              />
              PMTiles display overlay <span className="layer-tag">projection-only</span>
            </label>
          </li>
        </ul>
      </section>

      <section className="layer-rail__notice">
        <p role="note">{bundle.projection_notice}</p>
        {bundle.map_projection.pmtiles_available ? (
          <p className="pmtiles-label">{bundle.map_projection.pmtiles_label}</p>
        ) : null}
      </section>
    </nav>
  )
}
