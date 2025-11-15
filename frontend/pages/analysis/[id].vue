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
          <!-- Screening Result Badge -->
          <ScreeningBadge
            v-if="screeningResult"
            :variant="screeningResult"
          />

          <!-- Important Limits Disclaimer -->
          <ImportantLimits />

          <!-- Confidence Level -->
          <div
            v-if="analysesStore.currentAnalysis.confidence_score !== null"
            class="bg-white rounded-lg border border-gray-200 p-6"
          >
            <div class="flex items-center justify-between mb-3">
              <h2 class="text-lg font-semibold text-gray-900">
                Confidence Level
              </h2>
              <span
                class="px-3 py-1 rounded-full text-sm font-semibold"
                :class="{
                  'bg-green-100 text-green-800': analysesStore.currentAnalysis.confidence_score >= 0.8,
                  'bg-yellow-100 text-yellow-800': analysesStore.currentAnalysis.confidence_score >= 0.6 && analysesStore.currentAnalysis.confidence_score < 0.8,
                  'bg-red-100 text-red-800': analysesStore.currentAnalysis.confidence_score < 0.6,
                }"
              >
                {{ confidenceLevel }}
              </span>
            </div>
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
            <p v-if="confidenceReason" class="text-sm text-gray-600">
              {{ confidenceReason }}
            </p>
          </div>

          <!-- About the Contract -->
          <div v-if="formattedOutput.about" class="bg-white rounded-lg border border-gray-200 p-6">
            <h2 class="text-xl font-semibold text-gray-900 mb-4">
              About the Contract
            </h2>
            <div class="prose prose-sm max-w-none">
              <p v-if="formattedOutput.about.description" class="text-gray-700 mb-4">
                {{ formattedOutput.about.description }}
              </p>

              <!-- What you pay and when -->
              <div v-if="formattedOutput.payment_terms" class="mb-4">
                <h3 class="text-sm font-semibold text-gray-900 mb-2">
                  What you pay and when:
                </h3>
                <ExpandableList
                  :items="formatPaymentTerms(formattedOutput.payment_terms)"
                  :initial-count="5"
                >
                  <template #item="{ item }">
                    <p class="text-sm text-gray-700">{{ item }}</p>
                  </template>
                </ExpandableList>
              </div>

              <!-- What you agree to do -->
              <div v-if="formattedOutput.obligations" class="mb-4">
                <h3 class="text-sm font-semibold text-gray-900 mb-2">
                  What you agree to do:
                </h3>
                <ExpandableList
                  :items="formattedOutput.obligations"
                  :initial-count="5"
                >
                  <template #item="{ item }">
                    <div class="text-sm">
                      <p class="font-semibold text-gray-900">{{ item.action }}</p>
                      <p v-if="item.time_window" class="text-gray-600 mt-1">
                        When: {{ item.time_window }}
                      </p>
                      <p v-if="item.consequence" class="text-red-600 mt-1">
                        If not done: {{ item.consequence }}
                      </p>
                    </div>
                  </template>
                </ExpandableList>
              </div>
            </div>
          </div>

          <!-- Suggestions -->
          <div v-if="formattedOutput.risks || formattedOutput.rights" class="bg-white rounded-lg border border-gray-200 p-6">
            <h2 class="text-xl font-semibold text-gray-900 mb-4">
              Suggestions
            </h2>

            <!-- Check these terms (Risks) -->
            <div v-if="formattedOutput.risks" class="mb-6">
              <h3 class="text-sm font-semibold text-gray-900 mb-3">
                Check these terms:
              </h3>
              <ExpandableList
                :items="formattedOutput.risks"
                :initial-count="5"
              >
                <template #item="{ item }">
                  <div class="text-sm">
                    <div class="flex items-center gap-2 mb-1">
                      <span
                        class="px-2 py-1 rounded text-xs font-semibold"
                        :class="{
                          'bg-red-100 text-red-800': item.level === 'high',
                          'bg-yellow-100 text-yellow-800': item.level === 'medium',
                          'bg-green-100 text-green-800': item.level === 'low',
                        }"
                      >
                        {{ item.level?.toUpperCase() }}
                      </span>
                      <span v-if="item.category" class="text-gray-600">{{ item.category }}</span>
                    </div>
                    <p class="text-gray-900 mb-1">{{ item.description }}</p>
                    <p v-if="item.recommendation" class="text-blue-700 text-sm">
                      → {{ item.recommendation }}
                    </p>
                  </div>
                </template>
              </ExpandableList>
            </div>

            <!-- Your rights -->
            <div v-if="formattedOutput.rights" class="mb-6">
              <h3 class="text-sm font-semibold text-gray-900 mb-3">
                Your rights:
              </h3>
              <ExpandableList
                :items="formattedOutput.rights"
                :initial-count="5"
              >
                <template #item="{ item }">
                  <div class="text-sm">
                    <p class="font-semibold text-gray-900">{{ item.right }}</p>
                    <p v-if="item.how_to_exercise" class="text-gray-600 mt-1">
                      How: {{ item.how_to_exercise }}
                    </p>
                    <p v-if="item.conditions" class="text-gray-600 mt-1">
                      Conditions: {{ item.conditions }}
                    </p>
                  </div>
                </template>
              </ExpandableList>
            </div>
          </div>

          <!-- All Key Terms (Collapsed by default) -->
          <CollapsibleSection
            title="All Key Terms"
            subtitle="Click to view complete analysis"
            :default-open="false"
          >
            <div class="space-y-4">
              <AnalysisSection
                v-for="(section, key) in formattedOutput"
                :key="key"
                :title="formatSectionTitle(key)"
                :content="section"
                :section-key="key"
                @feedback="handleFeedback"
              />
            </div>
          </CollapsibleSection>

          <!-- Actions -->
          <div class="flex flex-wrap gap-3">
            <button
              type="button"
              class="btn btn--secondary"
              @click="handleExport"
            >
              <svg
                class="h-5 w-5 -ml-1"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fill-rule="evenodd"
                  d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z"
                  clip-rule="evenodd"
                />
              </svg>
              Export Results
            </button>
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
import type { AnalysisEvent } from '~/stores/analyses'
import { exportAnalysisToPDF } from '~/utils/exportToPDF'
import { exportAnalysisToDOCX } from '~/utils/exportToDOCX'

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
const showExportModal = ref(false)

