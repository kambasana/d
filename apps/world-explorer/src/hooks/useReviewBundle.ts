import { useCallback, useEffect, useState } from 'react'
import { fetchReviewBundle } from '../api/reviewBundle'
import type { LoadedReviewBundle } from '../api/types'

export type LoadState =
  | { status: 'loading' }
  | { status: 'error'; message: string }
  | { status: 'ready'; data: LoadedReviewBundle }

export function useReviewBundle(): LoadState & { reload: () => void } {
  const [state, setState] = useState<LoadState>({ status: 'loading' })
  const [reloadToken, setReloadToken] = useState(0)

  const reload = useCallback(() => {
    setState({ status: 'loading' })
    setReloadToken((value) => value + 1)
  }, [])

  useEffect(() => {
    const controller = new AbortController()
    fetchReviewBundle(controller.signal)
      .then((data) => setState({ status: 'ready', data }))
      .catch((error: unknown) => {
        if (controller.signal.aborted) return
        const message = error instanceof Error ? error.message : 'Unknown load error'
        setState({ status: 'error', message })
      })
    return () => controller.abort()
  }, [reloadToken])

  return { ...state, reload }
}
