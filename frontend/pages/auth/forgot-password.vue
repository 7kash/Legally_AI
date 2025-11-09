<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 px-4 py-12 sm:px-6 lg:px-8 dark:bg-gray-900">
    <div class="w-full max-w-md">
      <!-- Header -->
      <div class="text-center">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
          Reset Password
        </h1>
        <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
          Enter your email address and we'll send you a link to reset your password
        </p>
      </div>

      <!-- Form or Success Message -->
      <div v-if="!emailSent" class="mt-8">
        <form
          class="space-y-6"
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

          <!-- Email field -->
          <div class="form-group">
            <label
              for="email"
              class="block text-sm font-medium text-gray-700 dark:text-gray-300"
            >
              Email address
            </label>
            <input
              id="email"
              v-model="email"
              type="email"
              name="email"
              autocomplete="email"
              required
              class="input"
              placeholder="you@example.com"
              @input="error = ''"
            >
          </div>

          <!-- Submit button -->
          <div>
            <button
              type="submit"
              class="btn btn--primary w-full"
              :disabled="loading || !email"
              :aria-busy="loading"
            >
              <span v-if="!loading">Send Reset Link</span>
              <span
                v-else
                class="flex items-center justify-center gap-2"
              >
                <span class="spinner" aria-hidden="true" />
                <span>Sending...</span>
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

      <!-- Success Message -->
      <div v-else class="mt-8 text-center">
        <div class="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-green-100 dark:bg-green-900">
          <svg
            class="h-6 w-6 text-green-600 dark:text-green-400"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            aria-hidden="true"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M5 13l4 4L19 7"
            />
          </svg>
        </div>
        <h2 class="mt-4 text-lg font-semibold text-gray-900 dark:text-white">
          Check your email
        </h2>
        <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
          We've sent a password reset link to <strong>{{ email }}</strong>
        </p>
        <p class="mt-4 text-xs text-gray-500 dark:text-gray-500">
          Didn't receive the email? Check your spam folder or
          <button
            type="button"
            class="text-primary-600 hover:text-primary-500 dark:text-primary-400"
            @click="resendEmail"
          >
            resend
          </button>
        </p>
        <div class="mt-6">
          <NuxtLink
            to="/login"
            class="btn btn--secondary w-full"
          >
            Back to login
          </NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

/**
 * Forgot Password Page
 * Allows users to request password reset email
 */

definePageMeta({
  layout: false,
  middleware: 'guest',
})

const email = ref('')
const loading = ref(false)
const error = ref('')
const emailSent = ref(false)

async function handleSubmit() {
  if (!email.value) return

  loading.value = true
  error.value = ''

  try {
    // TODO: Call API to send password reset email
    // await $fetch('/auth/forgot-password', {
    //   method: 'POST',
    //   body: { email: email.value },
    //   baseURL: useRuntimeConfig().public.apiBase,
    // })

    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 1500))

    emailSent.value = true

    // Track event
    const { $analytics } = useNuxtApp()
    $analytics.trackEvent('password_reset_requested', { email: email.value })
  } catch (err: any) {
    error.value = err.data?.detail || 'Failed to send reset email. Please try again.'
  } finally {
    loading.value = false
  }
}

async function resendEmail() {
  emailSent.value = false
  await handleSubmit()
}

// Set page title
useHead({
  title: 'Reset Password',
})
</script>
