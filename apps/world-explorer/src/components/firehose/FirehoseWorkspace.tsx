import { useState } from 'react'
import type { FirehoseEvent } from '../../api/types'
import {
  useFirehoseFilters,
  uniqueActorIds,
  uniqueEventTypes,
  type FirehoseFilters,
} from '../../hooks/useFirehoseFilters'
import { formatSimulationTime } from '../../utils/mapProjection'

interface FirehoseWorkspaceProps {
  events: FirehoseEvent[]
  simulationTime: string
  compact?: boolean
}

/** AWG-UX-012 Firehose Explorer — optional lower panel or dedicated workspace. */
export function FirehoseWorkspace({ events, simulationTime, compact = false }: FirehoseWorkspaceProps) {
  const [filters, setFilters] = useState<FirehoseFilters>({ query: '', eventType: '', actorId: '' })
  const filtered = useFirehoseFilters(events, filters)

  return (
    <section
      className={`workspace workspace--firehose ${compact ? 'workspace--compact' : ''}`}
      aria-label="Event firehose"
    >
      {!compact ? (
        <header className="workspace__header">
          <h2>Firehose Explorer</h2>
          <p role="note">Structured event browsing. Selecting rows does not mutate world state.</p>
        </header>
      ) : (
        <h2 className="panel-heading">Firehose panel</h2>
      )}
      <div className="firehose__filters">
        <label>
          Search
          <input
            type="search"
            value={filters.query}
            onChange={(event) => setFilters((current) => ({ ...current, query: event.target.value }))}
          />
        </label>
        <label>
          Event type
          <select
            value={filters.eventType}
            onChange={(event) => setFilters((current) => ({ ...current, eventType: event.target.value }))}
          >
            <option value="">All types</option>
            {uniqueEventTypes(events).map((type) => (
              <option key={type} value={type}>
                {type}
              </option>
            ))}
          </select>
        </label>
        <label>
          Actor
          <select
            value={filters.actorId}
            onChange={(event) => setFilters((current) => ({ ...current, actorId: event.target.value }))}
          >
            <option value="">All actors</option>
            {uniqueActorIds(events).map((id) => (
              <option key={id} value={id}>
                {id}
              </option>
            ))}
          </select>
        </label>
        <p className="firehose__count">
          {filtered.length} / {events.length} through{' '}
          <time dateTime={simulationTime}>{formatSimulationTime(simulationTime)}</time>
        </p>
      </div>
      <div className="firehose__table-wrap" tabIndex={0}>
        <table className="firehose__table">
          <thead>
            <tr>
              <th scope="col">Seq</th>
              <th scope="col">Time</th>
              <th scope="col">Type</th>
              <th scope="col">Actor</th>
              <th scope="col">Summary</th>
              <th scope="col">Parents</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((event) => (
              <tr key={event.event_id}>
                <td>{event.sequence}</td>
                <td>
                  <time dateTime={event.simulation_time}>{formatSimulationTime(event.simulation_time)}</time>
                </td>
                <td>{event.event_type}</td>
                <td>{event.actor_id ?? '—'}</td>
                <td>{event.summary}</td>
                <td>{event.causal_parent_ids.join(', ') || '—'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  )
}
