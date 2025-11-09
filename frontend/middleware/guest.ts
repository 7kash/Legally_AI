/**
 * Guest Middleware
 * Redirects authenticated users away from guest-only pages
 */

export default defineNuxtRouteMiddleware((to, from) => {
  const authStore = useAuthStore()

  // If user is already authenticated, redirect to upload page
  if (authStore.isAuthenticated) {
    return navigateTo('/upload')
  }
})
