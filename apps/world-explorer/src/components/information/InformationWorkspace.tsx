import type { ReviewBundle } from '../../api/types'

interface InformationWorkspaceProps {
  bundle: ReviewBundle
}

/** AWG-UX-010 / AWG-UX-001 Information Space workspace — not stacked on the map. */
export function InformationWorkspace({ bundle }: InformationWorkspaceProps) {
  const summary = bundle.information_space

  return (
    <section className="workspace workspace--information" aria-label="Information space">
      <header className="workspace__header">
        <h2>Information Space</h2>
        <p role="note">{summary.notice}</p>
      </header>
      <div className="workspace__grid">
        <article>
          <h3>Channels</h3>
          <ul>
            {summary.channels.map((channel) => (
              <li key={channel.channel_id}>
                <strong>{channel.label}</strong>
                <span>
                  {channel.message_count} messages · reach {channel.reach_estimate} ·{' '}
                  {channel.classification}
                </span>
              </li>
            ))}
          </ul>
        </article>
        <article>
          <h3>Claims and exposure</h3>
          <dl>
            <div>
              <dt>Claims</dt>
              <dd>{summary.claim_count}</dd>
            </div>
            <div>
              <dt>Exposure edges</dt>
              <dd>{summary.exposure_edges}</dd>
            </div>
            <div>
              <dt>Disputed</dt>
              <dd>{summary.disputed_claim_count}</dd>
            </div>
          </dl>
          <p role="note">Likes, views, and follows are not treated as belief or endorsement.</p>
        </article>
      </div>
    </section>
  )
}
