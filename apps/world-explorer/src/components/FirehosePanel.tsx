import { useId, useState } from 'react'
import type { FirehoseEvent } from '../api/types'
import { useFirehoseFilters, uniqueActorIds, uniqueEventTypes, type FirehoseFilters } from '../hooks/useFirehoseFilters'
import { formatSimulationTime } from '../utils/mapProjection'

interface FirehosePanelProps {
  events: FirehoseEvent[]
  simulationTime: string
}

export function FirehosePanel({ events, simulationTime }: FirehosePanelProps) {
  const [collapsed, setCollapsed] = useState(false)
  const [filters, setFilters] = useState<FirehoseFilters>({ query: '', eventType: '', actorId: '' })
  const panelId = useId()
  const filtered = useFirehoseFilters(events, filters)
  const eventTypes = uniqueEventTypes(events)
  const actorIds = uniqueActorIds(events)

  return (
    <section className="firehose" aria-label="Event firehose">
      <header className="firehose__header">
        <button
          type="button"
          className="firehose__toggle"
          aria-expanded={!collapsed}
          aria-controls={panelId}
          onClick={() => setCollapsed((v) => !v)}
        >
          {collapsed ? 'Show firehose' : 'Hide firehose'}
        </button>
        <h2 className="panel-heading">Firehose</h2>
        <span className="firehose__count">
          {filtered.length} / {events.length} events · through{' '}
          <time dateTime={simulationTime}>{formatSimulationTime(simulationTime)}</time>
        </span>
      </header>

      {!collapsed ? (
        <div id={panelId} className="firehose__body">
          <div className="firehose__filters">
            <label>
              Search
              <input
                type="search"
                value={filters.query}
                placeholder="Filter by summary or id"
                onChange={(e) => setFilters((f) => ({ ...f, query: e.target.value }))}
              />
            </label>
            <label>
              Event type
              <select
                value={filters.eventType}
                onChange={(e) => setFilters((f) => ({ ...f, eventType: e.target.value }))}
              >
                <option value="">All types</option>
                {eventTypes.map((t) => (
                  <option key={t} value={t}>
                    {t}
                  </option>
                ))}
              </select>
            </label>
            <label>
              Actor
              <select
                value={filters.actorId}
                onChange={(e) => setFilters((f) => ({ ...f, actorId: e.target.value }))}
              >
                <option value="">All actors</option>
                {actorIds.map((id) => (
                  <option key={id} value={id}>
                    {id}
                  </option>
                ))}
              </select>
            </label>
          </div>
          <div className="firehose__table-wrap" role="region" aria-label="Filtered firehose events" tabIndex={0}>
            <table className="firehose__table">
              <thead>
                <tr>
                  <th scope="col">Seq</th>
                  <th scope="col">Time</th>
                  <th scope="col">Type</th>
                  <th scope="col">Actor</th>
                  <th scope="col">Summary</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((event) => (
                  <tr key={event.event_id}>
                    <td>{event.sequence}</td>
                    <td>
                      <time dateTime={event.simulation_time}>
                        {formatSimulationTime(event.simulation_time)}
                      </time>
                    </td>
                    <td>
                      <span className="event-type">{event.event_type}</span>
                    </td>
                    <td>{event.actor_id ?? '—'}</td>
                    <td>{event.summary}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            {filtered.length === 0 ? <p className="firehose__empty">No events match the current filters.</p> : null}
          </div>
        </div>
      ) : null}
    </section>
  )
}
