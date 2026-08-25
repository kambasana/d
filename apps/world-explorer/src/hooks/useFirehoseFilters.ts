import { useMemo } from 'react'
import type { FirehoseEvent, ReviewBundle, SemanticZoomLevelId } from '../api/types'

export interface FirehoseFilters {
  query: string
  eventType: string
  actorId: string
}

export function filterFirehose(events: FirehoseEvent[], filters: FirehoseFilters): FirehoseEvent[] {
  const q = filters.query.trim().toLowerCase()
  return events.filter((event) => {
    if (filters.eventType && event.event_type !== filters.eventType) return false
    if (filters.actorId && event.actor_id !== filters.actorId) return false
    if (!q) return true
    return (
      event.summary.toLowerCase().includes(q) ||
      event.event_id.toLowerCase().includes(q) ||
      (event.actor_id?.toLowerCase().includes(q) ?? false)
    )
  })
}

export function visibleClusters(bundle: ReviewBundle, zoom: SemanticZoomLevelId) {
  return bundle.clusters.filter((cluster) => cluster.visible_at.includes(zoom))
}

export function visibleAgents(bundle: ReviewBundle, zoom: SemanticZoomLevelId) {
  if (zoom === 'district') return []
  return bundle.agents
}

export function uniqueEventTypes(events: FirehoseEvent[]): string[] {
  return [...new Set(events.map((e) => e.event_type))].sort()
}

export function uniqueActorIds(events: FirehoseEvent[]): string[] {
  return [...new Set(events.map((e) => e.actor_id).filter(Boolean) as string[])].sort()
}

export function useFirehoseFilters(events: FirehoseEvent[], filters: FirehoseFilters) {
  return useMemo(() => filterFirehose(events, filters), [events, filters])
}
