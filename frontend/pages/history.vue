<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="container-custom max-w-6xl">
      <!-- Header -->
      <div class="mb-8">
        <div class="flex items-start justify-between">
          <div>
            <h1 class="text-3xl font-bold text-gray-900">
              Analysis History
            </h1>
            <p class="mt-2 text-gray-600">
              View and manage your past contract analyses
            </p>
          </div>

          <NuxtLink
            to="/upload"
            class="btn btn--primary"
          >
            Upload New Contract
          </NuxtLink>
        </div>
      </div>

      <!-- Loading State -->
      <div
        v-if="contractsStore.loading && !contractsStore.hasContracts"
        class="flex items-center justify-center py-20"
      >
        <div class="text-center">
          <div class="spinner mx-auto h-12 w-12" aria-hidden="true" />
          <p class="mt-4 text-gray-600">Loading contracts...</p>
        </div>
      </div>

      <!-- Error State -->
      <div
        v-else-if="contractsStore.error && !contractsStore.hasContracts"
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
        <span>{{ contractsStore.error }}</span>
      </div>

      <!-- Empty State -->
      <div
        v-else-if="!contractsStore.hasContracts"
        class="bg-white rounded-lg border border-gray-200 p-12 text-center"
      >
        <svg
          class="mx-auto h-12 w-12 text-gray-400 mb-4"
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
            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
          />
        </svg>
        <h2 class="text-xl font-semibold text-gray-900 mb-2">
          No contracts yet
        </h2>
        <p class="text-gray-600 mb-6">
          Upload your first contract to get started with AI-powered analysis
        </p>
        <NuxtLink
          to="/upload"
          class="btn btn--primary inline-flex"
        >
          Upload Contract
        </NuxtLink>
      </div>

      <!-- Contracts List -->
      <div v-else class="space-y-4">
        <div
          v-for="contract in contractsStore.contracts"
          :key="contract.id"
          class="card hover:shadow-lg transition-shadow"
        >
          <div class="flex items-start justify-between gap-4">
            <!-- Contract Info -->
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-3 mb-2">
                <!-- File Icon -->
                <div
                  class="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-lg bg-primary-100"
                  aria-hidden="true"
                >
                  <svg
                    class="h-6 w-6 text-primary-600"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                    />
                  </svg>
                </div>

                <!-- Filename and metadata -->
                <div class="flex-1 min-w-0">
                  <h3 class="text-lg font-semibold text-gray-900 truncate">
                    {{ contract.filename }}
                  </h3>
                  <div class="flex flex-wrap items-center gap-x-3 gap-y-1 text-sm text-gray-500">
                    <span>{{ formatFileSize(contract.file_size) }}</span>
                    <span aria-hidden="true">•</span>
                    <span>{{ formatDate(contract.uploaded_at) }}</span>
                    <span v-if="contract.detected_language" aria-hidden="true">•</span>
                    <span v-if="contract.detected_language">{{ formatLanguage(contract.detected_language) }}</span>
                  </div>
                </div>
              </div>

              <!-- Page Count -->
              <div v-if="contract.page_count" class="mt-2">
                <span class="text-sm text-gray-600">
                  {{ contract.page_count }} {{ contract.page_count === 1 ? 'page' : 'pages' }}
                </span>
              </div>
            </div>

            <!-- Actions -->
            <div class="flex flex-col gap-2">
              <!-- View existing analysis if available -->
              <button
                v-if="contract.latest_analysis_id"
                type="button"
                class="btn btn--primary btn-sm"
                @click="viewExistingAnalysis(contract.latest_analysis_id)"
              >
                <svg
                  class="h-4 w-4 -ml-1 mr-1"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                  <path
                    fill-rule="evenodd"
                    d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z"
                    clip-rule="evenodd"
                  />
                </svg>
                View Results
              </button>

              <!-- Analyze again if no analysis exists -->
              <button
                v-else
                type="button"
                class="btn btn--primary btn-sm"
                @click="analyzeContract(contract.id)"
              >
                <svg
                  class="h-4 w-4 -ml-1 mr-1"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fill-rule="evenodd"
                    d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z"
                    clip-rule="evenodd"
                  />
                </svg>
                Analyze Contract
              </button>

              <button
                type="button"
                class="btn btn--secondary btn-sm"
                :aria-label="`Delete ${contract.filename}`"
                @click="confirmDelete(contract.id, contract.filename)"
              >
                Delete
              </button>
            </div>
          </div>
        </div>

        <!-- Pagination -->
        <div
          v-if="contractsStore.totalPages > 1"
          class="flex items-center justify-between border-t border-gray-200 bg-white px-4 py-3 sm:px-6 rounded-lg"
        >
          <div class="flex flex-1 justify-between sm:hidden">
            <button
              type="button"
              class="btn btn--secondary"
              :disabled="contractsStore.currentPage === 1"
              @click="loadPage(contractsStore.currentPage - 1)"
            >
              Previous
            </button>
            <button
              type="button"
              class="btn btn--secondary"
              :disabled="contractsStore.currentPage === contractsStore.totalPages"
              @click="loadPage(contractsStore.currentPage + 1)"
            >
              Next
            </button>
          </div>

          <div class="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between">
            <div>
              <p class="text-sm text-gray-700">
                Showing
                <span class="font-medium">
                  {{ (contractsStore.currentPage - 1) * contractsStore.perPage + 1 }}
                </span>
                to
                <span class="font-medium">
                  {{
                    Math.min(
                      contractsStore.currentPage * contractsStore.perPage,
                      contractsStore.total
                    )
                  }}
                </span>
                of
                <span class="font-medium">{{ contractsStore.total }}</span>
                results
              </p>
            </div>

            <nav
              class="isolate inline-flex -space-x-px rounded-md shadow-sm"
              aria-label="Pagination"
            >
              <button
                type="button"
                class="relative inline-flex items-center rounded-l-md px-2 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0 disabled:opacity-50 disabled:cursor-not-allowed"
                :disabled="contractsStore.currentPage === 1"
                aria-label="Previous page"
                @click="loadPage(contractsStore.currentPage - 1)"
              >
                <svg
                  class="h-5 w-5"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                  aria-hidden="true"
                >
                  <path
                    fill-rule="evenodd"
                    d="M12.79 5.23a.75.75 0 01-.02 1.06L8.832 10l3.938 3.71a.75.75 0 11-1.04 1.08l-4.5-4.25a.75.75 0 010-1.08l4.5-4.25a.75.75 0 011.06.02z"
                    clip-rule="evenodd"
                  />
                </svg>
              </button>

              <!-- Page numbers -->
              <button
                v-for="page in visiblePages"
                :key="page"
                type="button"
                class="relative inline-flex items-center px-4 py-2 text-sm font-semibold ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0"
                :class="{
                  'bg-primary-600 text-white ring-primary-600 hover:bg-primary-700':
                    page === contractsStore.currentPage,
                  'text-gray-900': page !== contractsStore.currentPage,
                }"
                :aria-label="`Page ${page}`"
                :aria-current="page === contractsStore.currentPage ? 'page' : undefined"
                @click="loadPage(page)"
              >
                {{ page }}
              </button>

              <button
                type="button"
                class="relative inline-flex items-center rounded-r-md px-2 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0 disabled:opacity-50 disabled:cursor-not-allowed"
                :disabled="contractsStore.currentPage === contractsStore.totalPages"
                aria-label="Next page"
                @click="loadPage(contractsStore.currentPage + 1)"
              >
                <svg
                  class="h-5 w-5"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                  aria-hidden="true"
                >
                  <path
                    fill-rule="evenodd"
                    d="M7.21 14.77a.75.75 0 01.02-1.06L11.168 10 7.23 6.29a.75.75 0 111.04-1.08l4.5 4.25a.75.75 0 010 1.08l-4.5 4.25a.75.75 0 01-1.06-.02z"
                    clip-rule="evenodd"
                  />
                </svg>
              </button>
            </nav>
          </div>
        </div>
      </div>

      <!-- Delete Confirmation Modal (Simple version) -->
      <Teleport to="body">
        <div
          v-if="deleteConfirmation.show"
          class="fixed inset-0 z-50 overflow-y-auto"
          aria-labelledby="modal-title"
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
                    id="modal-title"
                    class="text-base font-semibold leading-6 text-gray-900"
                  >
                    Delete contract
                  </h3>
                  <div class="mt-2">
                    <p class="text-sm text-gray-500">
                      Are you sure you want to delete "{{ deleteConfirmation.filename }}"? This
                      action cannot be undone.
                    </p>
                  </div>
                </div>
              </div>

              <div class="mt-5 sm:mt-4 sm:flex sm:flex-row-reverse gap-3">
                <button
                  type="button"
                  class="btn btn--danger w-full sm:w-auto"
                  :disabled="contractsStore.loading"
                  @click="handleDelete"
                >
                  Delete
                </button>
                <button
                  type="button"
                  class="btn btn--secondary w-full sm:w-auto mt-3 sm:mt-0"
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
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useContractsStore } from '~/stores/contracts'

