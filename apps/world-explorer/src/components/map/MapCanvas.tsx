import { useEffect, useMemo, useRef } from 'react'
import {
  Map as MapLibreMap,
  NavigationControl,
  addProtocol,
  type GeoJSONSource,
  type MapLayerMouseEvent,
} from 'maplibre-gl'
import { Protocol } from 'pmtiles'
import type { FeatureCollection } from 'geojson'
import type { LayerState } from '../shell/LayerRail'
import type { DistrictNode, ReviewBundle, Selection, SemanticZoomLevelId } from '../../api/types'
import { visibleAgents, visibleClusters } from '../../hooks/useFirehoseFilters'
import { clusterKindLabel } from '../../utils/mapProjection'
import 'maplibre-gl/dist/maplibre-gl.css'

interface MapCanvasProps {
  bundle: ReviewBundle
  zoomLevel: SemanticZoomLevelId
  selection: Selection
  onSelect: (selection: Selection) => void
  layers: LayerState
}

let pmtilesRegistered = false

function ensurePmtilesProtocol(): void {
  if (pmtilesRegistered) return
  const protocol = new Protocol()
  addProtocol('pmtiles', protocol.tile)
  pmtilesRegistered = true
}

function nodesById(bundle: ReviewBundle): Record<string, DistrictNode> {
  const lookup: Record<string, DistrictNode> = {}
  for (const node of bundle.district.nodes) {
    lookup[node.node_id] = node
  }
  return lookup
}

function emptyCollection(): FeatureCollection {
  return { type: 'FeatureCollection', features: [] }
}

function districtBoundary(bundle: ReviewBundle): FeatureCollection {
  const { min_lon, max_lon, min_lat, max_lat } = bundle.district.bounds
  return {
    type: 'FeatureCollection',
    features: [
      {
        type: 'Feature',
        properties: { id: 'district-bounds', class: 'base' },
        geometry: {
          type: 'Polygon',
          coordinates: [
            [
              [min_lon, min_lat],
              [max_lon, min_lat],
              [max_lon, max_lat],
              [min_lon, max_lat],
              [min_lon, min_lat],
            ],
          ],
        },
      },
    ],
  }
}

function routesCollection(bundle: ReviewBundle): FeatureCollection {
  const byId = nodesById(bundle)
  return {
    type: 'FeatureCollection',
    features: bundle.district.edges.flatMap((edge) => {
      const source = byId[edge.source]
      const target = byId[edge.target]
      if (!source || !target) return []
      return [
        {
          type: 'Feature' as const,
          properties: {
            id: edge.edge_id,
            accessible: edge.accessible,
          },
          geometry: {
            type: 'LineString' as const,
            coordinates: [
              [source.longitude, source.latitude],
              [target.longitude, target.latitude],
            ],
          },
        },
      ]
    }),
  }
}

function buildingsCollection(bundle: ReviewBundle): FeatureCollection {
  const byId = nodesById(bundle)
  const delta = 0.00035
  return {
    type: 'FeatureCollection',
    features: bundle.district.buildings.flatMap((building) => {
      const node = byId[building.route_node_id]
      if (!node) return []
      const lon = node.longitude
      const lat = node.latitude
      return [
        {
          type: 'Feature' as const,
          properties: {
            id: building.building_id,
            name: building.name,
            occupancy: building.occupancy,
            capacity: building.capacity,
          },
          geometry: {
            type: 'Polygon' as const,
            coordinates: [
              [
                [lon - delta, lat - delta],
                [lon + delta, lat - delta],
                [lon + delta, lat + delta],
                [lon - delta, lat + delta],
                [lon - delta, lat - delta],
              ],
            ],
          },
        },
      ]
    }),
  }
}

function agentsCollection(
  bundle: ReviewBundle,
  zoomLevel: SemanticZoomLevelId,
): FeatureCollection {
  return {
    type: 'FeatureCollection',
    features: visibleAgents(bundle, zoomLevel).map((agent) => ({
      type: 'Feature' as const,
      properties: {
        id: agent.agent_id,
        name: agent.display_name,
        status: agent.status,
      },
      geometry: {
        type: 'Point' as const,
        coordinates: [agent.longitude, agent.latitude],
      },
    })),
  }
}

function clustersCollection(
  bundle: ReviewBundle,
  zoomLevel: SemanticZoomLevelId,
): FeatureCollection {
  return {
    type: 'FeatureCollection',
    features: visibleClusters(bundle, zoomLevel).map((cluster) => ({
      type: 'Feature' as const,
      properties: {
        id: cluster.cluster_id,
        label: cluster.label,
        count: cluster.count,
        kind: cluster.kind,
        radius: Math.max(14, Math.min(40, 10 + cluster.count * 2)),
      },
      geometry: {
        type: 'Point' as const,
        coordinates: [cluster.centroid.longitude, cluster.centroid.latitude],
      },
    })),
  }
}

