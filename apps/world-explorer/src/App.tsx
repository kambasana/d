import { useMemo, useState } from 'react'
import { AppShell } from './components/AppShell'
import { DistrictMap } from './components/DistrictMap'
import { FirehosePanel } from './components/FirehosePanel'
import { InformationSpacePanel } from './components/InformationSpacePanel'
import { Inspector } from './components/Inspector'
import { LayerRail } from './components/LayerRail'
import { ScaleSummaryPanel } from './components/ScaleSummaryPanel'
import { TimelineScrubber } from './components/TimelineScrubber'
import { TopBar } from './components/TopBar'
import { useReviewBundle } from './hooks/useReviewBundle'
import type { Selection, SemanticZoomLevelId } from './api/types'
import './App.css'

function App() {
  const loadState = useReviewBundle()
  const [zoomLevel, setZoomLevel] = useState<SemanticZoomLevelId>('district')
  const [selection, setSelection] = useState<Selection>(null)
  const [tickIndex, setTickIndex] = useState(4)
  const [layers, setLayers] = useState({
    clusters: true,
    agents: true,
    buildings: true,
    routes: true,
    pmtiles: false,
  })

  const selectionLabel = useMemo(() => {
    if (!selection) return 'None'
    return `${selection.kind}: ${selection.id}`
  }, [selection])

  const zoomLabel = useMemo(() => {
    if (loadState.status !== 'ready') return '—'
    const level = loadState.data.bundle.semantic_zoom.levels.find((l) => l.id === zoomLevel)
    return level?.label ?? zoomLevel
  }, [loadState, zoomLevel])

  if (loadState.status === 'loading') {
    return (
      <div className="app-loading" role="status" aria-live="polite">
        Loading review bundle…
      </div>
    )
  }

  if (loadState.status === 'error') {
    return (
      <div className="app-error" role="alert">
        <h1>Unable to load review bundle</h1>
        <p>{loadState.message}</p>
        <button type="button" onClick={loadState.reload}>
          Retry
        </button>
      </div>
    )
  }

  const { bundle } = loadState.data
  const effectiveTick = bundle.timeline.ticks[tickIndex] ?? bundle.timeline.ticks[bundle.timeline.default_tick_index]
  const firehoseThroughTime = effectiveTick?.simulation_time ?? bundle.world.simulation_time
  const visibleFirehose = bundle.firehose.filter(
    (event) => event.simulation_time <= firehoseThroughTime,
  )

  const handleLayerToggle = (layer: keyof typeof layers) => {
    setLayers((prev) => ({ ...prev, [layer]: !prev[layer] }))
  }

  return (
    <AppShell
      topBar={<TopBar data={loadState.data} zoomLabel={zoomLabel} selectionLabel={selectionLabel} />}
      layerRail={
        <LayerRail
          bundle={bundle}
          zoomLevel={zoomLevel}
          onZoomChange={setZoomLevel}
          showClusters={layers.clusters}
          showAgents={layers.agents}
          showBuildings={layers.buildings}
          showRoutes={layers.routes}
          showPmtilesNotice={layers.pmtiles}
          onToggle={handleLayerToggle}
        />
      }
      map={
        <DistrictMap
          bundle={bundle}
          zoomLevel={zoomLevel}
          selection={selection}
          onSelect={setSelection}
          showClusters={layers.clusters}
          showAgents={layers.agents}
          showBuildings={layers.buildings}
          showRoutes={layers.routes}
          showPmtilesNotice={layers.pmtiles}
        />
      }
      inspector={<Inspector bundle={bundle} selection={selection} />}
      timeline={
        <TimelineScrubber
          timeline={bundle.timeline}
          tickIndex={tickIndex}
          onTickChange={setTickIndex}
        />
      }
      firehose={<FirehosePanel events={visibleFirehose} simulationTime={firehoseThroughTime} />}
      infoPanels={
        <>
          <InformationSpacePanel summary={bundle.information_space} />
          <ScaleSummaryPanel summary={bundle.scale_summary} zoomLevel={zoomLevel} />
        </>
      }
    />
  )
}

export default App
