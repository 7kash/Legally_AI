<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="container-custom max-w-4xl">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">
          Account Settings
        </h1>
        <p class="mt-2 text-gray-600">
          Manage your account and subscription
        </p>
      </div>

      <!-- Loading State -->
      <div
        v-if="authStore.loading"
        class="flex items-center justify-center py-20"
      >
        <div class="text-center">
          <div class="spinner mx-auto h-12 w-12" aria-hidden="true" />
          <p class="mt-4 text-gray-600">Loading account...</p>
        </div>
      </div>

      <!-- Account Content -->
      <div v-else-if="authStore.user" class="space-y-6">
        <!-- User Info Card -->
        <section class="card">
          <h2 class="text-lg font-semibold text-gray-900 mb-4">
            Account Information
          </h2>

          <div class="space-y-4">
            <div>
              <div class="block text-sm font-medium text-gray-700 mb-1">
                Email Address
              </div>
              <p class="text-gray-900">
                {{ authStore.user.email }}
              </p>
            </div>

            <div>
              <div class="block text-sm font-medium text-gray-700 mb-1">
                Member Since
              </div>
              <p class="text-gray-900">
                {{ formatDate(authStore.user.created_at) }}
              </p>
            </div>

            <div>
              <div class="block text-sm font-medium text-gray-700 mb-1">
                User ID
              </div>
              <p class="text-gray-500 text-sm font-mono">
                {{ authStore.user.id }}
              </p>
            </div>
          </div>
        </section>

        <!-- Subscription Card -->
        <section class="card">
          <div class="flex items-start justify-between mb-4">
            <div>
              <h2 class="text-lg font-semibold text-gray-900">
                Subscription
              </h2>
              <p class="text-sm text-gray-600 mt-1">
                Current plan: <span class="font-semibold">{{ authStore.user.tier === 'free' ? 'Free' : 'Premium' }}</span>
              </p>
            </div>

            <span
              class="badge"
              :class="{
                'badge--info': authStore.user.tier === 'free',
                'badge--success': authStore.user.tier === 'premium',
              }"
            >
              {{ authStore.user.tier }}
            </span>
          </div>

          <!-- Free Tier Info -->
          <div v-if="authStore.user.tier === 'free'" class="space-y-4">
            <div class="rounded-lg bg-blue-50 border border-blue-200 p-4">
              <div class="flex items-start gap-3">
                <svg
                  class="h-5 w-5 text-blue-600 flex-shrink-0 mt-0.5"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                  aria-hidden="true"
                >
                  <path
                    fill-rule="evenodd"
                    d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a.75.75 0 000 1.5h.253a.25.25 0 01.244.304l-.459 2.066A1.75 1.75 0 0010.747 15H11a.75.75 0 000-1.5h-.253a.25.25 0 01-.244-.304l.459-2.066A1.75 1.75 0 009.253 9H9z"
                    clip-rule="evenodd"
                  />
                </svg>
                <div>
                  <p class="text-sm font-medium text-blue-900">
                    Free Tier - {{ authStore.user.analyses_remaining }} of 3 analyses remaining
                  </p>
                  <p class="mt-1 text-sm text-blue-700">
                    Upgrade to Premium for unlimited analyses and priority support
                  </p>
                </div>
              </div>
            </div>

            <!-- Usage Progress -->
            <div>
              <div class="flex items-center justify-between mb-2">
                <span class="text-sm font-medium text-gray-700">Usage</span>
                <span class="text-sm text-gray-600">
                  {{ authStore.user.contracts_analyzed }} / 3 analyses used
                </span>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-2">
                <div
                  class="h-2 rounded-full transition-all"
                  :class="{
                    'bg-green-500': authStore.user.contracts_analyzed < 2,
                    'bg-yellow-500': authStore.user.contracts_analyzed === 2,
                    'bg-red-500': authStore.user.contracts_analyzed >= 3,
                  }"
                  :style="{
                    width: `${(authStore.user.contracts_analyzed / 3) * 100}%`,
                  }"
                  role="progressbar"
                  :aria-valuenow="authStore.user.contracts_analyzed"
                  aria-valuemin="0"
                  aria-valuemax="3"
                />
              </div>
            </div>

            <!-- Upgrade CTA -->
            <button
              type="button"
              class="btn btn--primary w-full"
              @click="showUpgradeInfo = !showUpgradeInfo"
            >
              Upgrade to Premium
            </button>
          </div>

          <!-- Premium Tier Info -->
          <div v-else class="space-y-4">
            <div class="rounded-lg bg-green-50 border border-green-200 p-4">
              <div class="flex items-start gap-3">
                <svg
                  class="h-5 w-5 text-green-600 flex-shrink-0 mt-0.5"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                  aria-hidden="true"
                >
                  <path
                    fill-rule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z"
                    clip-rule="evenodd"
                  />
                </svg>
                <div>
                  <p class="text-sm font-medium text-green-900">
                    Premium Plan Active
                  </p>
                  <p class="mt-1 text-sm text-green-700">
                    You have unlimited contract analyses and priority support
                  </p>
                </div>
              </div>
            </div>

            <div>
              <p class="text-sm text-gray-600">
                Total analyses: <span class="font-semibold text-gray-900">{{ authStore.user.contracts_analyzed }}</span>
              </p>
            </div>
          </div>
        </section>

        <!-- Premium Benefits (shown when user clicks upgrade) -->
        <section
          v-if="showUpgradeInfo && authStore.user.tier === 'free'"
          class="card border-primary-200 bg-primary-50"
        >
          <h2 class="text-lg font-semibold text-gray-900 mb-4">
            Premium Benefits
          </h2>

          <ul class="space-y-3 mb-6">
            <li class="flex items-start gap-3">
              <svg
                class="h-5 w-5 text-primary-600 flex-shrink-0 mt-0.5"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fill-rule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z"
                  clip-rule="evenodd"
                />
              </svg>
              <span class="text-gray-700">Unlimited contract analyses</span>
            </li>
            <li class="flex items-start gap-3">
              <svg
                class="h-5 w-5 text-primary-600 flex-shrink-0 mt-0.5"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fill-rule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z"
                  clip-rule="evenodd"
                />
              </svg>
              <span class="text-gray-700">Priority processing for faster results</span>
            </li>
            <li class="flex items-start gap-3">
              <svg
                class="h-5 w-5 text-primary-600 flex-shrink-0 mt-0.5"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fill-rule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z"
                  clip-rule="evenodd"
                />
              </svg>
              <span class="text-gray-700">Advanced analysis features</span>
            </li>
            <li class="flex items-start gap-3">
              <svg
                class="h-5 w-5 text-primary-600 flex-shrink-0 mt-0.5"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fill-rule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z"
                  clip-rule="evenodd"
                />
              </svg>
              <span class="text-gray-700">Email and priority support</span>
            </li>
            <li class="flex items-start gap-3">
              <svg
                class="h-5 w-5 text-primary-600 flex-shrink-0 mt-0.5"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fill-rule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z"
                  clip-rule="evenodd"
                />
              </svg>
              <span class="text-gray-700">Export analysis results to PDF</span>
            </li>
          </ul>

          <div class="rounded-lg bg-white border border-gray-200 p-4">
            <div class="text-center">
              <p class="text-3xl font-bold text-gray-900">
                $29<span class="text-lg font-normal text-gray-600">/month</span>
              </p>
              <p class="mt-1 text-sm text-gray-600">
                or $290/year (save 17%)
              </p>
              <button
                type="button"
                class="btn btn--primary w-full mt-4"
                disabled
              >
                Coming Soon
              </button>
              <p class="mt-2 text-xs text-gray-500">
                Payment processing will be available soon
              </p>
            </div>
          </div>
        </section>

        <!-- GDPR Data Management -->
        <section class="card border-blue-200">
          <h2 class="text-lg font-semibold text-gray-900 mb-4">
            Your Data
          </h2>

          <div class="space-y-4">
            <div>
              <h3 class="text-sm font-medium text-gray-900 mb-1">
                Export Your Data
              </h3>
              <p class="text-sm text-gray-600 mb-3">
                Download all your account data including contracts, analyses, and settings in JSON format
              </p>
              <button
                type="button"
                class="btn btn--secondary"
                :disabled="exportLoading"
                @click="handleExportData"
              >
                <span v-if="!exportLoading">Download My Data</span>
                <span v-else class="flex items-center gap-2">
                  <span class="spinner h-4 w-4" aria-hidden="true" />
                  <span>Preparing...</span>
                </span>
              </button>
            </div>
          </div>
        </section>

        <!-- Danger Zone -->
        <section class="card border-red-200">
          <h2 class="text-lg font-semibold text-red-900 mb-4">
            Danger Zone
          </h2>

          <div class="space-y-4">
            <div>
              <h3 class="text-sm font-medium text-gray-900 mb-1">
                Logout
              </h3>
              <p class="text-sm text-gray-600 mb-3">
                Sign out of your account on this device
              </p>
              <button
                type="button"
                class="btn btn--secondary"
                @click="handleLogout"
              >
                Logout
              </button>
            </div>

            <div class="pt-4 border-t border-gray-200">
              <h3 class="text-sm font-medium text-red-900 mb-1">
                Delete Account
              </h3>
              <p class="text-sm text-gray-600 mb-3">
                Permanently delete your account and all associated data. This action cannot be undone.
              </p>
              <button
                type="button"
                class="btn btn--danger"
                @click="showDeleteConfirmation = true"
              >
                Delete Account
              </button>
            </div>
          </div>
        </section>
      </div>
    </div>

    <!-- Delete Account Confirmation Modal -->
    <Teleport to="body">
      <div
        v-if="showDeleteConfirmation"
        class="fixed inset-0 z-50 overflow-y-auto"
        aria-labelledby="delete-modal-title"
        role="dialog"
        aria-modal="true"
      >
        <!-- Backdrop -->
        <div
          class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
          @click="cancelDelete"
        />

        <!-- Modal -->
        <div class="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
          <div
            class="relative transform overflow-hidden rounded-lg bg-white px-4 pb-4 pt-5 text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg sm:p-6"
          >
            <div class="sm:flex sm:items-start">
              <div
                class="mx-auto flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-full bg-red-100 sm:mx-0 sm:h-10 sm:w-10"
                aria-hidden="true"
              >
                <svg
                  class="h-6 w-6 text-red-600"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke-width="1.5"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z"
                  />
                </svg>
              </div>

              <div class="mt-3 text-center sm:ml-4 sm:mt-0 sm:text-left">
                <h3
                  id="delete-modal-title"
                  class="text-base font-semibold leading-6 text-gray-900"
                >
                  Delete account permanently?
                </h3>
                <div class="mt-2">
                  <p class="text-sm text-gray-500 mb-3">
                    This will permanently delete your account and all associated data including:
                  </p>
                  <ul class="text-sm text-gray-500 list-disc list-inside space-y-1 mb-3">
                    <li>All uploaded contracts</li>
                    <li>All analysis results</li>
                    <li>Your account settings</li>
                    <li>Usage history</li>
                  </ul>
                  <p class="text-sm font-semibold text-red-600">
                    This action cannot be undone.
                  </p>
                  <div class="mt-4">
                    <label for="confirm-delete" class="block text-sm font-medium text-gray-700 mb-2">
                      Type <span class="font-mono font-semibold">DELETE</span> to confirm:
                    </label>
                    <input
                      id="confirm-delete"
                      v-model="deleteConfirmText"
                      type="text"
                      class="input w-full"
                      placeholder="DELETE"
                      @keyup.enter="deleteConfirmText === 'DELETE' && handleDeleteAccount()"
                    />
                  </div>
                </div>
              </div>
            </div>

            <div class="mt-5 sm:mt-4 sm:flex sm:flex-row-reverse gap-3">
              <button
                type="button"
                class="btn btn--danger w-full sm:w-auto"
                :disabled="deleteConfirmText !== 'DELETE' || deleteLoading"
                @click="handleDeleteAccount"
              >
                <span v-if="!deleteLoading">Delete My Account</span>
                <span v-else class="flex items-center gap-2">
                  <span class="spinner h-4 w-4" aria-hidden="true" />
                  <span>Deleting...</span>
                </span>
              </button>
              <button
                type="button"
                class="btn btn--secondary w-full sm:w-auto mt-3 sm:mt-0"
                :disabled="deleteLoading"
                @click="cancelDelete"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '~/stores/auth'
