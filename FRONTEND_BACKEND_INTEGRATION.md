# Frontend-Backend Integration Code Guide

This document provides the exact code changes needed to connect the Nuxt 3 frontend to the FastAPI backend.

---

## Table of Contents

1. [Authentication Integration](#authentication-integration)
2. [Contract Upload Integration](#contract-upload-integration)
3. [Analysis Integration](#analysis-integration)
4. [SSE Real-time Updates](#sse-real-time-updates)
5. [Password Reset Integration](#password-reset-integration)
6. [Email Verification Integration](#email-verification-integration)

---

## Authentication Integration

### File: `stores/auth.ts`

Replace the TODO placeholders with actual API calls:

```typescript
// frontend/stores/auth.ts
import { defineStore } from 'pinia'
import type { User, LoginCredentials, RegisterData } from '~/types'

interface AuthState {
  user: User | null
  token: string | null
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: null,
    token: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token && !!state.user,
    currentUser: (state) => state.user,
  },

  actions: {
    // LOGIN
    async login(credentials: LoginCredentials) {
      try {
        const config = useRuntimeConfig()
        const response = await $fetch<{ access_token: string; user: User }>('/auth/login', {
          method: 'POST',
          body: credentials,
          baseURL: config.public.apiBase,
        })

        this.token = response.access_token
        this.user = response.user

        // Store token in localStorage for persistence
        if (process.client) {
          localStorage.setItem('auth_token', response.access_token)
          localStorage.setItem('auth_user', JSON.stringify(response.user))
        }

        return response
      } catch (error: any) {
        console.error('Login error:', error)
        throw new Error(error.data?.detail || 'Login failed')
      }
    },

    // REGISTER
    async register(data: RegisterData) {
      try {
        const config = useRuntimeConfig()
        const response = await $fetch<{ access_token: string; user: User }>('/auth/register', {
          method: 'POST',
          body: data,
          baseURL: config.public.apiBase,
        })

        this.token = response.access_token
        this.user = response.user

        // Store token in localStorage
        if (process.client) {
          localStorage.setItem('auth_token', response.access_token)
          localStorage.setItem('auth_user', JSON.stringify(response.user))
        }

        return response
      } catch (error: any) {
        console.error('Registration error:', error)
        throw new Error(error.data?.detail || 'Registration failed')
      }
    },

    // LOGOUT
    async logout() {
      try {
        const config = useRuntimeConfig()

        if (this.token) {
          await $fetch('/auth/logout', {
            method: 'POST',
            baseURL: config.public.apiBase,
            headers: {
              Authorization: `Bearer ${this.token}`,
            },
          })
        }
      } catch (error) {
        console.error('Logout error:', error)
      } finally {
        // Clear state regardless of API call success
        this.token = null
        this.user = null

        if (process.client) {
          localStorage.removeItem('auth_token')
          localStorage.removeItem('auth_user')
        }

        // Redirect to login
        await navigateTo('/login')
      }
    },

    // CHECK AUTH (called on app init)
    async checkAuth() {
      if (process.client) {
        const token = localStorage.getItem('auth_token')
        const userStr = localStorage.getItem('auth_user')

        if (token && userStr) {
          try {
            const config = useRuntimeConfig()
            // Verify token is still valid by fetching user
            const user = await $fetch<User>('/auth/me', {
              method: 'GET',
              baseURL: config.public.apiBase,
              headers: {
                Authorization: `Bearer ${token}`,
              },
            })

            this.token = token
            this.user = user
            return true
          } catch (error) {
            // Token invalid, clear storage
            localStorage.removeItem('auth_token')
            localStorage.removeItem('auth_user')
            this.token = null
            this.user = null
            return false
          }
        }
      }
      return false
    },

    // REFRESH TOKEN (if using refresh tokens)
    async refreshToken() {
      try {
        const config = useRuntimeConfig()
        const response = await $fetch<{ access_token: string }>('/auth/refresh', {
          method: 'POST',
          baseURL: config.public.apiBase,
          headers: {
            Authorization: `Bearer ${this.token}`,
          },
        })

        this.token = response.access_token

        if (process.client) {
          localStorage.setItem('auth_token', response.access_token)
        }

        return response.access_token
      } catch (error) {
        // Refresh failed, logout
        await this.logout()
        throw error
      }
    },
  },
})
```

---

## Contract Upload Integration

### File: `stores/contracts.ts`

```typescript
// frontend/stores/contracts.ts
import { defineStore } from 'pinia'
import { useAuthStore } from './auth'
import type { Contract } from '~/types'

interface ContractState {
  contracts: Contract[]
  currentContract: Contract | null
  uploadProgress: number
  isUploading: boolean
}

export const useContractStore = defineStore('contracts', {
  state: (): ContractState => ({
    contracts: [],
    currentContract: null,
    uploadProgress: 0,
    isUploading: false,
  }),

  actions: {
    // UPLOAD CONTRACT
    async uploadContract(file: File) {
      const authStore = useAuthStore()
      const config = useRuntimeConfig()

      if (!authStore.token) {
        throw new Error('Not authenticated')
      }

      try {
        this.isUploading = true
        this.uploadProgress = 0

        const formData = new FormData()
        formData.append('file', file)

        const response = await $fetch<{ contract_id: string; task_id: string }>('/contracts/upload', {
          method: 'POST',
          body: formData,
          baseURL: config.public.apiBase,
          headers: {
            Authorization: `Bearer ${authStore.token}`,
          },
          onUploadProgress: (progressEvent: ProgressEvent) => {
            if (progressEvent.lengthComputable) {
              this.uploadProgress = Math.round((progressEvent.loaded * 100) / progressEvent.total)
            }
          },
        })

        return response
      } catch (error: any) {
        console.error('Upload error:', error)
        throw new Error(error.data?.detail || 'Upload failed')
      } finally {
        this.isUploading = false
        this.uploadProgress = 0
      }
    },

    // FETCH CONTRACTS (history)
    async fetchContracts() {
      const authStore = useAuthStore()
      const config = useRuntimeConfig()

      if (!authStore.token) {
        throw new Error('Not authenticated')
      }

      try {
        const response = await $fetch<Contract[]>('/contracts', {
          method: 'GET',
          baseURL: config.public.apiBase,
          headers: {
            Authorization: `Bearer ${authStore.token}`,
          },
        })

        this.contracts = response
        return response
      } catch (error: any) {
        console.error('Fetch contracts error:', error)
        throw new Error(error.data?.detail || 'Failed to fetch contracts')
      }
    },

    // GET CONTRACT BY ID
    async getContract(id: string) {
      const authStore = useAuthStore()
      const config = useRuntimeConfig()

      if (!authStore.token) {
        throw new Error('Not authenticated')
      }

      try {
        const response = await $fetch<Contract>(`/contracts/${id}`, {
          method: 'GET',
          baseURL: config.public.apiBase,
          headers: {
            Authorization: `Bearer ${authStore.token}`,
          },
        })

        this.currentContract = response
        return response
      } catch (error: any) {
        console.error('Get contract error:', error)
        throw new Error(error.data?.detail || 'Failed to fetch contract')
      }
    },

    // DELETE CONTRACT
    async deleteContract(id: string) {
      const authStore = useAuthStore()
      const config = useRuntimeConfig()

      if (!authStore.token) {
        throw new Error('Not authenticated')
      }

      try {
        await $fetch(`/contracts/${id}`, {
          method: 'DELETE',
          baseURL: config.public.apiBase,
          headers: {
            Authorization: `Bearer ${authStore.token}`,
          },
        })

        // Remove from local state
        this.contracts = this.contracts.filter(c => c.id !== id)
      } catch (error: any) {
        console.error('Delete contract error:', error)
        throw new Error(error.data?.detail || 'Failed to delete contract')
      }
    },

    // TRIGGER ANALYSIS
    async triggerAnalysis(contractId: string) {
      const authStore = useAuthStore()
      const config = useRuntimeConfig()

      if (!authStore.token) {
        throw new Error('Not authenticated')
      }

      try {
        const response = await $fetch<{ analysis_id: string; task_id: string }>(`/contracts/${contractId}/analyze`, {
          method: 'POST',
          baseURL: config.public.apiBase,
          headers: {
            Authorization: `Bearer ${authStore.token}`,
          },
        })

        return response
      } catch (error: any) {
        console.error('Trigger analysis error:', error)
        throw new Error(error.data?.detail || 'Failed to trigger analysis')
      }
    },
  },
})
```

---

## Analysis Integration

### File: `stores/analyses.ts`

```typescript
// frontend/stores/analyses.ts
import { defineStore } from 'pinia'
import { useAuthStore } from './auth'
import type { Analysis, AnalysisEvent } from '~/types'

interface AnalysisState {
  currentAnalysis: Analysis | null
  events: AnalysisEvent[]
  eventSource: EventSource | null
  isConnected: boolean
  progress: number
  status: string
}

export const useAnalysisStore = defineStore('analyses', {
  state: (): AnalysisState => ({
    currentAnalysis: null,
    events: [],
    eventSource: null,
    isConnected: false,
    progress: 0,
    status: 'idle',
  }),

  actions: {
    // CONNECT TO SSE
    connectSSE(analysisId: string) {
      const authStore = useAuthStore()
      const config = useRuntimeConfig()

      if (!authStore.token) {
        throw new Error('Not authenticated')
      }

      if (this.eventSource) {
        this.disconnectSSE()
      }

      const baseURL = config.public.apiBase.replace('/api', '') // Remove /api for SSE
      const url = `${baseURL}/api/analyses/${analysisId}/stream?token=${authStore.token}`

      this.eventSource = new EventSource(url)
      this.events = []

      this.eventSource.onopen = () => {
        console.log('SSE connected')
        this.isConnected = true
      }

      this.eventSource.onmessage = (event) => {
        try {
          const data: AnalysisEvent = JSON.parse(event.data)
          this.events.push(data)

          // Update progress based on event type
          switch (data.type) {
            case 'parsing':
              this.progress = 10
              this.status = 'Parsing document...'
              break
            case 'preparation':
              this.progress = 40
              this.status = 'Preparing analysis...'
              break
            case 'analysis':
              this.progress = 80
              this.status = 'Analyzing contract...'
              break
            case 'formatting':
              this.progress = 95
              this.status = 'Formatting results...'
              break
            case 'completed':
              this.progress = 100
              this.status = 'Analysis complete!'
              this.disconnectSSE()
              break
            case 'error':
              this.status = 'Error occurred'
              this.disconnectSSE()
              break
          }

          console.log('SSE event:', data)
        } catch (error) {
          console.error('Error parsing SSE event:', error)
        }
      }

      this.eventSource.onerror = (error) => {
        console.error('SSE error:', error)
        this.isConnected = false
        this.disconnectSSE()
      }
    },

    // DISCONNECT SSE
    disconnectSSE() {
      if (this.eventSource) {
        this.eventSource.close()
        this.eventSource = null
        this.isConnected = false
      }
    },

    // FETCH ANALYSIS RESULTS
    async fetchAnalysis(id: string) {
      const authStore = useAuthStore()
      const config = useRuntimeConfig()

      if (!authStore.token) {
        throw new Error('Not authenticated')
      }

      try {
        const response = await $fetch<Analysis>(`/analyses/${id}`, {
          method: 'GET',
          baseURL: config.public.apiBase,
          headers: {
            Authorization: `Bearer ${authStore.token}`,
          },
        })

        this.currentAnalysis = response
        return response
      } catch (error: any) {
        console.error('Fetch analysis error:', error)
        throw new Error(error.data?.detail || 'Failed to fetch analysis')
      }
    },

    // SUBMIT FEEDBACK
    async submitFeedback(analysisId: string, sectionKey: string, isCorrect: boolean, comment?: string) {
      const authStore = useAuthStore()
      const config = useRuntimeConfig()

      if (!authStore.token) {
        throw new Error('Not authenticated')
      }

      try {
        await $fetch(`/analyses/${analysisId}/feedback`, {
          method: 'POST',
          body: {
            section: sectionKey,
            is_correct: isCorrect,
            comment,
          },
          baseURL: config.public.apiBase,
          headers: {
            Authorization: `Bearer ${authStore.token}`,
          },
        })
      } catch (error: any) {
        console.error('Submit feedback error:', error)
        throw new Error(error.data?.detail || 'Failed to submit feedback')
      }
    },

    // EXPORT ANALYSIS
    async exportAnalysis(analysisId: string, format: 'pdf' | 'docx') {
      const authStore = useAuthStore()
      const config = useRuntimeConfig()

      if (!authStore.token) {
        throw new Error('Not authenticated')
      }

      try {
        const response = await $fetch(`/analyses/${analysisId}/export/${format}`, {
          method: 'GET',
          baseURL: config.public.apiBase,
          headers: {
            Authorization: `Bearer ${authStore.token}`,
          },
          responseType: 'blob',
        })

        // Trigger download
        if (process.client && response instanceof Blob) {
          const url = URL.createObjectURL(response)
          const link = document.createElement('a')
          link.href = url
          link.download = `analysis-${analysisId}.${format}`
          document.body.appendChild(link)
          link.click()
          document.body.removeChild(link)
          URL.revokeObjectURL(url)
        }

        return response
      } catch (error: any) {
        console.error('Export analysis error:', error)
        throw new Error(error.data?.detail || 'Failed to export analysis')
      }
    },
  },
})
```

---

## SSE Real-time Updates

### Usage in Component

```vue
<!-- pages/analysis/[id].vue -->
<script setup lang="ts">
const route = useRoute()
const analysisStore = useAnalysisStore()
const { success, error } = useNotifications()

const analysisId = computed(() => route.params.id as string)

onMounted(async () => {
  try {
    // Connect to SSE for real-time updates
    analysisStore.connectSSE(analysisId.value)

    // Also fetch the analysis data
    await analysisStore.fetchAnalysis(analysisId.value)
  } catch (err: any) {
    error('Failed to load analysis', err.message)
  }
})

onBeforeUnmount(() => {
  // Clean up SSE connection
  analysisStore.disconnectSSE()
})
</script>

<template>
  <div>
    <!-- Progress Bar -->
    <div v-if="analysisStore.isConnected" class="progress-bar">
      <div class="progress-fill" :style="{ width: `${analysisStore.progress}%` }"></div>
      <span>{{ analysisStore.status }}</span>
    </div>

    <!-- Event Timeline -->
    <div class="events-timeline">
      <div v-for="(event, index) in analysisStore.events" :key="index" class="event">
        <span class="event-type">{{ event.type }}</span>
        <span class="event-time">{{ new Date(event.timestamp).toLocaleTimeString() }}</span>
        <p v-if="event.message">{{ event.message }}</p>
      </div>
    </div>

    <!-- Analysis Results (when complete) -->
    <div v-if="analysisStore.currentAnalysis" class="results">
      <!-- Display analysis sections here -->
    </div>
  </div>
</template>
```

---

## Password Reset Integration

### File: `pages/auth/forgot-password.vue`

```vue
<!-- pages/auth/forgot-password.vue -->
<script setup lang="ts">
const email = ref('')
const loading = ref(false)
const emailSent = ref(false)
const { success, error } = useNotifications()
const config = useRuntimeConfig()

async function handleSubmit() {
  loading.value = true
  try {
    await $fetch('/auth/forgot-password', {
      method: 'POST',
      body: { email: email.value },
      baseURL: config.public.apiBase,
    })

    emailSent.value = true
    success('Email sent', 'Check your inbox for password reset instructions')
  } catch (err: any) {
    error('Failed to send email', err.data?.detail || 'Please try again')
  } finally {
    loading.value = false
  }
}
</script>
```

### File: `pages/auth/reset-password.vue`

```vue
<!-- pages/auth/reset-password.vue -->
<script setup lang="ts">
const route = useRoute()
const router = useRouter()
const password = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const { success, error } = useNotifications()
const config = useRuntimeConfig()

const token = computed(() => route.query.token as string)

const isFormValid = computed(() => {
  return password.value.length >= 8 && password.value === confirmPassword.value
})

async function handleSubmit() {
  if (!isFormValid.value) return

  loading.value = true
  try {
    await $fetch('/auth/reset-password', {
      method: 'POST',
      body: {
        token: token.value,
        new_password: password.value,
      },
      baseURL: config.public.apiBase,
    })

    success('Password reset', 'You can now login with your new password')
    await router.push('/login')
  } catch (err: any) {
    error('Failed to reset password', err.data?.detail || 'Please try again')
  } finally {
    loading.value = false
  }
}
</script>
```

---

## Email Verification Integration

### File: `pages/auth/verify-email.vue`

```vue
<!-- pages/auth/verify-email.vue -->
<script setup lang="ts">
const route = useRoute()
const router = useRouter()
const loading = ref(true)
const verified = ref(false)
const errorMessage = ref('')
const { success, error: showError } = useNotifications()
const config = useRuntimeConfig()

const token = computed(() => route.query.token as string)

async function verifyEmail() {
  loading.value = true
  try {
    await $fetch('/auth/verify-email', {
      method: 'POST',
      body: { token: token.value },
      baseURL: config.public.apiBase,
    })

    verified.value = true
    success('Email verified!', 'Your account is now active')
  } catch (err: any) {
    errorMessage.value = err.data?.detail || 'Verification failed'
    showError('Verification failed', errorMessage.value)
  } finally {
    loading.value = false
  }
}

async function resendVerification() {
  try {
    await $fetch('/auth/resend-verification', {
      method: 'POST',
      baseURL: config.public.apiBase,
    })

    success('Email sent', 'Check your inbox for a new verification link')
  } catch (err: any) {
    showError('Failed to resend', err.data?.detail || 'Please try again')
  }
}

onMounted(() => {
  if (token.value) {
    verifyEmail()
  } else {
    loading.value = false
    errorMessage.value = 'No verification token provided'
  }
})
</script>

<template>
  <div class="verify-email-container">
    <!-- Loading State -->
    <div v-if="loading" class="loading">
      <SkeletonLoader variant="circle" width="64px" height="64px" />
      <p>Verifying your email...</p>
    </div>

    <!-- Success State -->
    <div v-else-if="verified" class="success">
      <h2>Email Verified!</h2>
      <p>Your account is now active. You can start analyzing contracts.</p>
      <NuxtLink to="/upload" class="btn btn--primary">
        Start Analyzing Contracts
      </NuxtLink>
    </div>

    <!-- Error State -->
    <div v-else class="error">
      <h2>Verification Failed</h2>
      <p>{{ errorMessage }}</p>
      <button @click="resendVerification" class="btn btn--secondary">
        Resend Verification Email
      </button>
      <NuxtLink to="/login" class="btn btn--ghost">
        Back to Login
      </NuxtLink>
    </div>
  </div>
</template>
```

---

## Error Handling Best Practices

### Global Error Handler

```typescript
// plugins/api-error-handler.client.ts
export default defineNuxtPlugin(() => {
  const { error } = useNotifications()

  // Global error handler for fetch errors
  $fetch.create({
    onResponseError({ response }) {
      if (response.status === 401) {
        error('Unauthorized', 'Please login again')
        navigateTo('/login')
      } else if (response.status === 403) {
        error('Forbidden', 'You do not have permission for this action')
      } else if (response.status === 429) {
        error('Rate limited', 'Too many requests. Please try again later')
      } else if (response.status >= 500) {
        error('Server error', 'Something went wrong. Please try again')
      }
    },
  })
})
```

### Retry Logic for Failed Requests

```typescript
// utils/fetchWithRetry.ts
export async function fetchWithRetry<T>(
  url: string,
  options: any = {},
  maxRetries = 3
): Promise<T> {
  let lastError: Error

  for (let i = 0; i < maxRetries; i++) {
    try {
      return await $fetch<T>(url, options)
    } catch (error: any) {
      lastError = error

      // Don't retry on 4xx errors
      if (error.status >= 400 && error.status < 500) {
        throw error
      }

      // Wait before retrying (exponential backoff)
      if (i < maxRetries - 1) {
        await new Promise(resolve => setTimeout(resolve, Math.pow(2, i) * 1000))
      }
    }
  }

  throw lastError!
}
```

---

## Testing the Integration

### Manual Test Script

```typescript
// test-integration.ts
async function testIntegration() {
  const config = useRuntimeConfig()
  const baseURL = config.public.apiBase

  console.log('Testing backend integration...')

  // Test 1: Health check
  try {
    await $fetch('/health', { baseURL })
    console.log('✅ Backend is running')
  } catch {
    console.error('❌ Backend not reachable')
    return
  }

  // Test 2: Register
  try {
    const { access_token } = await $fetch('/auth/register', {
      method: 'POST',
      body: {
        email: 'test@example.com',
        password: 'TestPassword123',
      },
      baseURL,
    })
    console.log('✅ Registration works')
  } catch {
    console.log('⚠️ User might already exist, trying login...')
  }

  // Test 3: Login
  let token: string
  try {
    const response = await $fetch('/auth/login', {
      method: 'POST',
      body: {
        email: 'test@example.com',
        password: 'TestPassword123',
      },
      baseURL,
    })
    token = response.access_token
    console.log('✅ Login works')
  } catch {
    console.error('❌ Login failed')
    return
  }

  // Test 4: Authenticated request
  try {
    await $fetch('/auth/me', {
      baseURL,
      headers: { Authorization: `Bearer ${token}` },
    })
    console.log('✅ Authentication works')
  } catch {
    console.error('❌ Authentication failed')
  }

  console.log('Integration test complete!')
}
```

---

## Next Steps

After implementing these integrations:

1. **Test each endpoint individually** using the manual test scripts
2. **Test the complete flow** from registration to analysis
3. **Monitor network requests** in browser DevTools
4. **Check SSE connection** in DevTools > Network > EventStream
5. **Verify error handling** by testing failure scenarios
6. **Run E2E tests** with Playwright

See `INTEGRATION_CHECKLIST.md` for the complete testing checklist.

---

**Last Updated**: 2025-11-09
**Version**: 1.0.0 (Phase 4 - Integration Ready)
