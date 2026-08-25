import { describe, expect, it } from 'vitest'
import type { FirehoseEvent } from '../api/types'
import { filterFirehose, visibleClusters } from '../hooks/useFirehoseFilters'
import syntheticFixture from '../fixtures/review-bundle.synthetic.json'
import type { ReviewBundle } from '../api/types'

const bundle = syntheticFixture as ReviewBundle

const events: FirehoseEvent[] = [
  {
    event_id: 'e1',
    sequence: 1,
    simulation_time: '2042-05-04T10:00:00Z',
    event_type: 'journey.started',
    actor_id: 'agent:a-001',
    summary: 'started',
    causal_parent_ids: [],
  },
  {
    event_id: 'e2',
    sequence: 2,
    simulation_time: '2042-05-04T11:00:00Z',
    event_type: 'occupancy.entered',
    actor_id: 'agent:a-002',
    summary: 'entered cafe',
    causal_parent_ids: [],
  },
]

describe('filterFirehose', () => {
  it('filters by query, type, and actor', () => {
    expect(filterFirehose(events, { query: 'cafe', eventType: '', actorId: '' })).toHaveLength(1)
    expect(
      filterFirehose(events, { query: '', eventType: 'journey.started', actorId: '' }),
    ).toHaveLength(1)
    expect(
      filterFirehose(events, { query: '', eventType: '', actorId: 'agent:a-002' }),
    ).toHaveLength(1)
  })
})

describe('visibleClusters', () => {
  it('returns district-level clusters only at district zoom', () => {
    const districtClusters = visibleClusters(bundle, 'district')
    expect(districtClusters.every((c) => c.visible_at.includes('district'))).toBe(true)
    expect(visibleClusters(bundle, 'street').some((c) => c.kind === 'co_location')).toBe(true)
  })
})
