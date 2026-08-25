import { render, screen, waitFor } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import App from './App'

describe('App', () => {
  it('renders read-only World Explorer shell with fixture data', async () => {
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
      expect(screen.getByRole('main', { name: 'District map projection' })).toBeInTheDocument()
      expect(screen.getByRole('heading', { name: /Inspector/i })).toBeInTheDocument()
    } finally {
      globalThis.fetch = originalFetch
    }
  })
})
