import { describe, expect, it } from 'vitest'
import { fetchReviewBundle } from '../api/reviewBundle'
import syntheticFixture from '../fixtures/review-bundle.synthetic.json'

describe('fetchReviewBundle', () => {
  it('falls back to bundled synthetic fixture when API is unavailable', async () => {
    const originalFetch = globalThis.fetch
    globalThis.fetch = async () => {
      throw new Error('network unavailable')
    }
    try {
      const result = await fetchReviewBundle()
      expect(result.meta.source).toBe('fixture')
      expect(result.bundle.bundle_id).toBe(syntheticFixture.bundle_id)
      expect(result.bundle.world.world_id).toBe('world:mvp1-reference-district')
    } finally {
      globalThis.fetch = originalFetch
    }
  })

  it('returns API payload when GET succeeds', async () => {
    const originalFetch = globalThis.fetch
    globalThis.fetch = async () =>
      ({
        ok: true,
        json: async () => syntheticFixture,
      }) as Response
    try {
      const result = await fetchReviewBundle()
      expect(result.meta.source).toBe('api')
      expect(result.bundle.firehose.length).toBeGreaterThan(0)
    } finally {
      globalThis.fetch = originalFetch
    }
  })
})
