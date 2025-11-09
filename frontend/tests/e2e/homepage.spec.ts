import { test, expect } from '@playwright/test'

/**
 * Homepage E2E Tests
 */

test.describe('Homepage', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/')
  })

  test('should load successfully', async ({ page }) => {
    await expect(page).toHaveTitle(/Legally AI/)
  })

  test('should have main navigation', async ({ page }) => {
    const nav = page.getByRole('navigation', { name: 'Main navigation' })
    await expect(nav).toBeVisible()

    // Check for logo
    const logo = page.getByRole('link', { name: /Legally AI/i })
    await expect(logo).toBeVisible()
  })

  test('should have login and register buttons for unauthenticated users', async ({ page }) => {
    const loginButton = page.getByRole('link', { name: /Login/i })
    const registerButton = page.getByRole('link', { name: /Get Started/i })

    await expect(loginButton).toBeVisible()
    await expect(registerButton).toBeVisible()
  })

  test('should have skip to main content link', async ({ page }) => {
    const skipLink = page.getByRole('link', { name: /Skip to main content/i })
    await expect(skipLink).toBeInViewport({ ratio: 0 }) // Hidden by default
  })

  test('should navigate to login page', async ({ page }) => {
    await page.getByRole('link', { name: /Login/i }).click()
    await expect(page).toHaveURL(/\/login/)
  })

  test('should navigate to register page', async ({ page }) => {
    await page.getByRole('link', { name: /Get Started/i }).click()
    await expect(page).toHaveURL(/\/register/)
  })

  test('should be responsive on mobile', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 })
    await expect(page.getByRole('navigation')).toBeVisible()

    // Mobile menu button should be visible
    const mobileMenuButton = page.getByRole('button', { name: /Toggle mobile menu/i })
    await expect(mobileMenuButton).toBeVisible()
  })
})
