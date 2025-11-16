<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="container-custom max-w-4xl">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">
          Upload Contract
        </h1>
        <p class="mt-2 text-gray-600">
          Upload your contract in PDF or DOCX format for AI-powered analysis.
        </p>

        <!-- Analysis limit info for free users -->
        <div
          v-if="authStore.isFreeUser && authStore.user"
          class="mt-4 rounded-lg bg-blue-50 border border-blue-200 p-4"
          role="status"
        >
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
            <div class="flex-1">
              <p class="text-sm font-medium text-blue-900">
                Free Tier: {{ authStore.user.analyses_remaining }} of 3 analyses remaining
              </p>
              <p class="mt-1 text-sm text-blue-700">
                Upgrade to Premium for unlimited analyses.
                <NuxtLink
                  to="/account"
                  class="font-semibold underline hover:text-blue-900"
                >
                  Learn more
                </NuxtLink>
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Upload Form -->
      <div class="bg-white rounded-lg border border-gray-200 p-6 sm:p-8">
        <form @submit.prevent="handleSubmit">
          <!-- Language Selection -->
          <div class="mb-6 grid gap-6 md:grid-cols-2">
            <!-- Output Language -->
            <div>
              <label
                for="output-language"
                class="block text-sm font-medium text-gray-700 mb-2"
              >
                Output Language
              </label>
              <select
                id="output-language"
                v-model="outputLanguage"
                name="output-language"
                class="input w-full"
                required
              >
                <option value="english">
                  English
                </option>
                <option value="russian">
                  Russian (Русский)
                </option>
                <option value="serbian">
                  Serbian (Српски)
                </option>
                <option value="french">
                  French (Français)
                </option>
              </select>
              <p class="mt-1 text-sm text-gray-500">
                Language for the analysis output
              </p>
            </div>

            <!-- Contract Language Override (Optional) -->
            <div>
              <label
                for="contract-language"
                class="block text-sm font-medium text-gray-700 mb-2"
              >
                Contract Language <span class="text-gray-500 font-normal">(Optional)</span>
              </label>
              <select
                id="contract-language"
                v-model="contractLanguage"
                name="contract-language"
                class="input w-full"
              >
                <option value="">
                  Auto-detect
                </option>
                <option value="english">
                  English
                </option>
                <option value="russian">
                  Russian (Русский)
                </option>
                <option value="serbian">
                  Serbian (Српски)
                </option>
                <option value="french">
                  French (Français)
                </option>
              </select>
              <p class="mt-1 text-sm text-gray-500">
                Override automatic language detection
              </p>
            </div>
          </div>

          <!-- File Upload -->
          <div class="mb-6">
            <label for="file-input" class="block text-sm font-medium text-gray-700 mb-2">
              Contract Document
            </label>
            <FileUpload
              ref="fileUploadRef"
              :uploading="contractsStore.uploading"
              :upload-progress="contractsStore.uploadProgress"
              hide-upload-button
              @file-selected="handleFileSelected"
              @error="handleUploadError"
            />
          </div>

          <!-- Error Alert -->
          <div
            v-if="contractsStore.error"
            role="alert"
            class="alert alert--error mb-6"
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
            <button
              type="button"
              class="ml-auto"
              aria-label="Dismiss error"
              @click="contractsStore.clearError"
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

          <!-- Submit Button -->
          <div class="flex flex-col sm:flex-row gap-3">
            <button
              type="submit"
              class="btn btn--primary flex-1 sm:flex-initial"
              :disabled="!canSubmit"
              :aria-busy="contractsStore.uploading"
            >
              <span v-if="!contractsStore.uploading">
                Upload and Analyze
              </span>
              <span
                v-else
                class="flex items-center justify-center gap-2"
              >
                <span class="spinner" aria-hidden="true" />
                <span>Uploading... {{ contractsStore.uploadProgress }}%</span>
              </span>
            </button>

            <NuxtLink
              to="/history"
              class="btn btn--secondary flex-1 sm:flex-initial"
            >
              View History
            </NuxtLink>
          </div>
        </form>
      </div>

      <!-- How it works -->
      <div class="mt-8 bg-white rounded-lg border border-gray-200 p-6">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">
          How it works
        </h2>
        <ol class="space-y-3">
          <li class="flex gap-3">
            <span
              class="flex h-6 w-6 flex-shrink-0 items-center justify-center rounded-full bg-primary-100 text-sm font-semibold text-primary-600"
              aria-hidden="true"
            >
              1
            </span>
            <p class="text-gray-600">
              Upload your contract in PDF or DOCX format (max 10MB)
            </p>
          </li>
          <li class="flex gap-3">
            <span
              class="flex h-6 w-6 flex-shrink-0 items-center justify-center rounded-full bg-primary-100 text-sm font-semibold text-primary-600"
              aria-hidden="true"
            >
              2
            </span>
            <p class="text-gray-600">
              Our AI analyzes your document and detects the language automatically
            </p>
          </li>
          <li class="flex gap-3">
            <span
              class="flex h-6 w-6 flex-shrink-0 items-center justify-center rounded-full bg-primary-100 text-sm font-semibold text-primary-600"
              aria-hidden="true"
            >
              3
            </span>
            <p class="text-gray-600">
              Get comprehensive analysis including summary, key clauses, obligations, and risk
              assessment
            </p>
          </li>
          <li class="flex gap-3">
            <span
              class="flex h-6 w-6 flex-shrink-0 items-center justify-center rounded-full bg-primary-100 text-sm font-semibold text-primary-600"
              aria-hidden="true"
            >
              4
            </span>
            <p class="text-gray-600">
              Ask follow-up questions about your contract using the interactive Q&A feature
            </p>
          </li>
        </ol>
      </div>

      <!-- Supported formats info -->
      <div class="mt-6 text-center text-sm text-gray-500">
        <p>
          Supported formats: PDF, DOCX • Maximum file size: 10MB
        </p>
        <p class="mt-1">
          Supported languages: English, Russian, Serbian, French
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '~/stores/auth'
import { useContractsStore } from '~/stores/contracts'
import FileUpload from '~/components/upload/FileUpload.vue'

