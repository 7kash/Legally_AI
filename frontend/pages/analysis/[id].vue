<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 py-8">
    <div class="container-custom max-w-4xl">
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
        <div class="mb-8 text-center">
          <h1 class="text-4xl font-bold text-gray-900 mb-2">
            Contract Analysis
          </h1>
          <p class="text-gray-600">
            AI-powered insights for your contract
          </p>
        </div>

        <!-- Processing State -->
        <div
          v-if="analysesStore.isAnalyzing"
          class="bg-white rounded-xl shadow-lg border border-gray-200 p-8"
        >
          <div class="text-center">
            <div class="spinner mx-auto h-12 w-12 mb-4" />
            <h2 class="text-xl font-semibold text-gray-900 mb-2">
              Analyzing your contract...
            </h2>
            <p class="text-gray-600 mb-6">
              This may take a few moments. Please don't close this page.
            </p>

            <!-- Progress Events -->
            <div v-if="analysesStore.events.length > 0" class="mt-6 space-y-2">
              <h3 class="text-sm font-medium text-gray-700 mb-3">Progress:</h3>
              <div class="space-y-2 max-h-48 overflow-y-auto">
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
          <!-- ELI5 Mode Toggle -->
          <ELI5Toggle
            v-model="eli5Enabled"
            :loading="eli5Loading"
            @toggle="toggleELI5Mode"
          />

          <!-- Important Limits Disclaimer -->
          <ImportantLimits />

          <!-- Screening Badge -->
          <ScreeningBadge v-if="screeningResult" :variant="screeningResult" />

          <!-- Confidence Level -->
          <div
            v-if="analysesStore.currentAnalysis?.confidence_score != null"
            class="bg-white rounded-xl shadow-sm border border-gray-200 p-6"
          >
            <h2 class="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <svg class="h-5 w-5 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Confidence Level
            </h2>
            <div class="flex items-center gap-4 mb-3">
              <div class="flex-1 bg-gray-200 rounded-full h-3">
                <div
                  class="h-3 rounded-full transition-all"
                  :class="{
                    'bg-green-500': analysesStore.currentAnalysis.confidence_score >= 0.8,
                    'bg-yellow-500': analysesStore.currentAnalysis.confidence_score >= 0.6 && analysesStore.currentAnalysis.confidence_score < 0.8,
                    'bg-red-500': analysesStore.currentAnalysis.confidence_score < 0.6,
                  }"
                  :style="{ width: `${analysesStore.currentAnalysis.confidence_score * 100}%` }"
                />
              </div>
              <span class="text-lg font-bold text-gray-900">
                {{ Math.round(analysesStore.currentAnalysis.confidence_score * 100) }}%
              </span>
            </div>
            <p v-if="confidenceReason" class="text-sm text-gray-600">
              {{ confidenceReason }}
            </p>
          </div>

          <!-- About the Contract -->
          <div v-if="getAboutSummary()" class="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl shadow-sm border border-blue-200 p-6">
            <h2 class="text-lg font-semibold text-gray-900 mb-3 flex items-center gap-2">
              <svg class="h-5 w-5 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              About the Contract
            </h2>
            <p class="text-gray-800 leading-relaxed">{{ getAboutSummary() }}</p>
          </div>

          <!-- Dynamic Widget Rendering -->
          <component
            v-for="key in widgetOrder"
            :key="key"
            :is="getWidgetComponent(key)"
            v-if="formattedOutput[key] && hasContent(formattedOutput[key])"
            :title="getWidgetTitle(key)"
            :content="formattedOutput[key]"
            :eli5-enabled="eli5Enabled"
            :icon="getWidgetConfig(key)?.icon"
            :color="getWidgetConfig(key)?.color"
          />

          <!-- Actions -->
          <div class="flex flex-wrap gap-3 pt-4">
            <button
              type="button"
              class="btn btn--primary flex items-center gap-2"
              @click="handleExport"
            >
              <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
              Export Results
            </button>
            <NuxtLink to="/upload" class="btn btn--secondary">
              Analyze Another Contract
            </NuxtLink>
            <NuxtLink to="/history" class="btn btn--secondary">
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
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
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
            <NuxtLink to="/upload" class="btn btn--primary">
              Upload New Contract
            </NuxtLink>
          </div>
        </div>
      </template>

      <!-- Export Modal -->
      <ExportModal
        v-model="showExportModal"
        @export="handleExportFormat"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, computed, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useAnalysesStore } from '~/stores/analyses'
import { useAuthStore } from '~/stores/auth'
import type { AnalysisEvent } from '~/stores/analyses'
import { exportAnalysisToPDF } from '~/utils/exportToPDF'
import { exportAnalysisToDOCX } from '~/utils/exportToDOCX'
import { exportLawyerPackToPDF } from '~/utils/exportLawyerPack'
import { WIDGET_REGISTRY, hasContent, getWidgetConfig } from '~/components/analysis/widgets'
import ELI5Toggle from '~/components/analysis/widgets/ELI5Toggle.vue'

