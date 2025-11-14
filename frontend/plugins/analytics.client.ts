/**
 * Analytics Plugin
 * Tracks page views and user events
 */

export default defineNuxtPlugin((nuxtApp) => {
  const config = useRuntimeConfig()
  const router = useRouter()

  // Simple analytics tracking
  // In production, replace with Google Analytics, Plausible, or similar
  const trackPageView = (url: string) => {
    if (import.meta.client && config.public.enableAnalytics) {
      // Example: Google Analytics
      // if (window.gtag) {
      //   window.gtag('config', config.public.gaTrackingId, {
      //     page_path: url,
      //   })
      // }

      // Example: Plausible
      // if (window.plausible) {
      //   window.plausible('pageview')
      // }

      // For now, just console log in development
      if (process.env.NODE_ENV === 'development') {
        console.log('[Analytics] Page view:', url)
      }
    }
  }

  const trackEvent = (eventName: string, properties?: Record<string, any>) => {
    if (import.meta.client && config.public.enableAnalytics) {
      // Example: Google Analytics
      // if (window.gtag) {
      //   window.gtag('event', eventName, properties)
      // }

      // Example: Plausible
      // if (window.plausible) {
      //   window.plausible(eventName, { props: properties })
      // }

      // For now, just console log in development
      if (process.env.NODE_ENV === 'development') {
        console.log('[Analytics] Event:', eventName, properties)
      }
    }
  }

  // Track initial page view
  trackPageView(router.currentRoute.value.fullPath)

  // Track route changes
  router.afterEach((to) => {
    trackPageView(to.fullPath)
  })

  // Provide analytics methods globally
  return {
    provide: {
      analytics: {
        trackPageView,
        trackEvent,
      },
    },
  }
})
