import type { LoadedReviewBundle, ReviewBundle } from './types'
import syntheticFixture from '../fixtures/review-bundle.synthetic.json'

const REVIEW_BUNDLE_URL = '/api/review-bundle'

function isReviewBundle(value: unknown): value is ReviewBundle {
  if (!value || typeof value !== 'object') return false
  const candidate = value as ReviewBundle
  return (
    typeof candidate.schema_version === 'string' &&
    typeof candidate.bundle_id === 'string' &&
    candidate.world != null &&
    Array.isArray(candidate.firehose)
  )
}

/** GET-only loader: tries /api/review-bundle, falls back to bundled synthetic fixture. */
export async function fetchReviewBundle(signal?: AbortSignal): Promise<LoadedReviewBundle> {
  try {
    const response = await fetch(REVIEW_BUNDLE_URL, {
      method: 'GET',
      headers: { Accept: 'application/json' },
      signal,
    })
    if (!response.ok) {
      throw new Error(`Review bundle request failed: ${response.status}`)
    }
    const data: unknown = await response.json()
    if (!isReviewBundle(data)) {
      throw new Error('Review bundle response failed schema check')
    }
    return {
      bundle: data,
      meta: { source: 'api', fetched_at: new Date().toISOString() },
    }
  } catch {
    return {
      bundle: syntheticFixture as ReviewBundle,
      meta: { source: 'fixture', fetched_at: new Date().toISOString() },
    }
  }
}

export { REVIEW_BUNDLE_URL }
