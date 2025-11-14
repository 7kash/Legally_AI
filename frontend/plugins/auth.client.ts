/**
 * Auth Plugin
 * Initializes authentication on app startup (client-side only)
 */

export default defineNuxtPlugin(() => {
  const authStore = useAuthStore()

  // Initialize auth from localStorage
  authStore.initializeAuth()
})
