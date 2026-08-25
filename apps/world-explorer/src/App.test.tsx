import { render, screen, waitFor } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'

vi.mock('maplibre-gl', () => {
  class MapLibreMap {
    constructor() {}
    addControl() {
      return this
    }
    on() {
      return this
    }
    remove() {}
    isStyleLoaded() {
      return false
    }
    getSource() {
      return undefined
    }
    getLayer() {
      return undefined
    }
    setLayoutProperty() {}
    easeTo() {}
    addSource() {}
    addLayer() {}
  }
  class NavigationControl {}
  return {
    Map: MapLibreMap,
    NavigationControl,
    addProtocol() {},
  }
})

vi.mock('pmtiles', () => ({
  Protocol: class {
    tile = () => undefined
  },
}))

import App from './App'

describe('App', () => {
  it('renders AWG-UX shell regions with workspace switching', async () => {
    const originalFetch = globalThis.fetch
    globalThis.fetch = async () => {
      throw new Error('offline')
    }
    try {
      render(<App />)
      await waitFor(() => {
        expect(screen.getByRole('heading', { name: /World Explorer/i })).toBeInTheDocument()
      })
      expect(screen.getByTitle('Read-only review interface')).toBeInTheDocument()
      expect(screen.getByText(/synthetic fixture fallback/i)).toBeInTheDocument()
      expect(screen.getByRole('main', { name: 'Primary workspace' })).toBeInTheDocument()
      expect(screen.getByLabelText('Map layers and filters')).toBeInTheDocument()
      expect(screen.getByLabelText('Selection inspector')).toBeInTheDocument()
      expect(screen.getByLabelText('Simulation timeline')).toBeInTheDocument()
      expect(screen.getByRole('navigation', { name: 'Core workspaces' })).toBeInTheDocument()
      expect(
        screen.getByRole('application', { name: 'World Explorer operational map' }),
      ).toBeInTheDocument()

      screen.getByRole('button', { name: 'Information Space' }).click()
      await waitFor(() => {
        expect(screen.getByRole('heading', { name: 'Information Space' })).toBeInTheDocument()
      })
      expect(screen.queryByLabelText('Map layers and filters')).not.toBeInTheDocument()
    } finally {
      globalThis.fetch = originalFetch
    }
  })
})