/**
 * History Page
 * Displays user's contract analysis history with pagination
 */

definePageMeta({
  middleware: 'auth', // TODO: Create auth middleware
})

const router = useRouter()
const contractsStore = useContractsStore()

// State
const deleteConfirmation = ref({
  show: false,
  contractId: '',
  filename: '',
})

// Computed
const visiblePages = computed(() => {
  const pages: number[] = []
  const total = contractsStore.totalPages
  const current = contractsStore.currentPage

  // Always show first page
  pages.push(1)

  // Show pages around current page
  for (let i = Math.max(2, current - 1); i <= Math.min(total - 1, current + 1); i++) {
    if (!pages.includes(i)) {
      pages.push(i)
    }
  }

  // Always show last page
  if (total > 1 && !pages.includes(total)) {
    pages.push(total)
  }

  return pages.sort((a, b) => a - b)
})

// Lifecycle
onMounted(async () => {
  try {
    await contractsStore.fetchContracts(1)
  } catch (error) {
    console.error('Failed to load contracts:', error)
  }
})

// Methods
async function loadPage(page: number): Promise<void> {
  try {
    await contractsStore.fetchContracts(page)
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' })
  } catch (error) {
    console.error('Failed to load page:', error)
  }
}

function viewExistingAnalysis(analysisId: string): void {
  // Navigate to existing analysis results (no re-analysis needed)
  router.push(`/analysis/${analysisId}`)
}

