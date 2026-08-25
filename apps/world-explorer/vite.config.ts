import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import react from '@vitejs/plugin-react'
import { defineConfig } from 'vitest/config'

const rootDir = path.dirname(fileURLToPath(import.meta.url))
const reviewBundlePath = path.resolve(rootDir, 'public/api/review-bundle.json')

function reviewBundleMiddleware(
  req: import('node:http').IncomingMessage,
  res: import('node:http').ServerResponse,
  next: () => void,
) {
  if (req.url !== '/api/review-bundle') {
    next()
    return
  }
  if (req.method !== 'GET') {
    res.statusCode = 405
    res.setHeader('Allow', 'GET')
    res.end('Method Not Allowed')
    return
  }
  res.statusCode = 200
  res.setHeader('Content-Type', 'application/json')
  fs.createReadStream(reviewBundlePath).pipe(res)
}

export default defineConfig({
  plugins: [
    react(),
    {
      name: 'review-bundle-api',
      configureServer(server) {
        server.middlewares.use(reviewBundleMiddleware)
      },
      configurePreviewServer(server) {
        server.middlewares.use(reviewBundleMiddleware)
      },
    },
  ],
  test: {
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
    css: true,
    include: ['src/**/*.test.{ts,tsx}'],
  },
})
