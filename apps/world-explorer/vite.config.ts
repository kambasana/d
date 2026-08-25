import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api/review-bundle': {
        target: 'http://localhost:4173',
        bypass: (req) => {
          if (req.url?.startsWith('/api/review-bundle')) {
            return '/api/review-bundle.json'
          }
        },
      },
    },
  },
  test: {
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
    css: true,
  },
})
