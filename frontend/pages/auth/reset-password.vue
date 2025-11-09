<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 px-4 py-12 sm:px-6 lg:px-8 dark:bg-gray-900">
    <div class="w-full max-w-md">
      <!-- Header -->
      <div class="text-center">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
          Set New Password
        </h1>
        <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
          Enter your new password below
        </p>
      </div>

      <!-- Form -->
      <form
        class="mt-8 space-y-6"
        @submit.prevent="handleSubmit"
      >
        <!-- Error Alert -->
        <div
          v-if="error"
          role="alert"
          class="alert alert--error"
        >
          <svg
            class="h-5 w-5 flex-shrink-0"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 20 20"
            fill="currentColor"
            aria-hidden="true"
          >
            <path
              fill-rule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.28 7.22a.75.75 0 00-1.06 1.06L8.94 10l-1.72 1.72a.75.75 0 101.06 1.06L10 11.06l1.72 1.72a.75.75 0 101.06-1.06L11.06 10l1.72-1.72a.75.75 0 00-1.06-1.06L10 8.94 8.28 7.22z"
              clip-rule="evenodd"
            />
          </svg>
          <span>{{ error }}</span>
        </div>

        <div class="space-y-4">
          <!-- New Password field -->
          <div class="form-group">
            <label
              for="password"
              class="block text-sm font-medium text-gray-700 dark:text-gray-300"
            >
              New Password
            </label>
            <div class="relative">
              <input
                id="password"
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                name="password"
                autocomplete="new-password"
                required
                class="input pr-10"
                placeholder="At least 8 characters"
                @input="error = ''"
              >
              <button
                type="button"
                class="absolute inset-y-0 right-0 flex items-center pr-3"
                :aria-label="showPassword ? 'Hide password' : 'Show password'"
                @click="showPassword = !showPassword"
              >
                <svg
                  v-if="!showPassword"
                  class="h-5 w-5 text-gray-400"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                  aria-hidden="true"
                >
                  <path d="M10 12.5a2.5 2.5 0 100-5 2.5 2.5 0 000 5z" />
                  <path
                    fill-rule="evenodd"
                    d="M.664 10.59a1.651 1.651 0 010-1.186A10.004 10.004 0 0110 3c4.257 0 7.893 2.66 9.336 6.41.147.381.146.804 0 1.186A10.004 10.004 0 0110 17c-4.257 0-7.893-2.66-9.336-6.41zM14 10a4 4 0 11-8 0 4 4 0 018 0z"
                    clip-rule="evenodd"
                  />
                </svg>
                <svg
                  v-else
                  class="h-5 w-5 text-gray-400"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                  aria-hidden="true"
                >
                  <path
                    fill-rule="evenodd"
                    d="M3.28 2.22a.75.75 0 00-1.06 1.06l14.5 14.5a.75.75 0 101.06-1.06l-1.745-1.745a10.029 10.029 0 003.3-4.38 1.651 1.651 0 000-1.185A10.004 10.004 0 009.999 3a9.956 9.956 0 00-4.744 1.194L3.28 2.22zM7.752 6.69l1.092 1.092a2.5 2.5 0 013.374 3.373l1.091 1.092a4 4 0 00-5.557-5.557z"
                    clip-rule="evenodd"
                  />
                  <path
                    d="M10.748 13.93l2.523 2.523a9.987 9.987 0 01-3.27.547c-4.258 0-7.894-2.66-9.337-6.41a1.651 1.651 0 010-1.186A10.007 10.007 0 012.839 6.02L6.07 9.252a4 4 0 004.678 4.678z"
                  />
                </svg>
              </button>
            </div>
            <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
              Must be at least 8 characters long
            </p>
          </div>

          <!-- Confirm Password field -->
          <div class="form-group">
            <label
              for="confirm-password"
              class="block text-sm font-medium text-gray-700 dark:text-gray-300"
            >
              Confirm New Password
            </label>
            <input
              id="confirm-password"
              v-model="confirmPassword"
              :type="showPassword ? 'text' : 'password'"
              name="confirm-password"
              autocomplete="new-password"
              required
              class="input"
              placeholder="Re-enter your password"
              @input="error = ''"
            >
          </div>
        </div>

        <!-- Submit button -->
        <div>
          <button
            type="submit"
            class="btn btn--primary w-full"
            :disabled="loading || !isFormValid"
            :aria-busy="loading"
          >
            <span v-if="!loading">Reset Password</span>
            <span
              v-else
              class="flex items-center justify-center gap-2"
            >
              <span class="spinner" aria-hidden="true" />
              <span>Resetting...</span>
            </span>
          </button>
        </div>

        <!-- Back to login -->
        <div class="text-center">
          <NuxtLink
            to="/login"
            class="text-sm font-medium text-primary-600 hover:text-primary-500 focus:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 rounded dark:text-primary-400"
          >
            Back to login
          </NuxtLink>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'

/**
 * Reset Password Page
 * Allows users to set a new password using reset token
 */

definePageMeta({
  layout: false,
  middleware: 'guest',
})

const router = useRouter()
const route = useRoute()

const password = ref('')
const confirmPassword = ref('')
const showPassword = ref(false)
const loading = ref(false)
const error = ref('')

const token = computed(() => route.query.token as string || '')

const isFormValid = computed(() => {
  return (
    password.value.length >= 8 &&
    password.value === confirmPassword.value
  )
})

async function handleSubmit() {
  if (!isFormValid.value) {
    error.value = 'Please check your password and try again'
    return
  }

  if (!token.value) {
    error.value = 'Invalid reset token. Please request a new password reset link.'
    return
  }

  loading.value = true
  error.value = ''

  try {
    // Call API to reset password
    await $fetch('/auth/reset-password', {
      method: 'POST',
      body: {
        token: token.value,
        password: password.value,
      },
      baseURL: useRuntimeConfig().public.apiBase,
    })

    // Show success notification
    const { success } = useNotifications()
    success('Password reset successful', 'You can now login with your new password')

    // Track event
    const { $analytics } = useNuxtApp()
    $analytics.trackEvent('password_reset_completed')

    // Redirect to login
    await router.push('/login')
  } catch (err: any) {
    error.value = err.data?.detail || 'Failed to reset password. Please try again.'
  } finally {
    loading.value = false
  }
}

// Set page title
useHead({
  title: 'Reset Password',
})
</script>
