<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="container-custom max-w-5xl">
      <!-- Loading State -->
      <div
        v-if="analysesStore.loading && !analysesStore.currentAnalysis"
        class="flex items-center justify-center py-20"
      >
        <div class="text-center">
          <div class="spinner mx-auto h-12 w-12" aria-hidden="true" />
          <p class="mt-4 text-gray-600">Loading analysis...</p>
        </div>
      </div>

      <!-- Error State -->
      <div
        v-else-if="analysesStore.error && !analysesStore.currentAnalysis"
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
        <span>{{ analysesStore.error }}</span>
      </div>

      <!-- Analysis Content -->
      <template v-else-if="analysesStore.currentAnalysis">
        <!-- Header -->
        <div class="mb-6">
          <div class="flex items-start justify-between">
            <div>
              <h1 class="text-3xl font-bold text-gray-900">
                Contract Analysis
              </h1>
              <p class="mt-2 text-gray-600">
                Analysis ID: {{ analysisId }}
              </p>
            </div>

            <!-- Status Badge -->
            <span
              class="badge"
              :class="{
                'badge--info': analysesStore.currentAnalysis.status === 'queued',
                'badge--warning': analysesStore.currentAnalysis.status === 'running',
                'badge--success': analysesStore.currentAnalysis.status === 'succeeded',
                'badge--error': analysesStore.currentAnalysis.status === 'failed',
              }"
              role="status"
            >
              {{ analysesStore.currentAnalysis.status }}
            </span>
          </div>
        </div>

        <!-- Processing State -->
        <div
          v-if="analysesStore.isAnalyzing"
          class="bg-white rounded-lg border border-gray-200 p-8"
        >
          <div class="text-center">
            <div class="spinner mx-auto h-12 w-12 mb-4" aria-hidden="true" />
            <h2 class="text-xl font-semibold text-gray-900 mb-2">
              Analyzing your contract...
            </h2>
            <p class="text-gray-600 mb-6">
              This may take a few moments. Please don't close this page.
            </p>

            <!-- Progress Events -->
            <div
              v-if="analysesStore.events.length > 0"
              class="mt-6 space-y-2"
            >
              <h3 class="text-sm font-medium text-gray-700 mb-3">
                Progress:
              </h3>
              <div class="space-y-2 max-h-48 overflow-y-auto scrollbar-custom">
                <div
                  v-for="(event, index) in analysesStore.events"
                  :key="index"
                  class="flex items-start gap-2 text-sm text-left"
                >
                  <svg
                    class="h-5 w-5 text-green-500 flex-shrink-0 mt-0.5"
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
                  <span class="text-gray-700">{{ formatEventMessage(event) }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Analysis Results -->
        <div v-else-if="analysesStore.hasResults" class="space-y-6">
          <!-- Confidence Score -->
          <div
            v-if="analysesStore.currentAnalysis.confidence_score !== null"
            class="bg-white rounded-lg border border-gray-200 p-6"
          >
            <h2 class="text-lg font-semibold text-gray-900 mb-3">
              Confidence Score
            </h2>
            <div class="flex items-center gap-4">
              <div class="flex-1 bg-gray-200 rounded-full h-3">
                <div
                  class="h-3 rounded-full transition-all"
                  :class="{
                    'bg-green-500': analysesStore.currentAnalysis.confidence_score >= 0.8,
                    'bg-yellow-500': analysesStore.currentAnalysis.confidence_score >= 0.6 && analysesStore.currentAnalysis.confidence_score < 0.8,
                    'bg-red-500': analysesStore.currentAnalysis.confidence_score < 0.6,
                  }"
                  :style="{ width: `${analysesStore.currentAnalysis.confidence_score * 100}%` }"
                  role="progressbar"
                  :aria-valuenow="analysesStore.currentAnalysis.confidence_score * 100"
                  aria-valuemin="0"
                  aria-valuemax="100"
                />
              </div>
              <span class="text-lg font-semibold text-gray-900">
                {{ Math.round(analysesStore.currentAnalysis.confidence_score * 100) }}%
              </span>
            </div>
          </div>

          <!-- Analysis Sections -->
          <AnalysisSection
            v-for="(section, key) in formattedOutput"
            :key="key"
            :title="formatSectionTitle(key)"
            :content="section"
            :section-key="key"
            @feedback="handleFeedback"
          />

          <!-- Actions -->
          <div class="flex flex-wrap gap-3">
            <NuxtLink
              to="/upload"
              class="btn btn--primary"
            >
              Analyze Another Contract
            </NuxtLink>
            <NuxtLink
              to="/history"
              class="btn btn--secondary"
            >
              View History
            </NuxtLink>
          </div>
        </div>

        <!-- Failed State -->
        <div
          v-else-if="analysesStore.currentAnalysis.status === 'failed'"
          class="bg-white rounded-lg border border-red-200 p-8"
        >
          <div class="text-center">
            <svg
              class="mx-auto h-12 w-12 text-red-500 mb-4"
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
                d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            <h2 class="text-xl font-semibold text-gray-900 mb-2">
              Analysis Failed
            </h2>
            <p class="text-gray-600 mb-6">
              We encountered an error while analyzing your contract. Please try again.
            </p>
            <NuxtLink
              to="/upload"
              class="btn btn--primary"
            >
              Upload New Contract
            </NuxtLink>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAnalysesStore } from '~/stores/analyses'
import type { AnalysisEvent } from '~/stores/analyses'

/**
 * Analysis Results Page
 * Displays analysis results with SSE real-time updates
 */

definePageMeta({
  middleware: 'auth', // TODO: Create auth middleware
})

const route = useRoute()
const analysesStore = useAnalysesStore()

const analysisId = computed(() => route.params.id as string)

const formattedOutput = computed(() => {
  return analysesStore.currentAnalysis?.formatted_output || {}
})

// Lifecycle
onMounted(async () => {
  try {
    // Fetch initial analysis
    await analysesStore.fetchAnalysis(analysisId.value)

    // Connect to SSE for real-time updates if still processing
    if (analysesStore.isAnalyzing) {
      analysesStore.connectSSE(analysisId.value)
    }
  } catch (error) {
    console.error('Failed to load analysis:', error)
  }
})

onUnmounted(() => {
  // Clean up SSE connection
  analysesStore.disconnectSSE()
})

// Methods
function formatEventMessage(event: AnalysisEvent): string {
  switch (event.kind) {
    case 'parsing':
      return 'Extracting text from document...'
    case 'language_detection':
      return `Detected language: ${event.payload.language || 'Unknown'}`
    case 'preprocessing':
      return 'Preparing contract for analysis...'
    case 'analysis':
      return 'Analyzing contract clauses...'
    case 'formatting':
      return 'Formatting results...'
    case 'completed':
      return 'Analysis completed!'
    case 'failed':
      return 'Analysis failed'
    default:
      return event.kind
  }
}

function formatSectionTitle(key: string): string {
  // Convert snake_case to Title Case
  return key
    .split('_')
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

async function handleFeedback(data: {
  sectionKey: string
  isCorrect: boolean
  comment?: string
}): Promise<void> {
  try {
    await analysesStore.submitFeedback(
      analysisId.value,
      data.sectionKey,
      data.isCorrect,
      data.comment
    )
  } catch (error) {
    console.error('Failed to submit feedback:', error)
  }
}

// Set page title
useHead({
  title: 'Analysis Results',
})
</script>
