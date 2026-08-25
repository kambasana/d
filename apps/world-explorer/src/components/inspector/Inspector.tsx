import { useState } from 'react'
import type { ReviewBundle, Selection } from '../../api/types'
import { clusterKindLabel, confidenceLabel } from '../../utils/mapProjection'

interface InspectorProps {
  bundle: ReviewBundle
  selection: Selection
}

type InspectorTab = 'world_truth' | 'agent_perspective'

/** AWG-UX-004: separate World truth and Agent perspective tabs. */
export function Inspector({ bundle, selection }: InspectorProps) {
  const [tab, setTab] = useState<InspectorTab>('world_truth')

  if (!selection) {
    return (
      <div className="inspector inspector--empty">
        <h2 className="panel-heading">Inspector</h2>
        <p>Select a cluster, agent, or building from the map or the accessible list.</p>
        <p className="inspector__hint" role="note">
          No mutation controls are available in this read-only review build.
        </p>
      </div>
    )
  }

  if (selection.kind === 'cluster') {
    const cluster = bundle.clusters.find((item) => item.cluster_id === selection.id)
    if (!cluster) return <Missing kind="cluster" id={selection.id} />
    return (
      <div className="inspector">
        <h2 className="panel-heading">Cluster inspector</h2>
        <span className="badge badge--projection">projection_only</span>
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
      </div>
    )
  }

  if (selection.kind === 'building') {
    const building = bundle.district.buildings.find((item) => item.building_id === selection.id)
    if (!building) return <Missing kind="building" id={selection.id} />
    return (
      <div className="inspector">
        <h2 className="panel-heading">Building inspector</h2>
        <span className="badge badge--truth">authoritative occupancy</span>
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
        <h3>Floors</h3>
        <ul className="floor-list">
          {building.floors.map((floor) => (
            <li key={floor.floor_id}>
              <span>{floor.label}</span>
              <span>{floor.occupancy} occupants</span>
            </li>
          ))}
        </ul>
      </div>
    )
  }

  const agent = bundle.agents.find((item) => item.agent_id === selection.id)
  const detail = bundle.agent_details[selection.id]
  if (!agent) return <Missing kind="agent" id={selection.id} />

  return (
    <div className="inspector">
      <h2 className="panel-heading">Agent inspector — {agent.display_name}</h2>
      <div className="inspector__tabs" role="tablist" aria-label="Inspector perspective">
        <button
          type="button"
          role="tab"
          aria-selected={tab === 'world_truth'}
          className={tab === 'world_truth' ? 'is-active' : ''}
          onClick={() => setTab('world_truth')}
        >
          World truth
        </button>
        <button
          type="button"
          role="tab"
          aria-selected={tab === 'agent_perspective'}
          className={tab === 'agent_perspective' ? 'is-active' : ''}
          onClick={() => setTab('agent_perspective')}
        >
          Agent perspective
        </button>
      </div>

      {tab === 'world_truth' ? (
        <section className="inspector__section inspector__section--truth" role="tabpanel">
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
                  {detail.world_truth.coordinates.longitude.toFixed(5)},{' '}
                  {detail.world_truth.coordinates.latitude.toFixed(5)}
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
            <p>Authoritative detail is not bundled for this agent.</p>
          )}
        </section>
      ) : (
        <section className="inspector__section inspector__section--belief" role="tabpanel">
          {detail ? (
            <>
              <p>
                <span className="badge badge--belief">Belief</span> {detail.agent_perspective.belief_summary}
              </p>
              <p>
                Observed as: {detail.agent_perspective.observed_place_name} ·{' '}
                {confidenceLabel(detail.agent_perspective.confidence)} (
                {Math.round(detail.agent_perspective.confidence * 100)}%)
              </p>
              <h3>Claims</h3>
              <ul className="claim-list">
                {detail.agent_perspective.claims.length ? (
                  detail.agent_perspective.claims.map((claim) => (
                    <li key={claim.claim_id}>
                      {claim.text}
                      <span>
                        {confidenceLabel(claim.confidence)} · {claim.source_type}
                      </span>
                    </li>
                  ))
                ) : (
                  <li>No claims on an observation path for this agent.</li>
                )}
              </ul>
              <h3>Knowledge gaps</h3>
              <ul>
                {detail.agent_perspective.knowledge_gaps.map((gap) => (
                  <li key={gap}>{gap}</li>
                ))}
              </ul>
            </>
          ) : (
            <p>No agent perspective bundle for this selection.</p>
          )}
        </section>
      )}
    </div>
  )
}

function Missing({ kind, id }: { kind: string; id: string }) {
  return (
    <div className="inspector inspector--empty">
      <h2 className="panel-heading">Inspector</h2>
      <p>
        Selected {kind} <code>{id}</code> is not present in the current review projection.
      </p>
    </div>
  )
}
