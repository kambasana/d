import { useCallback, useEffect, useState } from 'react'
import { fetchReviewBundle } from '../api/reviewBundle'
import type { LoadedReviewBundle } from '../api/types'

export type LoadState =
  | { status: 'loading' }
  | { status: 'error'; message: string }
  | { status: 'ready'; data: LoadedReviewBundle }

export function useReviewBundle(): LoadState & { reload: () => void } {
  const [state, setState] = useState<LoadState>({ status: 'loading' })

  const load = useCallback(() => {
    const controller = new AbortController()
    setState({ status: 'loading' })
    fetchReviewBundle(controller.signal)
      .then((data) => setState({ status: 'ready', data }))
      .catch((error: unknown) => {
        const message = error instanceof Error ? error.message : 'Unknown load error'
        setState({ status: 'error', message })
      })
    return () => controller.abort()
  }, [])

  useEffect(() => {
    const cleanup = load()
    return cleanup
  }, [load])

  return { ...state, reload: load }
}
