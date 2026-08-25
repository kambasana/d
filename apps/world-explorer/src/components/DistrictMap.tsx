import { useCallback, useEffect, useId, useMemo, useRef, useState, type KeyboardEvent } from 'react'
import type { ReviewBundle, Selection, SemanticZoomLevelId } from '../api/types'
import { clusterKindLabel, projectLonLat } from '../utils/mapProjection'
import { visibleAgents, visibleClusters } from '../hooks/useFirehoseFilters'

interface DistrictMapProps {
  bundle: ReviewBundle
  zoomLevel: SemanticZoomLevelId
  selection: Selection
  onSelect: (selection: Selection) => void
  showClusters: boolean
  showAgents: boolean
  showBuildings: boolean
  showRoutes: boolean
  showPmtilesNotice: boolean
}

type FocusableItem =
  | { kind: 'cluster'; id: string }
  | { kind: 'agent'; id: string }
  | { kind: 'building'; id: string }

export function DistrictMap({
  bundle,
  zoomLevel,
  selection,
  onSelect,
  showClusters,
  showAgents,
  showBuildings,
  showRoutes,
  showPmtilesNotice,
}: DistrictMapProps) {
  const svgRef = useRef<SVGSVGElement>(null)
  const [size, setSize] = useState({ width: 800, height: 520 })
  const titleId = useId()
  const descId = useId()

  const clusters = useMemo(
    () => (showClusters ? visibleClusters(bundle, zoomLevel) : []),
    [bundle, showClusters, zoomLevel],
  )
  const agents = useMemo(
    () => (showAgents ? visibleAgents(bundle, zoomLevel) : []),
    [bundle, showAgents, zoomLevel],
  )
  const buildings = useMemo(
    () => (showBuildings ? bundle.district.buildings : []),
    [bundle, showBuildings],
  )

  const focusables = useMemo<FocusableItem[]>(() => {
    const items: FocusableItem[] = []
    clusters.forEach((c) => items.push({ kind: 'cluster', id: c.cluster_id }))
    agents.forEach((a) => items.push({ kind: 'agent', id: a.agent_id }))
    if (zoomLevel !== 'district') {
      buildings.forEach((b) => items.push({ kind: 'building', id: b.building_id }))
    }
    return items
  }, [agents, buildings, clusters, zoomLevel])

  const [focusIndex, setFocusIndex] = useState(0)

  useEffect(() => {
    const node = svgRef.current?.parentElement
    if (!node) return
    const observer = new ResizeObserver((entries) => {
      const entry = entries[0]
      if (!entry) return
      setSize({ width: entry.contentRect.width, height: entry.contentRect.height })
    })
    observer.observe(node)
    return () => observer.disconnect()
  }, [])

  const project = useCallback(
    (lon: number, lat: number) => projectLonLat(lon, lat, bundle.district, size.width, size.height),
    [bundle.district, size.height, size.width],
  )

  const nodePositions = useMemo(() => {
    const map = new Map<string, { x: number; y: number }>()
    bundle.district.nodes.forEach((node) => {
      map.set(node.node_id, project(node.longitude, node.latitude))
    })
    return map
  }, [bundle.district.nodes, project])

  const handleKeyDown = (event: KeyboardEvent<HTMLDivElement>) => {
    if (!focusables.length) return
    if (event.key === 'ArrowRight' || event.key === 'ArrowDown') {
      event.preventDefault()
      const next = (focusIndex + 1) % focusables.length
      setFocusIndex(next)
      onSelect({ kind: focusables[next].kind, id: focusables[next].id })
    }
    if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') {
      event.preventDefault()
      const next = (focusIndex - 1 + focusables.length) % focusables.length
      setFocusIndex(next)
      onSelect({ kind: focusables[next].kind, id: focusables[next].id })
    }
    if (event.key === 'Escape') {
      onSelect(null)
    }
  }

  const isSelected = (kind: NonNullable<Selection>['kind'], id: string) =>
    selection?.kind === kind && selection.id === id

  return (
    <div className="district-map" tabIndex={0} onKeyDown={handleKeyDown} aria-label="District map">
      <div className="district-map__header">
        <h2 className="panel-heading">Synthetic district map</h2>
        <p className="district-map__subtitle">
          SVG projection for human review — not MapLibre/PMTiles authority
        </p>
      </div>
      <svg
        ref={svgRef}
        className="district-map__svg"
        width={size.width}
        height={size.height}
        role="img"
        aria-labelledby={titleId}
        aria-describedby={descId}
      >
        <title id={titleId}>Synthetic reference district map projection</title>
        <desc id={descId}>
          Read-only visualization of routes, projection-only clusters, agents, and buildings.
          Clusters are screen-space aggregations and do not change authoritative positions.
        </desc>

        {showPmtilesNotice ? (
          <g aria-hidden="true">
            <rect
              x={8}
              y={8}
              width={size.width - 16}
              height={size.height - 16}
              className="map-pmtiles-overlay"
              rx={8}
            />
            <text x={20} y={28} className="map-pmtiles-label">
              PMTiles display tile (projection-only)
            </text>
          </g>
        ) : null}

        <rect className="map-background" width={size.width} height={size.height} />

        {showRoutes
          ? bundle.district.edges.map((edge) => {
              const source = nodePositions.get(edge.source)
              const target = nodePositions.get(edge.target)
              if (!source || !target) return null
              return (
                <line
                  key={edge.edge_id}
                  x1={source.x}
                  y1={source.y}
                  x2={target.x}
                  y2={target.y}
                  className={edge.accessible ? 'map-edge' : 'map-edge map-edge--closed'}
                  aria-hidden="true"
                />
              )
            })
          : null}

        {buildings.map((building) => {
          const node = bundle.district.nodes.find((n) => n.node_id === building.route_node_id)
          if (!node) return null
          const { x, y } = project(node.longitude, node.latitude)
          const selected = isSelected('building', building.building_id)
          return (
            <g
              key={building.building_id}
              className={`map-building ${selected ? 'map-building--selected' : ''}`}
              transform={`translate(${x}, ${y})`}
              role="button"
              tabIndex={-1}
              aria-label={`${building.name}, occupancy ${building.occupancy} of ${building.capacity}`}
              onClick={() => onSelect({ kind: 'building', id: building.building_id })}
            >
              <rect x={-14} y={-14} width={28} height={28} rx={4} />
              <text y={4} textAnchor="middle" className="map-building__label">
                B
              </text>
            </g>
          )
        })}

        {clusters.map((cluster) => {
          const { x, y } = project(cluster.centroid.longitude, cluster.centroid.latitude)
          const selected = isSelected('cluster', cluster.cluster_id)
          const radius = 18 + Math.min(cluster.count, 20)
          return (
            <g
              key={cluster.cluster_id}
              className={`map-cluster map-cluster--${cluster.kind} ${selected ? 'map-cluster--selected' : ''}`}
              transform={`translate(${x}, ${y})`}
              role="button"
              tabIndex={-1}
              aria-label={`${clusterKindLabel(cluster.kind)}: ${cluster.label}, count ${cluster.count}. Projection only.`}
              onClick={() => onSelect({ kind: 'cluster', id: cluster.cluster_id })}
            >
              <circle r={radius} />
              <text y={5} textAnchor="middle" className="map-cluster__count">
                {cluster.count}
              </text>
            </g>
          )
        })}

        {agents.map((agent) => {
          const { x, y } = project(agent.longitude, agent.latitude)
          const selected = isSelected('agent', agent.agent_id)
          return (
            <g
              key={agent.agent_id}
              className={`map-agent ${selected ? 'map-agent--selected' : ''}`}
              transform={`translate(${x}, ${y})`}
              role="button"
              tabIndex={-1}
              aria-label={`Agent ${agent.display_name}, status ${agent.status}`}
              onClick={() => onSelect({ kind: 'agent', id: agent.agent_id })}
            >
              <circle r={7} />
              <text y={-10} textAnchor="middle" className="map-agent__label">
                {agent.display_name}
              </text>
            </g>
          )
        })}
      </svg>
      <p className="district-map__footer" role="note">
        Use arrow keys to move selection, Enter to focus inspector, Escape to clear. Cluster markers
        are projection-only and never relocate agents.
      </p>
    </div>
  )
}
