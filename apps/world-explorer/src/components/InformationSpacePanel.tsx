import type { InformationSpaceSummary } from '../api/types'

interface InformationSpacePanelProps {
  summary: InformationSpaceSummary
}

export function InformationSpacePanel({ summary }: InformationSpacePanelProps) {
  return (
    <section className="info-panel" aria-label="Information space summary">
      <h2 className="panel-heading">Information space</h2>
      <p className="info-panel__notice" role="note">
        {summary.notice}
      </p>
      <dl className="info-panel__stats">
        <div>
          <dt>Channels</dt>
          <dd>{summary.channels.length}</dd>
        </div>
        <div>
          <dt>Exposure edges</dt>
          <dd>{summary.exposure_edges}</dd>
        </div>
        <div>
          <dt>Claims</dt>
          <dd>{summary.claim_count}</dd>
        </div>
        <div>
          <dt>Disputed</dt>
          <dd>{summary.disputed_claim_count}</dd>
        </div>
      </dl>
      <ul className="channel-list">
        {summary.channels.map((channel) => (
          <li key={channel.channel_id}>
            <span className="channel-list__label">{channel.label}</span>
            <span className="channel-list__meta">
              {channel.message_count} msgs · reach ~{channel.reach_estimate} · {channel.classification}
            </span>
          </li>
        ))}
      </ul>
    </section>
  )
}