/**
 * Upload Page
 * Contract upload with language selection
 */

definePageMeta({
  middleware: 'auth', // TODO: Create auth middleware
})

const router = useRouter()
const authStore = useAuthStore()
const contractsStore = useContractsStore()

// State
const fileUploadRef = ref<any>(null)
const selectedFile = ref<File | null>(null)
const outputLanguage = ref('english')
const contractLanguage = ref('')  // Empty string means auto-detect

// Computed
const canSubmit = computed(() => {
  return (
    selectedFile.value !== null &&
    !contractsStore.uploading &&
    authStore.hasAnalysesRemaining
  )
})

// Methods
function handleFileSelected(file: File): void {
  selectedFile.value = file
  contractsStore.clearError()
}

function handleUploadError(error: string): void {
  selectedFile.value = null
}

async function handleSubmit(): Promise<void> {
  if (!selectedFile.value || !canSubmit.value) return

  try {
    // Upload contract
    const contractId = await contractsStore.uploadContract(selectedFile.value)

    // Create analysis immediately after upload
    const analysisId = await createAnalysis(contractId)

    // Navigate to analysis page
    await router.push(`/analysis/${analysisId}`)
  } catch (error) {
    console.error('Upload error:', error)
    // Error is handled by the store
  }
}

async function createAnalysis(contractId: string): Promise<string> {
  const { token } = authStore
  if (!token) {
    throw new Error('Not authenticated')
  }

  const response = await $fetch<{ id: string }>('/analyses', {
    method: 'POST',
    baseURL: useRuntimeConfig().public.apiBase,
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: {
      contract_id: contractId,
      output_language: outputLanguage.value,
      contract_language: contractLanguage.value || null,  // Send null if auto-detect
    },
  })

  return response.id
}

// Set page title
useHead({
  title: 'Upload Contract',
})
</script>