function centerOf(bundle: ReviewBundle): [number, number] {
  const { min_lon, max_lon, min_lat, max_lat } = bundle.district.bounds
  return [(min_lon + max_lon) / 2, (min_lat + max_lat) / 2]
}

/** AWG-UX-007 MapLibre operational map; PMTiles are presentation_only. */
export function MapCanvas({
  bundle,
  zoomLevel,
  selection,
  onSelect,
  layers,
}: MapCanvasProps) {
  const containerRef = useRef<HTMLDivElement | null>(null)
  const mapRef = useRef<MapLibreMap | null>(null)
  const onSelectRef = useRef(onSelect)

  useEffect(() => {
    onSelectRef.current = onSelect
  }, [onSelect])

  const listItems = useMemo(() => {
    const items: { kind: NonNullable<Selection>['kind']; id: string; label: string }[] = []
    for (const cluster of visibleClusters(bundle, zoomLevel)) {
      items.push({
        kind: 'cluster',
        id: cluster.cluster_id,
        label: `${clusterKindLabel(cluster.kind)}: ${cluster.label}`,
      })
    }
    for (const agent of visibleAgents(bundle, zoomLevel)) {
      items.push({
        kind: 'agent',
        id: agent.agent_id,
        label: `Agent ${agent.display_name}`,
      })
    }
    if (zoomLevel !== 'district') {
      for (const building of bundle.district.buildings) {
        items.push({
          kind: 'building',
          id: building.building_id,
          label: `${building.name} (${building.occupancy}/${building.capacity})`,
        })
      }
    }
    return items
  }, [bundle, zoomLevel])

  useEffect(() => {
    if (!containerRef.current || mapRef.current) return
    ensurePmtilesProtocol()

    const [lon, lat] = centerOf(bundle)
    const map = new MapLibreMap({
      container: containerRef.current,
      style: {
        version: 8,
        sources: {},
        layers: [
          {
            id: 'background',
            type: 'background',
            paint: { 'background-color': '#d5e0ec' },
          },
        ],
      },
      center: [lon, lat],
      zoom: 14.2,
      attributionControl: { compact: true },
    })

    map.addControl(new NavigationControl({ showCompass: false }), 'top-right')

    map.on('load', () => {
      map.addSource('district-bounds', { type: 'geojson', data: emptyCollection() })
      map.addSource('routes', { type: 'geojson', data: emptyCollection() })
      map.addSource('buildings', { type: 'geojson', data: emptyCollection() })
      map.addSource('clusters', { type: 'geojson', data: emptyCollection() })
      map.addSource('agents', { type: 'geojson', data: emptyCollection() })

      map.addLayer({
        id: 'district-fill',
        type: 'fill',
        source: 'district-bounds',
        paint: {
          'fill-color': '#b9c9b4',
          'fill-opacity': 0.35,
        },
      })
      map.addLayer({
        id: 'district-outline',
        type: 'line',
        source: 'district-bounds',
        paint: {
          'line-color': '#5d7386',
          'line-width': 1.5,
        },
      })
      map.addLayer({
        id: 'routes-line',
        type: 'line',
        source: 'routes',
        paint: {
          'line-color': [
            'case',
            ['==', ['get', 'accessible'], false],
            '#b42318',
            '#4a6f8f',
          ],
          'line-width': 3.5,
          'line-dasharray': [
            'case',
            ['==', ['get', 'accessible'], false],
            ['literal', [1.2, 1.2]],
            ['literal', [1, 0]],
          ],
        },
      })
      map.addLayer({
        id: 'buildings-fill',
        type: 'fill',
        source: 'buildings',
        paint: {
          'fill-color': '#8fa6b8',
          'fill-opacity': 0.7,
          'fill-outline-color': '#44586a',
        },
      })
      map.addLayer({
        id: 'clusters-circle',
        type: 'circle',
        source: 'clusters',
        paint: {
          'circle-radius': ['get', 'radius'],
          'circle-color': '#c45c26',
          'circle-opacity': 0.38,
          'circle-stroke-color': '#8a3d14',
          'circle-stroke-width': 1.5,
        },
      })
      map.addLayer({
        id: 'agents-circle',
        type: 'circle',
        source: 'agents',
        paint: {
          'circle-radius': 7,
          'circle-color': '#1f6feb',
          'circle-stroke-color': '#ffffff',
          'circle-stroke-width': 2,
        },
      })

      try {
        map.addSource('pmtiles-base', {
          type: 'raster',
          url: 'pmtiles:///assets/reference-district.pmtiles',
          tileSize: 256,
        })
        map.addLayer(
          {
            id: 'pmtiles-raster',
            type: 'raster',
            source: 'pmtiles-base',
            paint: { 'raster-opacity': 0.45 },
            layout: { visibility: 'none' },
          },
          'district-fill',
        )
      } catch {
        // Presentation archive is optional when unavailable.
      }

      const pick = (event: MapLayerMouseEvent, kind: NonNullable<Selection>['kind']) => {
        const id = event.features?.[0]?.properties?.id
        if (typeof id === 'string') {
          onSelectRef.current({ kind, id })
        }
      }

      map.on('click', 'buildings-fill', (event: MapLayerMouseEvent) =>
        pick(event, 'building'),
      )
      map.on('click', 'agents-circle', (event: MapLayerMouseEvent) => pick(event, 'agent'))
      map.on('click', 'clusters-circle', (event: MapLayerMouseEvent) =>
        pick(event, 'cluster'),
      )
      map.on('click', (event: MapLayerMouseEvent) => {
        const hits = map.queryRenderedFeatures(event.point, {
          layers: ['agents-circle', 'clusters-circle', 'buildings-fill'],
        })
        if (hits.length === 0) onSelectRef.current(null)
      })
    })

    mapRef.current = map
    return () => {
      map.remove()
      mapRef.current = null
    }
  }, [bundle])

  useEffect(() => {
    const map = mapRef.current
    if (!map?.isStyleLoaded()) return

    const setData = (sourceId: string, data: FeatureCollection) => {
      const source = map.getSource(sourceId) as GeoJSONSource | undefined
      source?.setData(data)
    }

    setData(
      'district-bounds',
      layers.basemap ? districtBoundary(bundle) : emptyCollection(),
    )
    setData('routes', layers.routes ? routesCollection(bundle) : emptyCollection())
    setData('buildings', layers.buildings ? buildingsCollection(bundle) : emptyCollection())
    setData(
      'clusters',
      layers.clusters ? clustersCollection(bundle, zoomLevel) : emptyCollection(),
    )
    setData('agents', layers.agents ? agentsCollection(bundle, zoomLevel) : emptyCollection())

    const visibility = (on: boolean) => (on ? 'visible' : 'none')
    for (const [layerId, on] of [
      ['district-fill', layers.basemap],
      ['district-outline', layers.basemap],
      ['routes-line', layers.routes],
      ['buildings-fill', layers.buildings],
      ['clusters-circle', layers.clusters],
      ['agents-circle', layers.agents],
      ['pmtiles-raster', layers.pmtiles],
    ] as const) {
      if (map.getLayer(layerId)) {
        map.setLayoutProperty(layerId, 'visibility', visibility(on))
      }
    }
  }, [bundle, layers, zoomLevel])

  useEffect(() => {
    const map = mapRef.current
    if (!map || !selection) return
    let lon: number | null = null
    let lat: number | null = null
    if (selection.kind === 'agent') {
      const agent = bundle.agents.find((item) => item.agent_id === selection.id)
      if (agent) {
        lon = agent.longitude
        lat = agent.latitude
      }
    } else if (selection.kind === 'building') {
      const building = bundle.district.buildings.find(
        (item) => item.building_id === selection.id,
      )
      const node = bundle.district.nodes.find(
        (item) => item.node_id === building?.route_node_id,
      )
      if (node) {
        lon = node.longitude
        lat = node.latitude
      }
    } else if (selection.kind === 'cluster') {
      const cluster = bundle.clusters.find((item) => item.cluster_id === selection.id)
      if (cluster) {
        lon = cluster.centroid.longitude
        lat = cluster.centroid.latitude
      }
    }
    if (lon !== null && lat !== null) {
      map.easeTo({ center: [lon, lat], duration: 450 })
    }
  }, [selection, bundle])

  return (
    <div className="map-canvas">
      <div className="map-canvas__banner" role="note">
        MapLibre operational map · PMTiles presentation_only · clusters projection_only · not
        geography authority
      </div>
      <div
        ref={containerRef}
        className="map-canvas__viewport"
        data-testid="map-canvas"
        role="application"
        aria-label="World Explorer operational map"
      />
      <div className="map-canvas__legend" aria-label="Layer truth legend">
        <span className="legend-item legend-item--truth">Routes / agents / occupancy: world-state</span>
        <span className="legend-item legend-item--projection">Clusters: projection_only</span>
        <span className="legend-item legend-item--pmtiles">PMTiles: presentation_only</span>
      </div>
      <ul className="map-canvas__list-alt" aria-label="List alternative to map selection">
        {listItems.length === 0 ? (
          <li>
            <span>No selectable entities at this semantic zoom. Switch to Street or Building.</span>
          </li>
        ) : (
          listItems.map((item) => (
            <li key={`${item.kind}:${item.id}`}>
              <button
                type="button"
                aria-pressed={selection?.kind === item.kind && selection.id === item.id}
                aria-label={item.label}
                onClick={() => onSelect({ kind: item.kind, id: item.id })}
              >
                {item.label}
              </button>
            </li>
          ))
        )}
      </ul>
    </div>
  )
}
