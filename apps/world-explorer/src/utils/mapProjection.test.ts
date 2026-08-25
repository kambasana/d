import { describe, expect, it } from 'vitest'
import type { DistrictGeometry } from '../api/types'
import { clusterKindLabel, confidenceLabel, projectLonLat } from './mapProjection'

const district: DistrictGeometry = {
  bounds: { min_lon: -2, max_lon: -1, min_lat: 53, max_lat: 54 },
  nodes: [],
  edges: [],
  places: [],
  buildings: [],
}

describe('projectLonLat', () => {
  it('maps bounds corners into padded canvas coordinates', () => {
    const min = projectLonLat(-2, 53, district, 200, 100, 0)
    const max = projectLonLat(-1, 54, district, 200, 100, 0)
    expect(min.x).toBe(0)
    expect(min.y).toBe(100)
    expect(max.x).toBe(200)
    expect(max.y).toBe(0)
  })
})

describe('labels', () => {
  it('describes cluster kinds without relying on color', () => {
    expect(clusterKindLabel('geographic')).toContain('Geographic')
    expect(clusterKindLabel('co_location')).toContain('Co-location')
  })

  it('maps confidence to text labels', () => {
    expect(confidenceLabel(0.9)).toBe('High confidence')
    expect(confidenceLabel(0.6)).toBe('Moderate confidence')
    expect(confidenceLabel(0.2)).toBe('Low confidence')
  })
})
