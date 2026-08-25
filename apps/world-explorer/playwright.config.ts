import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './e2e',
  fullyParallel: false,
  workers: 1,
  retries: 0,
  reporter: 'line',
  use: {
    baseURL: 'http://127.0.0.1:8766',
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  webServer: {
    command:
      'npm run build && cd ../.. && PYTHONPATH=. python3 scripts/run_world_explorer.py --host 127.0.0.1 --port 8766',
    url: 'http://127.0.0.1:8766/health',
    reuseExistingServer: false,
    timeout: 120_000,
  },
})
