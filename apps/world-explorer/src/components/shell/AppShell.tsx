import type { ReactNode } from 'react'

interface AppShellProps {
  topBar: ReactNode
  layerRail: ReactNode
  center: ReactNode
  inspector: ReactNode
  timeline: ReactNode
  firehose: ReactNode
}

/** Persistent regions from AWG-UX-001. */
export function AppShell({
  topBar,
  layerRail,
  center,
  inspector,
  timeline,
  firehose,
}: AppShellProps) {
  return (
    <div className={`app-shell ${firehose ? 'app-shell--firehose-open' : ''}`}>
      <header className="app-shell__top" aria-label="Context and status">
        {topBar}
      </header>
      <div className="app-shell__body">
        {layerRail ? (
          <aside className="app-shell__rail" aria-label="Map layers and filters">
            {layerRail}
          </aside>
        ) : null}
        <main className="app-shell__main" aria-label="Primary workspace">
          {center}
        </main>
        {inspector ? (
          <aside className="app-shell__inspector" aria-label="Selection inspector">
            {inspector}
          </aside>
        ) : null}
      </div>
      <footer className="app-shell__bottom" aria-label="Timeline and optional firehose">
        <div className="app-shell__timeline">{timeline}</div>
        {firehose ? <div className="app-shell__firehose">{firehose}</div> : null}
      </footer>
    </div>
  )
}