async function analyzeContract(contractId: string): Promise<void> {
  // Create new analysis for this contract
  try {
    const { success } = useNotifications()

    // TODO: Call API to create new analysis
    // For now, navigate to analysis page (it will handle creation)
    router.push(`/analysis/${contractId}`)

    success('Analysis started', 'Your contract is being analyzed...')
  } catch (error) {
    console.error('Failed to start analysis:', error)
    const { error: showError } = useNotifications()
    showError('Analysis failed', 'Please try again later.')
  }
}

function confirmDelete(contractId: string, filename: string): void {
  deleteConfirmation.value = {
    show: true,
    contractId,
    filename,
  }
}

async function handleDelete(): Promise<void> {
  try {
    await contractsStore.deleteContract(deleteConfirmation.value.contractId)
    cancelDelete()
  } catch (error) {
    console.error('Failed to delete contract:', error)
  }
}

function cancelDelete(): void {
  deleteConfirmation.value = {
    show: false,
    contractId: '',
    filename: '',
  }
}

function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Bytes'

  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))

  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i]
}

function formatDate(dateString: string): string {
  const date = new Date(dateString)
  const now = new Date()
  const diffMs = now.getTime() - date.getTime()
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24))

  if (diffDays === 0) return 'Today'
  if (diffDays === 1) return 'Yesterday'
  if (diffDays < 7) return `${diffDays} days ago`

  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  })
}

function formatLanguage(lang: string): string {
  const languages: Record<string, string> = {
    english: 'English',
    russian: 'Russian',
    serbian: 'Serbian',
    french: 'French',
  }
  return languages[lang] || lang
}

// Set page title
useHead({
  title: 'History',
})
</script>

<style lang="scss" scoped>
.btn-sm {
  @apply px-3 py-2 text-sm;
}
</style>
