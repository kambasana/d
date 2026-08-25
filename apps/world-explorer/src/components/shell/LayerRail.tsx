import type { ReviewBundle, SemanticZoomLevelId } from '../../api/types'

export type LayerState = {
  basemap: boolean
  routes: boolean
  buildings: boolean
  clusters: boolean
  agents: boolean
  pmtiles: boolean
}

interface LayerRailProps {
  bundle: ReviewBundle
  zoomLevel: SemanticZoomLevelId
  onZoomChange: (level: SemanticZoomLevelId) => void
  layers: LayerState
  onToggle: (layer: keyof LayerState) => void
}

/** Layer classes follow AWG-UX-003: base/context, world-state, aggregate. */
export function LayerRail({
  bundle,
  zoomLevel,
  onZoomChange,
  layers,
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
        <h2 className="panel-heading">Base / context</h2>
        <ul className="layer-list">
          <li>
            <label>
              <input type="checkbox" checked={layers.basemap} onChange={() => onToggle('basemap')} />
              District geometry
              <span className="layer-tag">authoritative topology</span>
            </label>
          </li>
          <li>
            <label>
              <input type="checkbox" checked={layers.pmtiles} onChange={() => onToggle('pmtiles')} />
              PMTiles display tiles
              <span className="layer-tag">presentation_only</span>
            </label>
          </li>
        </ul>
      </section>

      <section>
        <h2 className="panel-heading">World-state projections</h2>
        <ul className="layer-list">
          <li>
            <label>
              <input type="checkbox" checked={layers.routes} onChange={() => onToggle('routes')} />
              Routes / journeys
              <span className="layer-tag">authoritative</span>
            </label>
          </li>
          <li>
            <label>
              <input
                type="checkbox"
                checked={layers.buildings}
                onChange={() => onToggle('buildings')}
              />
              Buildings / occupancy
              <span className="layer-tag">authoritative</span>
            </label>
          </li>
          <li>
            <label>
              <input type="checkbox" checked={layers.agents} onChange={() => onToggle('agents')} />
              Individual agents
              <span className="layer-tag">authoritative</span>
            </label>
          </li>
        </ul>
      </section>

      <section>
        <h2 className="panel-heading">Aggregate layers</h2>
        <ul className="layer-list">
          <li>
            <label>
              <input
                type="checkbox"
                checked={layers.clusters}
                onChange={() => onToggle('clusters')}
              />
              Semantic clusters
              <span className="layer-tag">projection_only</span>
            </label>
          </li>
        </ul>
      </section>

      <section className="layer-rail__notice" role="note">
        <p>{bundle.projection_notice}</p>
        <p>{bundle.map_projection.pmtiles_label}</p>
      </section>
    </nav>
  )
}
