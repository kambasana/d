import type { ReviewBundle, Selection } from '../api/types'
import { clusterKindLabel, confidenceLabel, formatSimulationTime } from '../utils/mapProjection'

interface InspectorProps {
  bundle: ReviewBundle
  selection: Selection
}

export function Inspector({ bundle, selection }: InspectorProps) {
  if (!selection) {
    return (
      <div className="inspector inspector--empty">
        <h2 className="panel-heading">Inspector</h2>
        <p>Select a cluster, agent, or building on the map to inspect world truth and agent perspective.</p>
        <p className="inspector__hint" role="note">
          No mutation controls are available in this read-only review build.
        </p>
      </div>
    )
  }

  if (selection.kind === 'cluster') {
    const cluster = bundle.clusters.find((c) => c.cluster_id === selection.id)
    if (!cluster) return <InspectorMissing kind="cluster" id={selection.id} />
    return (
      <div className="inspector">
        <h2 className="panel-heading">Cluster inspector</h2>
        <span className="badge badge--projection">Projection-only</span>
        <dl className="inspector__facts">
          <div>
            <dt>Kind</dt>
            <dd>{clusterKindLabel(cluster.kind)}</dd>
          </div>
          <div>
            <dt>Label</dt>
            <dd>{cluster.label}</dd>
          </div>
          <div>
            <dt>Count</dt>
            <dd>{cluster.count}</dd>
          </div>
          <div>
            <dt>Notice</dt>
            <dd>{cluster.projection_notice}</dd>
          </div>
        </dl>
        <section className="inspector__section inspector__section--truth">
          <h3>World truth (aggregate)</h3>
          <p>
            Member agents: {cluster.member_agent_ids.length || '—'} · Buildings:{' '}
            {cluster.member_building_ids.join(', ') || '—'}
          </p>
          <p role="note">Cluster geometry is a visualization aid; authoritative positions are unchanged.</p>
        </section>
      </div>
    )
  }

  if (selection.kind === 'building') {
    const building = bundle.district.buildings.find((b) => b.building_id === selection.id)
    if (!building) return <InspectorMissing kind="building" id={selection.id} />
    return (
      <div className="inspector">
        <h2 className="panel-heading">Building inspector</h2>
        <section className="inspector__section inspector__section--truth">
          <h3>World truth</h3>
          <dl className="inspector__facts">
            <div>
              <dt>Name</dt>
              <dd>{building.name}</dd>
            </div>
            <div>
              <dt>Occupancy</dt>
              <dd>
                {building.occupancy} / {building.capacity}
              </dd>
            </div>
          </dl>
          <h4>Floors</h4>
          <ul className="floor-list">
            {building.floors.map((floor) => (
              <li key={floor.floor_id}>
                <span className="floor-list__label">{floor.label}</span>
                <span className="floor-list__count">{floor.occupancy} occupants</span>
              </li>
            ))}
          </ul>
        </section>
        <section className="inspector__section inspector__section--belief">
          <h3>Agent perspective</h3>
          <p>Select an agent inside this building to compare belief against world truth.</p>
        </section>
      </div>
    )
  }

  const agent = bundle.agents.find((a) => a.agent_id === selection.id)
  const detail = bundle.agent_details[selection.id]
  if (!agent) return <InspectorMissing kind="agent" id={selection.id} />

  return (
    <div className="inspector">
      <h2 className="panel-heading">Agent inspector — {agent.display_name}</h2>

      <section className="inspector__section inspector__section--truth" aria-labelledby="world-truth-heading">
        <h3 id="world-truth-heading">World truth</h3>
        {detail ? (
          <dl className="inspector__facts">
            <div>
              <dt>Location</dt>
              <dd>{detail.world_truth.current_place_name}</dd>
            </div>
            <div>
              <dt>Journey</dt>
              <dd>{detail.world_truth.journey_status}</dd>
            </div>
            <div>
              <dt>Coordinates</dt>
              <dd>
                {detail.world_truth.coordinates.longitude.toFixed(4)},{' '}
                {detail.world_truth.coordinates.latitude.toFixed(4)}
              </dd>
            </div>
            <div>
              <dt>Last event</dt>
              <dd>{detail.world_truth.last_event_summary}</dd>
            </div>
            <div>
              <dt>Fidelity</dt>
              <dd>{detail.world_truth.fidelity}</dd>
            </div>
          </dl>
        ) : (
          <p>Authoritative detail not bundled for this agent in the review fixture.</p>
        )}
      </section>

      <section
        className="inspector__section inspector__section--belief"
        aria-labelledby="agent-perspective-heading"
      >
        <h3 id="agent-perspective-heading">Agent perspective</h3>
        {detail ? (
          <>
            <p>
              <span className="badge badge--belief">Belief</span>{' '}
              {detail.agent_perspective.belief_summary}
            </p>
            <p>
              Observed as: <strong>{detail.agent_perspective.observed_place_name}</strong>
              {' · '}
              <span title={confidenceLabel(detail.agent_perspective.confidence)}>
                {confidenceLabel(detail.agent_perspective.confidence)} (
                {Math.round(detail.agent_perspective.confidence * 100)}%)
              </span>
              {detail.agent_perspective.stale ? (
                <span className="badge badge--stale">Stale</span>
              ) : null}
            </p>
            <h4>Claims</h4>
            <ul className="claim-list">
              {detail.agent_perspective.claims.map((claim) => (
                <li key={claim.claim_id}>
                  <span className="claim-list__text">{claim.text}</span>
                  <span className="claim-list__meta">
                    {confidenceLabel(claim.confidence)} · {claim.source_type}
                  </span>
                </li>
              ))}
            </ul>
            {detail.agent_perspective.knowledge_gaps.length ? (
              <>
                <h4>Knowledge gaps</h4>
                <ul>
                  {detail.agent_perspective.knowledge_gaps.map((gap) => (
                    <li key={gap}>{gap}</li>
                  ))}
                </ul>
              </>
            ) : null}
          </>
        ) : (
          <p>No perspective bundle included for this agent.</p>
        )}
      </section>

      <p className="inspector__status">
        Status: {agent.status} · Place: {agent.place_id}
      </p>
    </div>
  )
}

function InspectorMissing({ kind, id }: { kind: string; id: string }) {
  return (
    <div className="inspector inspector--empty">
      <h2 className="panel-heading">Inspector</h2>
      <p>
        Selected {kind} <code>{id}</code> is not present in the current review bundle.
      </p>
    </div>
  )
}
