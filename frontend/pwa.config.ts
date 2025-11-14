import type { VitePWAOptions } from 'vite-plugin-pwa'

/**
 * PWA Configuration
 * Service Worker setup for offline support
 */

export const pwaOptions: Partial<VitePWAOptions> = {
  registerType: 'autoUpdate',
  includeAssets: ['favicon.ico', 'icon-192.png', 'icon-512.png'],

  manifest: {
    name: 'Legally AI - Contract Analysis',
    short_name: 'Legally AI',
    description: 'AI-powered contract analysis in multiple languages',
    theme_color: '#0ea5e9',
    background_color: '#ffffff',
    display: 'standalone',
    orientation: 'portrait',
    scope: '/',
    start_url: '/',
    icons: [
      {
        src: '/icon-192.png',
        sizes: '192x192',
        type: 'image/png',
        purpose: 'any maskable',
      },
      {
        src: '/icon-512.png',
        sizes: '512x512',
        type: 'image/png',
        purpose: 'any maskable',
      },
    ],
  },

  workbox: {
    // Cache strategies
    runtimeCaching: [
      {
        urlPattern: /^https:\/\/api\.*/i,
        handler: 'NetworkFirst',
        options: {
          cacheName: 'api-cache',
          expiration: {
            maxEntries: 50,
            maxAgeSeconds: 60 * 60, // 1 hour
          },
          cacheableResponse: {
            statuses: [0, 200],
          },
        },
      },
      {
        urlPattern: /\.(?:png|jpg|jpeg|svg|gif|webp)$/,
        handler: 'CacheFirst',
        options: {
          cacheName: 'image-cache',
          expiration: {
            maxEntries: 100,
            maxAgeSeconds: 60 * 60 * 24 * 30, // 30 days
          },
        },
      },
      {
        urlPattern: /\.(?:js|css)$/,
        handler: 'StaleWhileRevalidate',
        options: {
          cacheName: 'static-resources',
          expiration: {
            maxEntries: 60,
            maxAgeSeconds: 60 * 60 * 24 * 7, // 7 days
          },
        },
      },
    ],

    // Clean old caches
    cleanupOutdatedCaches: true,

    // Navigation fallback
    navigateFallback: '/',
    navigateFallbackDenylist: [/^\/api/],
  },

  devOptions: {
    enabled: false,
    type: 'module',
  },
}
