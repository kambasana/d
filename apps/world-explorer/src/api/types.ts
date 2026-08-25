/** GET /api/review-bundle — read-only review projection contract (not authoritative world state). */

export type ProjectionAuthority = 'projection_only'

export type SemanticZoomLevelId = 'district' | 'street' | 'building'

export type RunState = 'completed' | 'running' | 'paused'

export type ClusterKind = 'geographic' | 'co_location' | 'analytical'

export type SelectionKind = 'cluster' | 'agent' | 'building' | 'place'

export interface ReviewBundle {
  schema_version: string
  bundle_id: string
  projection_notice: string
  world: WorldContext
  map_projection: MapProjection
  semantic_zoom: SemanticZoomState
  district: DistrictGeometry
  clusters: MapCluster[]
  agents: AgentSummary[]
  agent_details: Record<string, AgentDetail>
  firehose: FirehoseEvent[]
  timeline: TimelineState
  information_space: InformationSpaceSummary
  scale_summary: ScaleSummary
}

export interface WorldContext {
  world_id: string
  scenario_id: string
  branch_id: string
  district_id: string
  district_name: string
  simulation_time: string
  start_time: string
  end_time: string
  run_state: RunState
  source_classification: 'generated' | 'imported' | 'synthetic'
  agent_count: number
}

export interface MapProjection {
  kind: 'synthetic_svg' | 'pmtiles_display'
  authority: ProjectionAuthority
  pmtiles_available: boolean
  pmtiles_label: string
  notice: string
}

export interface SemanticZoomState {
  levels: SemanticZoomLevel[]
  default_level: SemanticZoomLevelId
}

export interface SemanticZoomLevel {
  id: SemanticZoomLevelId
  label: string
  description: string
  min_agent_marker_px: number
}

export interface DistrictGeometry {
  bounds: {
    min_lon: number
    max_lon: number
    min_lat: number
    max_lat: number
  }
  nodes: DistrictNode[]
  edges: DistrictEdge[]
  places: Place[]
  buildings: Building[]
}

export interface DistrictNode {
  node_id: string
  longitude: number
  latitude: number
  place_id?: string
}

export interface DistrictEdge {
  edge_id: string
  source: string
  target: string
  distance_m: number
  accessible: boolean
}

export interface Place {
  place_id: string
  name: string
  route_node_id: string
  building_id?: string
}

export interface Building {
  building_id: string
  name: string
  route_node_id: string
  capacity: number
  occupancy: number
  floors: BuildingFloor[]
}

export interface BuildingFloor {
  floor_id: string
  level: number
  label: string
  occupancy: number
  room_ids: string[]
}

export interface MapCluster {
  cluster_id: string
  kind: ClusterKind
  label: string
  count: number
  centroid: { longitude: number; latitude: number }
  visible_at: SemanticZoomLevelId[]
  member_agent_ids: string[]
  member_building_ids: string[]
  projection_notice: string
}

export interface AgentSummary {
  agent_id: string
  display_name: string
  longitude: number
  latitude: number
  place_id: string
  building_id?: string
  status: string
  cluster_id?: string
}

export interface AgentDetail {
  agent_id: string
  display_name: string
  world_truth: AgentWorldTruth
  agent_perspective: AgentPerspective
}

export interface AgentWorldTruth {
  current_place_id: string
  current_place_name: string
  building_id?: string
  building_name?: string
  journey_status: string
  coordinates: { longitude: number; latitude: number }
  occupancy_zone?: string
  last_event_id: string
  last_event_summary: string
  fidelity: string
}

export interface AgentPerspective {
  observed_place_name: string
  belief_summary: string
  confidence: number
  claims: AgentClaim[]
  knowledge_gaps: string[]
  stale: boolean
}

export interface AgentClaim {
  claim_id: string
  text: string
  confidence: number
  source_type: string
}

export interface FirehoseEvent {
  event_id: string
  sequence: number
  simulation_time: string
  event_type: string
  actor_id?: string
  place_id?: string
  summary: string
  causal_parent_ids: string[]
}

export interface TimelineState {
  ticks: TimelineTick[]
  default_tick_index: number
}

export interface TimelineTick {
  tick_index: number
  simulation_time: string
  label: string
  is_historical_projection: boolean
  event_count: number
}

export interface InformationSpaceSummary {
  channels: InformationChannel[]
  exposure_edges: number
  claim_count: number
  disputed_claim_count: number
  notice: string
}

export interface InformationChannel {
  channel_id: string
  label: string
  message_count: number
  reach_estimate: number
  classification: 'synthetic' | 'simulated' | 'imported'
}

export interface ScaleSummary {
  current_level: SemanticZoomLevelId
  population_visible: number
  population_total: number
  cluster_count: number
  building_count: number
  active_journeys: number
  projection_density: string
}

export interface ReviewBundleMeta {
  source: 'api' | 'fixture'
  fetched_at: string
}

export interface LoadedReviewBundle {
  bundle: ReviewBundle
  meta: ReviewBundleMeta
}

export type Selection =
  | { kind: 'cluster'; id: string }
  | { kind: 'agent'; id: string }
  | { kind: 'building'; id: string }
  | null
