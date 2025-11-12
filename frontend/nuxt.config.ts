// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  // Modern mode
  future: {
    compatibilityVersion: 4,
  },

  // TypeScript
  typescript: {
    strict: true,
    typeCheck: false, // Disabled temporarily to avoid build issues
  },

  // Modules
  modules: [
    '@nuxtjs/tailwindcss',
    '@pinia/nuxt',
    '@vueuse/nuxt',
    '@nuxt/devtools',
    '@nuxtjs/i18n',
    '@vite-pwa/nuxt',
  ],

  // App configuration
  app: {
    head: {
      charset: 'utf-8',
      viewport: 'width=device-width, initial-scale=1',
      title: 'Legally AI - Contract Analysis',
      meta: [
        {
          name: 'description',
          content:
            'AI-powered multilingual contract analysis in Russian, Serbian, French, and English',
        },
        { name: 'format-detection', content: 'telephone=no' },
        // Open Graph
        { property: 'og:title', content: 'Legally AI - Contract Analysis' },
        {
          property: 'og:description',
          content: 'AI-powered multilingual contract analysis',
        },
        { property: 'og:type', content: 'website' },
        // Twitter
        { name: 'twitter:card', content: 'summary_large_image' },
      ],
      link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }],
    },
    // Performance optimization
    pageTransition: { name: 'page', mode: 'out-in' },
    layoutTransition: { name: 'layout', mode: 'out-in' },
  },

  // CSS
  css: ['~/assets/styles/main.scss'],

  // Runtime config
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000/api',
      appVersion: '1.0.0',
      enableAnalytics: process.env.NUXT_PUBLIC_ENABLE_ANALYTICS === 'true',
    },
  },

  // Build optimization
  build: {
    transpile: [],
  },

  // Vite configuration
  vite: {
    css: {
      preprocessorOptions: {
        scss: {
          additionalData: '@use "~/assets/styles/variables.scss" as *;',
        },
      },
    },
    build: {
      // Code splitting
      rollupOptions: {
        output: {
          manualChunks: {
            vendor: ['vue', 'vue-router', 'pinia'],
          },
        },
      },
      // Minification
      minify: 'terser',
      terserOptions: {
        compress: {
          drop_console: process.env.NODE_ENV === 'production',
        },
      },
    },
  },

  // Tailwind
  tailwindcss: {
    cssPath: '~/assets/styles/tailwind.css',
    configPath: 'tailwind.config.ts',
    exposeConfig: false,
    viewer: true,
  },

  // i18n
  i18n: {
    strategy: 'no_prefix',
    detectBrowserLanguage: {
      useCookie: true,
      cookieKey: 'legally_ai_locale',
      redirectOn: 'root',
      alwaysRedirect: false,
    },
    locales: [
      { code: 'en', iso: 'en-US', name: 'English' },
      { code: 'ru', iso: 'ru-RU', name: 'Русский' },
      { code: 'fr', iso: 'fr-FR', name: 'Français' },
      { code: 'sr', iso: 'sr-RS', name: 'Српски' },
    ],
    defaultLocale: 'en',
    vueI18n: './i18n.config.ts',
  },

  // PWA
  pwa: {
    registerType: 'autoUpdate',
    manifest: {
      name: 'Legally AI - Contract Analysis',
      short_name: 'Legally AI',
      description: 'AI-powered multilingual contract analysis',
      theme_color: '#0ea5e9',
      background_color: '#ffffff',
      display: 'standalone',
      icons: [
        {
          src: '/icons/icon-192x192.png',
          sizes: '192x192',
          type: 'image/png',
        },
        {
          src: '/icons/icon-512x512.png',
          sizes: '512x512',
          type: 'image/png',
        },
      ],
    },
    workbox: {
      navigateFallback: '/',
      globPatterns: ['**/*.{js,css,html,png,svg,ico}'],
      runtimeCaching: [
        {
          urlPattern: /^https:\/\/.*\/api\/.*/i,
          handler: 'NetworkFirst',
          options: {
            cacheName: 'api-cache',
            expiration: {
              maxEntries: 50,
              maxAgeSeconds: 3600,
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
              maxAgeSeconds: 86400 * 30,
            },
          },
        },
      ],
    },
    client: {
      installPrompt: true,
      periodicSyncForUpdates: 3600,
    },
    devOptions: {
      enabled: false,
      type: 'module',
    },
  },

  // Performance
  experimental: {
    payloadExtraction: true,
    renderJsonPayloads: true,
    viewTransition: true,
  },

  // Nitro (server)
  nitro: {
    compressPublicAssets: true,
    prerender: {
      crawlLinks: true,
      routes: ['/'],
    },
  },

  // Security headers
  routeRules: {
    '/**': {
      headers: {
        'X-Frame-Options': 'SAMEORIGIN',
        'X-Content-Type-Options': 'nosniff',
        'Referrer-Policy': 'strict-origin-when-cross-origin',
        'Permissions-Policy': 'camera=(), microphone=(), geolocation=()',
      },
    },
  },

  // DevTools
  devtools: {
    enabled: true,
  },

  // Compatibility
  compatibilityDate: '2024-01-09',
})
