import { useMemo, useState } from 'react'
import { AppShell } from './components/shell/AppShell'
import { TopBar } from './components/shell/TopBar'
import { LayerRail, type LayerState } from './components/shell/LayerRail'
import { MapCanvas } from './components/map/MapCanvas'
import { Inspector } from './components/inspector/Inspector'
import { TimelineScrubber } from './components/timeline/TimelineScrubber'
import { FirehoseWorkspace } from './components/firehose/FirehoseWorkspace'
import { InformationWorkspace } from './components/information/InformationWorkspace'
import { useReviewBundle } from './hooks/useReviewBundle'
import type { Selection, SemanticZoomLevelId, WorkspaceId } from './api/types'
import './App.css'

const INITIAL_LAYERS: LayerState = {
  basemap: true,
  routes: true,
  buildings: true,
  clusters: true,
  agents: true,
  pmtiles: false,
}

function App() {
  const loadState = useReviewBundle()
  const [workspace, setWorkspace] = useState<WorkspaceId>('world_explorer')
  const [zoomLevel, setZoomLevel] = useState<SemanticZoomLevelId>('district')
  const [selection, setSelection] = useState<Selection>(null)
  const [tickIndex, setTickIndex] = useState<number | null>(null)
  const [firehoseOpen, setFirehoseOpen] = useState(false)
  const [layers, setLayers] = useState<LayerState>(INITIAL_LAYERS)

  const selectionLabel = useMemo(() => {
    if (!selection) return 'None'
    return `${selection.kind}: ${selection.id}`
  }, [selection])

  const zoomLabel = useMemo(() => {
    if (loadState.status !== 'ready') return '—'
    const level = loadState.data.bundle.semantic_zoom.levels.find((item) => item.id === zoomLevel)
    return level?.label ?? zoomLevel
  }, [loadState, zoomLevel])

  if (loadState.status === 'loading') {
    return (
      <div className="app-loading" role="status" aria-live="polite">
        Loading review projection…
      </div>
    )
  }

  if (loadState.status === 'error') {
    return (
      <div className="app-error" role="alert">
        <h1>Unable to load review projection</h1>
        <p>{loadState.message}</p>
        <button type="button" onClick={loadState.reload}>
          Retry
        </button>
      </div>
    )
  }

  const { bundle } = loadState.data
  const activeTickIndex = tickIndex ?? bundle.timeline.default_tick_index
  const effectiveTick =
    bundle.timeline.ticks[activeTickIndex] ??
    bundle.timeline.ticks[bundle.timeline.default_tick_index]
  const firehoseThroughTime = effectiveTick?.simulation_time ?? bundle.world.simulation_time
  const visibleFirehose = bundle.firehose.filter(
    (event) => event.simulation_time <= firehoseThroughTime,
  )

  const handleLayerToggle = (layer: keyof LayerState) => {
    setLayers((prev) => ({ ...prev, [layer]: !prev[layer] }))
  }

  return (
    <AppShell
      topBar={
        <TopBar
          data={loadState.data}
          workspace={workspace}
          onWorkspaceChange={setWorkspace}
          zoomLabel={zoomLabel}
          selectionLabel={selectionLabel}
          firehoseOpen={firehoseOpen}
          onToggleFirehose={() => setFirehoseOpen((open) => !open)}
        />
      }
      layerRail={
        workspace === 'world_explorer' ? (
          <LayerRail
            bundle={bundle}
            zoomLevel={zoomLevel}
            onZoomChange={setZoomLevel}
            layers={layers}
            onToggle={handleLayerToggle}
          />
        ) : null
      }
      center={
        workspace === 'world_explorer' ? (
          <MapCanvas
            bundle={bundle}
            zoomLevel={zoomLevel}
            selection={selection}
            onSelect={setSelection}
            layers={layers}
          />
        ) : workspace === 'information_space' ? (
          <InformationWorkspace bundle={bundle} />
        ) : (
          <FirehoseWorkspace events={visibleFirehose} simulationTime={firehoseThroughTime} />
        )
      }
      inspector={
        workspace === 'world_explorer' ? (
          <Inspector bundle={bundle} selection={selection} />
        ) : null
      }
      timeline={
        <TimelineScrubber
          timeline={bundle.timeline}
          tickIndex={activeTickIndex}
          onTickChange={setTickIndex}
        />
      }
      firehose={
        firehoseOpen && workspace === 'world_explorer' ? (
          <FirehoseWorkspace
            events={visibleFirehose}
            simulationTime={firehoseThroughTime}
            compact
          />
        ) : null
      }
    />
  )
}

export default App