const formattedOutput = computed(() => {
  return analysesStore.currentAnalysis?.formatted_output || {}
})

const screeningResult = computed(() => {
  // Get screening result from analysis (could be in preparation_result or analysis_result)
  const prepResult = analysesStore.currentAnalysis?.preparation_result
  const analysisResult = analysesStore.currentAnalysis?.analysis_result

  return (
    prepResult?.screening_result ||
    analysisResult?.screening_result ||
    formattedOutput.value.screening_result ||
    'preliminary_review'
  )
})

const confidenceLevel = computed(() => {
  const score = analysesStore.currentAnalysis?.confidence_score
  if (!score) return 'Unknown'
  if (score >= 0.8) return 'High'
  if (score >= 0.6) return 'Medium'
  return 'Low'
})

const confidenceReason = computed(() => {
  const prepResult = analysesStore.currentAnalysis?.preparation_result
  const analysisResult = analysesStore.currentAnalysis?.analysis_result

  return (
    prepResult?.confidence?.reason ||
    analysisResult?.confidence?.reason ||
    formattedOutput.value.confidence_reason
  )
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
  // Use the message from the event payload if available
  if (event.payload?.message) {
    return event.payload.message
  }

  // Fallback to event kind-based messages
  switch (event.kind) {
    case 'status_change':
      return event.payload?.status === 'running' ? 'Analysis started' : 'Status changed'
    case 'progress':
      return 'Processing...'
    case 'succeeded':
      return 'Analysis completed successfully!'
    case 'failed':
      return 'Analysis failed'
    case 'error':
      return 'An error occurred'
    default:
      return event.kind || 'Processing...'
  }
}

function formatSectionTitle(key: string): string {
  // Convert snake_case to Title Case
  return key
    .split('_')
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

function formatPaymentTerms(paymentTerms: any): string[] {
  if (Array.isArray(paymentTerms)) {
    return paymentTerms
  }

  if (typeof paymentTerms === 'object' && paymentTerms !== null) {
    const terms: string[] = []

    if (paymentTerms.main_amount) {
      terms.push(`${paymentTerms.main_amount}${paymentTerms.frequency ? ` ${paymentTerms.frequency}` : ''}`)
    }

    if (paymentTerms.deposit_upfront) {
      terms.push(`Deposit: ${paymentTerms.deposit_upfront}`)
    }

    if (paymentTerms.first_due_date) {
      terms.push(`First payment due: ${paymentTerms.first_due_date}`)
    }

    if (paymentTerms.payment_method) {
      terms.push(`Payment method: ${paymentTerms.payment_method}`)
    }

    // Add any other fields
    for (const [key, value] of Object.entries(paymentTerms)) {
      if (!['main_amount', 'deposit_upfront', 'first_due_date', 'payment_method', 'frequency'].includes(key)) {
        terms.push(`${formatSectionTitle(key)}: ${value}`)
      }
    }

    return terms
  }

  return [String(paymentTerms)]
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

    // Show success notification
    const { success } = useNotifications()
    success('Feedback submitted', 'Thank you for your feedback!')
  } catch (error) {
    console.error('Failed to submit feedback:', error)
    const { error: showError } = useNotifications()
    showError('Failed to submit feedback', 'Please try again later.')
  }
}

function handleExport(): void {
  showExportModal.value = true
}

async function handleExportFormat(format: 'pdf' | 'docx' | 'json'): Promise<void> {
  try {
    const { success } = useNotifications()
    const metadata = {
      contractName: `Analysis ${analysisId.value}`,
      analysisDate: new Date(analysesStore.currentAnalysis?.created_at || '').toLocaleDateString(),
      confidenceScore: analysesStore.currentAnalysis?.confidence_score || undefined,
    }

    if (format === 'pdf') {
      await exportAnalysisToPDF({
        title: 'Contract Analysis',
        content: formattedOutput.value,
        metadata,
      })
      success('PDF exported successfully', 'Your analysis has been downloaded as a PDF.')
    } else if (format === 'docx') {
      await exportAnalysisToDOCX({
        title: 'Contract Analysis',
        content: formattedOutput.value,
        metadata,
      })
      success('DOCX exported successfully', 'Your analysis has been downloaded as a Word document.')
    } else if (format === 'json') {
      // Export as JSON
      const data = {
        analysisId: analysisId.value,
        metadata,
        analysis: analysesStore.currentAnalysis,
      }
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `analysis_${analysisId.value}.json`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      URL.revokeObjectURL(url)
      success('JSON exported successfully', 'Your analysis data has been downloaded.')
    }
  } catch (error) {
    console.error('Failed to export analysis:', error)
    const { error: showError } = useNotifications()
    showError('Export failed', 'Please try again later.')
  }
}

// Set page title
useHead({
  title: 'Analysis Results',
})
</script>
