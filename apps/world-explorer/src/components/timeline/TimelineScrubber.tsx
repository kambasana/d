import type { TimelineState } from '../../api/types'
import { formatSimulationTime } from '../../utils/mapProjection'

interface TimelineScrubberProps {
  timeline: TimelineState
  tickIndex: number
  onTickChange: (index: number) => void
}

export function TimelineScrubber({ timeline, tickIndex, onTickChange }: TimelineScrubberProps) {
  const current = timeline.ticks[tickIndex]
  const isHistorical = current?.is_historical_projection ?? false

  return (
    <section className="timeline" aria-label="Simulation timeline">
      <div className="timeline__header">
        <h2 className="panel-heading">Timeline</h2>
        {isHistorical ? (
          <span className="badge badge--historical">Historical projection</span>
        ) : (
          <span className="badge badge--current">Current review time</span>
        )}
      </div>
      <div className="timeline__controls">
        <label htmlFor="timeline-scrubber" className="visually-hidden">
          Scrub simulation time
        </label>
        <input
          id="timeline-scrubber"
          type="range"
          min={0}
          max={Math.max(timeline.ticks.length - 1, 0)}
          step={1}
          value={tickIndex}
          onChange={(event) => onTickChange(Number(event.target.value))}
          aria-valuetext={`${current?.label ?? ''}, ${current?.event_count ?? 0} events`}
        />
        <output htmlFor="timeline-scrubber" className="timeline__output">
          <time dateTime={current?.simulation_time}>{formatSimulationTime(current?.simulation_time ?? '')}</time>
          <span>{current?.label}</span>
          <span>{current?.event_count ?? 0} events</span>
        </output>
      </div>
      <p className="timeline__note" role="note">
        Scrubbing reads historical projections; it does not mutate simulation state.
      </p>
    </section>
  )
}
