import type { DistrictGeometry } from '../api/types'

export interface MapPoint {
  x: number
  y: number
}

export function projectLonLat(
  longitude: number,
  latitude: number,
  district: DistrictGeometry,
  width: number,
  height: number,
  padding = 24,
): MapPoint {
  const { min_lon, max_lon, min_lat, max_lat } = district.bounds
  const lonSpan = max_lon - min_lon || 1
  const latSpan = max_lat - min_lat || 1
  const innerW = width - padding * 2
  const innerH = height - padding * 2
  const x = padding + ((longitude - min_lon) / lonSpan) * innerW
  const y = padding + (1 - (latitude - min_lat) / latSpan) * innerH
  return { x, y }
}

export function formatSimulationTime(iso: string): string {
  const date = new Date(iso)
  return date.toLocaleString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    timeZoneName: 'short',
  })
}

export function clusterKindLabel(kind: string): string {
  switch (kind) {
    case 'geographic':
      return 'Geographic cluster'
    case 'co_location':
      return 'Co-location cluster'
    case 'analytical':
      return 'Analytical cluster'
    default:
      return kind
  }
}

export function confidenceLabel(value: number): string {
  if (value >= 0.8) return 'High confidence'
  if (value >= 0.5) return 'Moderate confidence'
  return 'Low confidence'
}