import { useNotifications } from '~/composables/useNotifications'

/**
 * Account Page
 * User account settings and subscription management
 */

definePageMeta({
  middleware: 'auth', // TODO: Create auth middleware
})

const router = useRouter()
const authStore = useAuthStore()
const { success: showSuccess, error: showError } = useNotifications()

// State
const showUpgradeInfo = ref(false)
const exportLoading = ref(false)
const showDeleteConfirmation = ref(false)
const deleteConfirmText = ref('')
const deleteLoading = ref(false)

// Methods
async function handleLogout(): Promise<void> {
  try {
    await authStore.logout()
    await router.push('/login')
  } catch (error) {
    console.error('Logout error:', error)
  }
}

function formatDate(dateString: string): string {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    month: 'long',
    day: 'numeric',
    year: 'numeric',
  })
}

async function handleExportData(): Promise<void> {
  exportLoading.value = true
  try {
    const { token } = authStore
    if (!token) throw new Error('Not authenticated')

    const response = await $fetch('/account/export', {
      method: 'GET',
      baseURL: useRuntimeConfig().public.apiBase,
      headers: {
        Authorization: `Bearer ${token}`,
      },
      responseType: 'blob',
    })

    // Create download link
    const blob = new Blob([response as any], { type: 'application/json' })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `legally-ai-data-${new Date().toISOString().split('T')[0]}.json`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)

    showSuccess('Data exported successfully')
  } catch (error) {
    console.error('Export error:', error)
    showError('Failed to export data', 'Please try again.')
  } finally {
    exportLoading.value = false
  }
}

async function handleDeleteAccount(): Promise<void> {
  if (deleteConfirmText.value !== 'DELETE') return

  deleteLoading.value = true
  try {
    const { token } = authStore
    if (!token) throw new Error('Not authenticated')

    await $fetch('/account', {
      method: 'DELETE',
      baseURL: useRuntimeConfig().public.apiBase,
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    // Clear auth and redirect
    await authStore.logout()
    showSuccess('Account deleted successfully')
    await router.push('/')
  } catch (error) {
    console.error('Delete error:', error)
    showError('Failed to delete account', 'Please try again.')
    deleteLoading.value = false
  }
}

function cancelDelete(): void {
  showDeleteConfirmation.value = false
  deleteConfirmText.value = ''
  deleteLoading.value = false
}

// Set page title
useHead({
  title: 'Account',
})
</script>
