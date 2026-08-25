import { expect, test } from '@playwright/test'

test('renders AWG-UX shell with workspaces, not a one-page dump', async ({ page, request }) => {
  await page.goto('/')

  await expect(page.getByRole('heading', { name: 'World Explorer' })).toBeVisible()
  await expect(page.getByLabel('Context and status')).toBeVisible()
  await expect(page.getByLabel('Map layers and filters')).toBeVisible()
  await expect(page.getByRole('main', { name: 'Primary workspace' })).toBeVisible()
  await expect(page.getByLabel('Selection inspector')).toBeVisible()
  await expect(page.getByLabel('Timeline and optional firehose')).toBeVisible()
  await expect(page.getByText('GET /api/review-bundle')).toBeVisible()
  await expect(page.getByTestId('map-canvas')).toBeVisible()
  await expect(page.getByText(/PMTiles display archive/)).toBeVisible()
  await expect(page.getByLabel('List alternative to map selection')).toBeVisible()

  // Firehose and information space are workspaces / optional panel — not always stacked.
  await expect(page.getByRole('heading', { name: 'Information Space' })).toHaveCount(0)
  await expect(page.getByRole('heading', { name: 'Firehose Explorer' })).toHaveCount(0)

  for (const method of ['post', 'put', 'patch', 'delete'] as const) {
    const response = await request[method]('/api/review-bundle')
    expect(response.status()).toBe(405)
  }
})

test('supports semantic zoom, list selection, inspector tabs, and optional firehose', async ({
  page,
}) => {
  await page.goto('/')

  await page.locator('input[name="semantic-zoom"][value="street"]').check()
  await expect(page.getByText('Street', { exact: true }).first()).toBeVisible()

  await page.getByRole('button', { name: /Agent A-001|Agent district/i }).first().click()
  await expect(page.getByRole('heading', { name: /Agent inspector/ })).toBeVisible()
  await expect(page.getByRole('tab', { name: 'World truth' })).toBeVisible()
  await expect(page.getByRole('tab', { name: 'Agent perspective' })).toBeVisible()
  await page.getByRole('tab', { name: 'Agent perspective' }).click()
  await expect(page.getByText(/Belief/i).first()).toBeVisible()

  await page.getByRole('button', { name: 'Show firehose panel' }).click()
  await expect(page.getByLabel('Event type')).toBeVisible()
  await page.getByLabel('Event type').selectOption({ index: 1 })
  await expect(page.locator('.firehose__count')).toBeVisible()
  await page.getByRole('button', { name: 'Hide firehose panel' }).click()
  await expect(page.getByRole('button', { name: 'Show firehose panel' })).toBeVisible()

  const timeline = page.getByLabel('Scrub simulation time')
  await timeline.focus()
  await timeline.press('Home')
  await expect(page.getByText('Historical projection', { exact: true })).toBeVisible()
})

test('workspace switching isolates information and firehose views', async ({ page }) => {
  await page.goto('/')

  await page.getByRole('button', { name: 'Information Space' }).click()
  await expect(page.getByRole('heading', { name: 'Information Space' })).toBeVisible()
  await expect(page.getByText(/Likes, views, and follows are not belief/)).toBeVisible()
  await expect(page.getByTestId('map-canvas')).toHaveCount(0)
  await expect(page.getByLabel('Map layers and filters')).toHaveCount(0)

  await page.getByRole('button', { name: 'Firehose Explorer' }).click()
  await expect(page.getByRole('heading', { name: 'Firehose Explorer' })).toBeVisible()
  await expect(page.getByLabel('Event type')).toBeVisible()
  await expect(page.getByTestId('map-canvas')).toHaveCount(0)

  await page.getByRole('button', { name: 'World Explorer' }).click()
  await expect(page.getByTestId('map-canvas')).toBeVisible()
})

test.describe('responsive and reduced-motion review', () => {
  test.use({ viewport: { width: 375, height: 667 }, reducedMotion: 'reduce' })

  test('keeps primary regions reachable at a narrow viewport', async ({ page }) => {
    await page.emulateMedia({ reducedMotion: 'reduce' })
    await page.goto('/')

    await expect(page.getByLabel('Context and status')).toBeVisible()
    await expect(page.getByLabel('Map layers and filters')).toBeVisible()
    await expect(page.getByRole('main', { name: 'Primary workspace' })).toBeVisible()
    await expect(page.getByLabel('Selection inspector')).toBeVisible()
    await expect(page.getByLabel('Simulation timeline')).toBeVisible()

    const reduced = await page.evaluate(() =>
      window.matchMedia('(prefers-reduced-motion: reduce)').matches,
    )
    expect(reduced).toBe(true)
  })
})
