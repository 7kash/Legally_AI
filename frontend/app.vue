<template>
  <div id="app" class="min-h-screen bg-background">
    <!-- Skip to main content link for keyboard navigation (WCAG 2.1 AA) -->
    <a href="#main-content" class="skip-to-main">
      Skip to main content
    </a>

    <!-- Main application layout -->
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>

    <!-- Global notifications/toasts -->
    <NotificationContainer />
  </div>
</template>

<script setup lang="ts">
import { useHead } from '#app'

/**
 * Root Application Component
 * Sets up global meta tags, imports global styles, and provides layout structure
 */

// SEO and meta configuration
useHead({
  titleTemplate: (titleChunk) => {
    return titleChunk ? `${titleChunk} - Legally AI` : 'Legally AI - AI-Powered Contract Analysis'
  },
  meta: [
    { charset: 'utf-8' },
    { name: 'viewport', content: 'width=device-width, initial-scale=1' },
    {
      name: 'description',
      content:
        'Legally AI provides AI-powered contract analysis to help you understand legal documents quickly and accurately.',
    },
    { name: 'format-detection', content: 'telephone=no' },
    // Open Graph
    { property: 'og:type', content: 'website' },
    { property: 'og:title', content: 'Legally AI - AI-Powered Contract Analysis' },
    {
      property: 'og:description',
      content: 'AI-powered contract analysis to help you understand legal documents.',
    },
    // Twitter Card
    { name: 'twitter:card', content: 'summary_large_image' },
    { name: 'twitter:title', content: 'Legally AI' },
  ],
  link: [
    { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
    // Preconnect to API
    { rel: 'preconnect', href: import.meta.env.VITE_API_URL || 'http://localhost:8000' },
  ],
  htmlAttrs: {
    lang: 'en',
  },
})
</script>

<style lang="scss">
@import '@/assets/styles/variables.scss';
@import '@/assets/styles/main.scss';
@import '@/assets/styles/tailwind.css';
</style>
