import { test, expect } from '@playwright/test'
import AxeBuilder from '@axe-core/playwright'

/**
 * Accessibility Tests (WCAG 2.1 AA)
 * Tests marked with @a11y tag
 */

test.describe('Accessibility @a11y', () => {
  test('homepage should not have any automatically detectable accessibility issues', async ({
    page,
  }) => {
    await page.goto('/')

    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze()

    expect(accessibilityScanResults.violations).toEqual([])
  })

  test('login page should not have accessibility issues', async ({ page }) => {
    await page.goto('/login')

    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze()

    expect(accessibilityScanResults.violations).toEqual([])
  })

  test('register page should not have accessibility issues', async ({ page }) => {
    await page.goto('/register')

    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze()

    expect(accessibilityScanResults.violations).toEqual([])
  })

  test('should have proper heading hierarchy', async ({ page }) => {
    await page.goto('/')

    // Get all headings
    const h1Count = await page.locator('h1').count()
    const h2Count = await page.locator('h2').count()

    // Should have exactly one h1
    expect(h1Count).toBe(1)

    // Should have some h2 headings
    expect(h2Count).toBeGreaterThan(0)
  })

  test('should support keyboard navigation', async ({ page }) => {
    await page.goto('/')

    // Tab through interactive elements
    await page.keyboard.press('Tab')

    // Skip link should be focused
    const skipLink = page.getByRole('link', { name: /Skip to main content/i })
    await expect(skipLink).toBeFocused()

    // Continue tabbing
    await page.keyboard.press('Tab')

    // Logo should be focused
    const logo = page.getByRole('link', { name: /Legally AI/i })
    await expect(logo).toBeFocused()
  })

  test('all images should have alt text', async ({ page }) => {
    await page.goto('/')

    const images = await page.locator('img').all()

    for (const image of images) {
      const alt = await image.getAttribute('alt')
      expect(alt).toBeDefined()
    }
  })

  test('form inputs should have labels', async ({ page }) => {
    await page.goto('/login')

    const inputs = await page.locator('input[type="text"], input[type="email"], input[type="password"]').all()

    for (const input of inputs) {
      const id = await input.getAttribute('id')
      if (id) {
        const label = page.locator(`label[for="${id}"]`)
        await expect(label).toBeVisible()
      }
    }
  })

  test('should have sufficient color contrast', async ({ page }) => {
    await page.goto('/')

    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2aa'])
      .include(['body'])
      .analyze()

    const contrastViolations = accessibilityScanResults.violations.filter(
      (v) => v.id === 'color-contrast'
    )

    expect(contrastViolations).toEqual([])
  })
})