definePageMeta({
  middleware: 'auth',
})

const route = useRoute()
const analysesStore = useAnalysesStore()
const authStore = useAuthStore()

const analysisId = computed(() => route.params.id as string)
const showExportModal = ref(false)

// ELI5 Mode state
const eli5Enabled = ref(false)
const eli5Data = ref<any>(null)
const eli5Loading = ref(false)

// Formatted output
const formattedOutput = computed(() => {
  return analysesStore.currentAnalysis?.formatted_output || {}
})

// Widget rendering order
const widgetOrder = [
  'agreement_type',
  'parties',
  'jurisdiction',
  'obligations',
  'rights',
  'payment_terms',
  'calendar',
  'risks',
  'mitigations'
]

// Screening result
const screeningResult = computed(() => {
  const prepResult = analysesStore.currentAnalysis?.preparation_result
  const analysisResult = analysesStore.currentAnalysis?.analysis_result

  return (
    prepResult?.screening_result ||
    analysisResult?.screening_result ||
    formattedOutput.value.screening_result ||
    'preliminary_review'
  )
})

// Confidence reason
const confidenceReason = computed(() => {
  const prepResult = analysesStore.currentAnalysis?.preparation_result
  const analysisResult = analysesStore.currentAnalysis?.analysis_result

  return (
    prepResult?.confidence?.reason ||
    analysisResult?.confidence?.reason ||
    formattedOutput.value.confidence_reason
  )
})

// Get widget component from registry
function getWidgetComponent(key: string) {
  return WIDGET_REGISTRY[key]?.component
}

// Get widget title
function getWidgetTitle(key: string): string {
  const section = formattedOutput.value[key]
  if (section && typeof section === 'object' && 'title' in section && section.title) {
    return section.title
  }
  // Fallback to formatted key name
  return key.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')
}

// Helper function
function getAboutSummary(): string {
  const prepResult = analysesStore.currentAnalysis?.preparation_result
  const analysisResult = analysesStore.currentAnalysis?.analysis_result

  return (
    analysisResult?.about_summary ||
    prepResult?.about ||
    formattedOutput.value.about?.description ||
    ''
  )
}

// ELI5 Mode toggle
async function toggleELI5Mode(): Promise<void> {
  if (eli5Enabled.value) {
    eli5Enabled.value = false
    return
  }

  // If we already have the data, just enable
  if (eli5Data.value) {
    eli5Enabled.value = true
    return
  }

  // Otherwise fetch simplified version
  try {
    eli5Loading.value = true

    const config = useRuntimeConfig()
    const response = await fetch(
      `${config.public.apiBase}/analyses/${analysisId.value}/simplify`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authStore.token}`,
        },
      }
    )

    if (!response.ok) {
      throw new Error('Failed to simplify analysis')
    }

    const data = await response.json()
    eli5Data.value = data.simplified_analysis
    eli5Enabled.value = true
  } catch (error: any) {
    const { error: showError } = useNotifications()
    showError('Failed to simplify', error.message || 'Please try again later.')
  } finally {
    eli5Loading.value = false
  }
}

// Export handlers
function handleExport() {
  showExportModal.value = true
}

async function handleExportFormat(format: 'pdf' | 'docx' | 'json' | 'lawyer-pack'): Promise<void> {
  const analysis = analysesStore.currentAnalysis
  if (!analysis) return

  try {
    if (format === 'pdf') {
      await exportAnalysisToPDF(analysis)
      const { success } = useNotifications()
      success('PDF exported', 'Your analysis has been downloaded as PDF')
    } else if (format === 'docx') {
      await exportAnalysisToDOCX(analysis)
      const { success } = useNotifications()
      success('DOCX exported', 'Your analysis has been downloaded as DOCX')
    } else if (format === 'lawyer-pack') {
      await exportLawyerPackToPDF(analysis)
      const { success } = useNotifications()
      success('Lawyer pack exported', 'Your lawyer pack has been downloaded')
    } else if (format === 'json') {
      const json = JSON.stringify(analysis, null, 2)
      const blob = new Blob([json], { type: 'application/json' })
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `analysis-${analysis.id}.json`
      link.click()
      URL.revokeObjectURL(url)
      const { success } = useNotifications()
      success('JSON exported', 'Your analysis has been downloaded as JSON')
    }
  } catch (error: any) {
    const { error: showError } = useNotifications()
    showError('Export failed', error.message || 'Please try again later.')
  } finally {
    showExportModal.value = false
  }
}

// Format event message
function formatEventMessage(event: AnalysisEvent): string {
  return event.message || event.event_type || 'Processing...'
}

// Lifecycle hooks
onMounted(async () => {
  if (analysisId.value) {
    await analysesStore.fetchAnalysis(analysisId.value)
    if (analysesStore.currentAnalysis?.status === 'processing') {
      analysesStore.connectSSE(analysisId.value)
    }
  }
})

onUnmounted(() => {
  analysesStore.disconnectSSE()
})
</script>
