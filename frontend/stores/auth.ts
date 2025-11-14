import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

/**
 * Authentication Store
 * Manages user authentication state and operations
 */

export interface User {
  id: string
  email: string
  tier: 'free' | 'premium'
  contracts_analyzed: number
  analyses_remaining: number
  created_at: string
}

export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterData {
  email: string
  password: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
  user: User
}

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<User | null>(null)
  const token = ref<string | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Computed
  const isAuthenticated = computed(() => !!token.value && !!user.value)
  const isFreeUser = computed(() => user.value?.tier === 'free')
  const isPremiumUser = computed(() => user.value?.tier === 'premium')
  const hasAnalysesRemaining = computed(() => {
    if (!user.value) return false
    return user.value.tier === 'premium' || user.value.analyses_remaining > 0
  })

  // Actions
  async function register(data: RegisterData): Promise<void> {
    loading.value = true
    error.value = null

    try {
      const response = await $fetch<AuthResponse>('/auth/register', {
        method: 'POST',
        body: data,
        baseURL: useRuntimeConfig().public.apiBase,
      })

      token.value = response.access_token
      user.value = response.user

      // Store token in localStorage
      if (import.meta.client) {
        localStorage.setItem('auth_token', response.access_token)
      }
    } catch (err: any) {
      error.value = err.data?.detail || 'Registration failed'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function login(credentials: LoginCredentials): Promise<void> {
    loading.value = true
    error.value = null

    try {
      const response = await $fetch<AuthResponse>('/auth/login', {
        method: 'POST',
        body: credentials,
        baseURL: useRuntimeConfig().public.apiBase,
      })

      token.value = response.access_token
      user.value = response.user

      // Store token in localStorage
      if (import.meta.client) {
        localStorage.setItem('auth_token', response.access_token)
      }
    } catch (err: any) {
      error.value = err.data?.detail || 'Login failed'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function logout(): Promise<void> {
    try {
      // Call logout endpoint
      await $fetch('/auth/logout', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token.value}`,
        },
        baseURL: useRuntimeConfig().public.apiBase,
      })
    } catch (err) {
      // Ignore logout errors
      console.error('Logout error:', err)
    } finally {
      // Clear state
      user.value = null
      token.value = null
      error.value = null

      // Clear localStorage
      if (import.meta.client) {
        localStorage.removeItem('auth_token')
      }
    }
  }

  async function fetchCurrentUser(): Promise<void> {
    if (!token.value) return

    loading.value = true
    error.value = null

    try {
      const response = await $fetch<User>('/auth/me', {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${token.value}`,
        },
        baseURL: useRuntimeConfig().public.apiBase,
      })

      user.value = response
    } catch (err: any) {
      error.value = err.data?.detail || 'Failed to fetch user'
      // Clear invalid token
      token.value = null
      if (import.meta.client) {
        localStorage.removeItem('auth_token')
      }
    } finally {
      loading.value = false
    }
  }

  function initializeAuth(): void {
    // Restore token from localStorage
    if (import.meta.client) {
      const savedToken = localStorage.getItem('auth_token')
      if (savedToken) {
        token.value = savedToken
        // Fetch current user data
        fetchCurrentUser()
      }
    }
  }

  function clearError(): void {
    error.value = null
  }

  return {
    // State
    user,
    token,
    loading,
    error,
    // Computed
    isAuthenticated,
    isFreeUser,
    isPremiumUser,
    hasAnalysesRemaining,
    // Actions
    register,
    login,
    logout,
    fetchCurrentUser,
    initializeAuth,
    clearError,
  }
})
