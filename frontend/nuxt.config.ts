// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  // Modern mode
  future: {
    compatibilityVersion: 4,
  },

  // TypeScript
  typescript: {
    strict: true,
    typeCheck: true,
  },

  // Modules
  modules: [
    '@nuxtjs/tailwindcss',
    '@pinia/nuxt',
    '@vueuse/nuxt',
    '@nuxt/devtools',
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
