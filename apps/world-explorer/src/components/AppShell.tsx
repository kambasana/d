import type { ReactNode } from 'react'
import './AppShell.css'

interface AppShellProps {
  topBar: ReactNode
  layerRail: ReactNode
  map: ReactNode
  inspector: ReactNode
  timeline: ReactNode
  firehose: ReactNode
  infoPanels?: ReactNode
}

export function AppShell({
  topBar,
  layerRail,
  map,
  inspector,
  timeline,
  firehose,
  infoPanels,
}: AppShellProps) {
  return (
    <div className="app-shell">
      <header className="app-shell__top" aria-label="Context and status">
        {topBar}
      </header>
      <div className="app-shell__body">
        <aside className="app-shell__rail" aria-label="Layer controls">
          {layerRail}
        </aside>
        <main className="app-shell__main" aria-label="District map projection">
          {map}
          {infoPanels ? <div className="app-shell__info-panels">{infoPanels}</div> : null}
        </main>
        <aside className="app-shell__inspector" aria-label="Selection inspector">
          {inspector}
        </aside>
      </div>
      <footer className="app-shell__bottom" aria-label="Timeline and event firehose">
        <div className="app-shell__timeline">{timeline}</div>
        <div className="app-shell__firehose">{firehose}</div>
      </footer>
    </div>
  )
}
