<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 px-4 py-12 sm:px-6 lg:px-8">
    <div class="w-full max-w-md">
      <!-- Header -->
      <div class="text-center">
        <h1 class="text-3xl font-bold text-gray-900">
          Welcome Back
        </h1>
        <p class="mt-2 text-sm text-gray-600">
          Sign in to your account to continue
        </p>
      </div>

      <!-- Login Form -->
      <form
        class="mt-8 space-y-6"
        @submit.prevent="handleSubmit"
      >
        <!-- Error Alert -->
        <div
          v-if="authStore.error"
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
          <span>{{ authStore.error }}</span>
          <button
            type="button"
            class="ml-auto"
            aria-label="Dismiss error"
            @click="authStore.clearError"
          >
            <svg
              class="h-5 w-5"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 20 20"
              fill="currentColor"
              aria-hidden="true"
            >
              <path
                d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z"
              />
            </svg>
          </button>
        </div>

        <div class="space-y-4">
          <!-- Email field -->
          <div class="form-group">
            <label
              for="email"
              class="block text-sm font-medium text-gray-700"
            >
              Email address
            </label>
            <input
              id="email"
              v-model="formData.email"
              type="email"
              name="email"
              autocomplete="email"
              required
              class="input"
              :class="{ 'input--error': emailError }"
              placeholder="you@example.com"
              :aria-invalid="!!emailError"
              :aria-describedby="emailError ? 'email-error' : undefined"
              @blur="validateEmail"
            >
            <p
              v-if="emailError"
              id="email-error"
              class="mt-1 text-sm text-red-600"
              role="alert"
            >
              {{ emailError }}
            </p>
          </div>

          <!-- Password field -->
          <div class="form-group">
            <label
              for="password"
              class="block text-sm font-medium text-gray-700"
            >
              Password
            </label>
            <div class="relative">
              <input
                id="password"
                v-model="formData.password"
                :type="showPassword ? 'text' : 'password'"
                name="password"
                autocomplete="current-password"
                required
                class="input pr-10"
                :class="{ 'input--error': passwordError }"
                placeholder="Enter your password"
                :aria-invalid="!!passwordError"
                :aria-describedby="passwordError ? 'password-error' : undefined"
                @blur="validatePassword"
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
            <p
              v-if="passwordError"
              id="password-error"
              class="mt-1 text-sm text-red-600"
              role="alert"
            >
              {{ passwordError }}
            </p>
          </div>
        </div>

        <!-- Forgot password link -->
        <div class="flex items-center justify-end">
          <NuxtLink
            to="/auth/forgot-password"
            class="text-sm font-medium text-primary-600 hover:text-primary-500 focus:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 rounded"
          >
            Forgot your password?
          </NuxtLink>
        </div>

        <!-- Submit button -->
        <div>
          <button
            type="submit"
            class="btn btn--primary w-full"
            :disabled="authStore.loading || !isFormValid"
            :aria-busy="authStore.loading"
          >
            <span v-if="!authStore.loading">Sign in</span>
            <span
              v-else
              class="flex items-center justify-center gap-2"
            >
              <span class="spinner" aria-hidden="true" />
              <span>Signing in...</span>
            </span>
          </button>
        </div>

        <!-- Register link -->
        <p class="text-center text-sm text-gray-600">
          Don't have an account?
          <NuxtLink
            to="/register"
            class="font-medium text-primary-600 hover:text-primary-500 focus:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 rounded"
          >
            Sign up for free
          </NuxtLink>
        </p>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '~/stores/auth'

/**
 * Login Page
 * WCAG 2.1 AA compliant with proper form validation and error handling
 */

definePageMeta({
  layout: false,
  middleware: 'guest', // TODO: Create guest middleware
})

const router = useRouter()
const authStore = useAuthStore()

// Form state
const formData = ref({
  email: '',
  password: '',
})

const showPassword = ref(false)
const emailError = ref('')
const passwordError = ref('')

// Computed
const isFormValid = computed(() => {
  return (
    formData.value.email.trim() !== '' &&
    formData.value.password.trim() !== '' &&
    !emailError.value &&
    !passwordError.value
  )
})

// Validation
function validateEmail() {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!formData.value.email.trim()) {
    emailError.value = 'Email is required'
  } else if (!emailRegex.test(formData.value.email)) {
    emailError.value = 'Please enter a valid email address'
  } else {
    emailError.value = ''
  }
}

function validatePassword() {
  if (!formData.value.password.trim()) {
    passwordError.value = 'Password is required'
  } else if (formData.value.password.length < 8) {
    passwordError.value = 'Password must be at least 8 characters'
  } else {
    passwordError.value = ''
  }
}

// Form submission
async function handleSubmit() {
  // Validate all fields
  validateEmail()
  validatePassword()

  if (!isFormValid.value) return

  try {
    await authStore.login({
      email: formData.value.email,
      password: formData.value.password,
    })

    // Redirect to upload page on success
    await router.push('/upload')
  } catch (error) {
    // Error is handled by the store
    console.error('Login error:', error)
  }
}

// Clear errors when user starts typing
watch(() => formData.value.email, () => {
  if (emailError.value) emailError.value = ''
  if (authStore.error) authStore.clearError()
})

watch(() => formData.value.password, () => {
  if (passwordError.value) passwordError.value = ''
  if (authStore.error) authStore.clearError()
})

// Set page title
useHead({
  title: 'Login',
})
</script>
