<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 px-4 py-12 sm:px-6 lg:px-8 dark:bg-gray-900">
    <div class="w-full max-w-md text-center">
      <!-- Loading State -->
      <div v-if="loading" class="space-y-4">
        <div class="spinner mx-auto h-12 w-12" aria-hidden="true" />
        <h2 class="text-xl font-semibold text-gray-900 dark:text-white">
          Verifying your email...
        </h2>
        <p class="text-sm text-gray-600 dark:text-gray-400">
          Please wait while we verify your email address
        </p>
      </div>

      <!-- Success State -->
      <div v-else-if="verified && !error" class="space-y-6">
        <div class="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-green-100 dark:bg-green-900">
          <svg
            class="h-8 w-8 text-green-600 dark:text-green-400"
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
        <div>
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white">
            Email Verified!
          </h2>
          <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
            Your email has been successfully verified. You can now access all features.
          </p>
        </div>
        <div class="space-y-3">
          <NuxtLink
            to="/upload"
            class="btn btn--primary w-full"
          >
            Start Analyzing Contracts
          </NuxtLink>
          <NuxtLink
            to="/login"
            class="btn btn--secondary w-full"
          >
            Go to Login
          </NuxtLink>
        </div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="space-y-6">
        <div class="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-red-100 dark:bg-red-900">
          <svg
            class="h-8 w-8 text-red-600 dark:text-red-400"
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
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </div>
        <div>
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white">
            Verification Failed
          </h2>
          <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
            {{ error }}
          </p>
        </div>
        <div class="space-y-3">
          <button
            type="button"
            class="btn btn--primary w-full"
            :disabled="resending"
            @click="resendVerification"
          >
            <span v-if="!resending">Resend Verification Email</span>
            <span
              v-else
              class="flex items-center justify-center gap-2"
            >
              <span class="spinner" aria-hidden="true" />
              <span>Sending...</span>
            </span>
          </button>
          <NuxtLink
            to="/login"
            class="btn btn--secondary w-full"
          >
            Back to Login
          </NuxtLink>
        </div>
      </div>

      <!-- No Token State -->
      <div v-else class="space-y-6">
        <div class="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-blue-100 dark:bg-blue-900">
          <svg
            class="h-8 w-8 text-blue-600 dark:text-blue-400"
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
              d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
            />
          </svg>
        </div>
        <div>
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white">
            Check Your Email
          </h2>
          <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
            We've sent a verification link to your email address. Please click the link to verify your account.
          </p>
        </div>
        <div>
          <NuxtLink
            to="/login"
            class="btn btn--secondary w-full"
          >
            Back to Login
          </NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'

/**
 * Email Verification Page
 * Verifies user email using token from email link
 */

definePageMeta({
  layout: false,
})

const route = useRoute()

const loading = ref(false)
const verified = ref(false)
const error = ref('')
const resending = ref(false)

const token = computed(() => route.query.token as string || '')

onMounted(async () => {
  if (token.value) {
    await verifyEmail()
  }
})

async function verifyEmail() {
  loading.value = true
  error.value = ''

  try {
    // TODO: Call API to verify email
    // await $fetch('/auth/verify-email', {
    //   method: 'POST',
    //   body: { token: token.value },
    //   baseURL: useRuntimeConfig().public.apiBase,
    // })

    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 2000))

    verified.value = true

    // Show success notification
    const { success } = useNotifications()
    success('Email verified!', 'Your account has been verified successfully')

    // Track event
    const { $analytics } = useNuxtApp()
    $analytics.trackEvent('email_verified')
  } catch (err: any) {
    error.value = err.data?.detail || 'Invalid or expired verification token. Please request a new verification email.'
  } finally {
    loading.value = false
  }
}

async function resendVerification() {
  resending.value = true

  try {
    // TODO: Call API to resend verification email
    // await $fetch('/auth/resend-verification', {
    //   method: 'POST',
    //   baseURL: useRuntimeConfig().public.apiBase,
    // })

    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 1500))

    const { success } = useNotifications()
    success('Verification email sent', 'Please check your inbox')
  } catch (err: any) {
    const { error: showError } = useNotifications()
    showError('Failed to send email', 'Please try again later')
  } finally {
    resending.value = false
  }
}

// Set page title
useHead({
  title: 'Verify Email',
})
</script>
