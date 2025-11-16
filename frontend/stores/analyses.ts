import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useAuthStore } from './auth'

/**
 * Analyses Store
 * Manages contract analysis state and operations
 */

export interface Analysis {
  id: string
  contract_id: string
  status: 'queued' | 'running' | 'succeeded' | 'failed'
  confidence_score: number | null
  formatted_output: Record<string, any> | null
  created_at: string
  updated_at: string
  completed_at: string | null
}

export interface AnalysisEvent {
  kind: string
  payload: Record<string, any>
  timestamp: string
}

export const useAnalysesStore = defineStore('analyses', () => {
  // State
  const currentAnalysis = ref<Analysis | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  const events = ref<AnalysisEvent[]>([])
  const eventSource = ref<EventSource | null>(null)
  const sseConnected = ref(false)

  // Computed
  const isAnalyzing = computed(() => {
    return (
      currentAnalysis.value?.status === 'queued' ||
      currentAnalysis.value?.status === 'running'
    )
  })

  const hasResults = computed(() => {
    return currentAnalysis.value?.status === 'succeeded' && currentAnalysis.value?.formatted_output
  })

  const latestEvent = computed(() => {
    return events.value.length > 0 ? events.value[events.value.length - 1] : null
  })

  // Actions
  async function fetchAnalysis(analysisId: string): Promise<void> {
    loading.value = true
    error.value = null

    try {
      const { token } = useAuthStore()
      if (!token) {
        throw new Error('Not authenticated')
      }

      const response = await $fetch<Analysis>(`/analyses/${analysisId}`, {
        method: 'GET',
        baseURL: useRuntimeConfig().public.apiBase,
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      currentAnalysis.value = response
    } catch (err: any) {
      error.value = err.data?.detail || 'Failed to fetch analysis'
      throw err
    } finally {
      loading.value = false
    }
  }

  function connectSSE(analysisId: string): void {
    // Close existing connection if any
    disconnectSSE()

    const { token } = useAuthStore()
    if (!token) {
      error.value = 'Not authenticated'
      return
    }

    const baseURL = useRuntimeConfig().public.apiBase
    const url = `${baseURL}/analyses/${analysisId}/stream`

    // Create EventSource with auth header (via query param since EventSource doesn't support headers)
    const es = new EventSource(`${url}?token=${token}`)

    es.onopen = () => {
      sseConnected.value = true
    }

    es.onmessage = (event) => {
      try {
        const data: AnalysisEvent = JSON.parse(event.data)
        events.value.push(data)

        // Update current analysis status based on event
        if (currentAnalysis.value) {
          // Handle status change events
          if (data.kind === 'status_change' && data.payload.status) {
            currentAnalysis.value.status = data.payload.status

            // Fetch full analysis when status changes to succeeded or failed
            if (data.payload.status === 'succeeded' || data.payload.status === 'failed') {
              fetchAnalysis(analysisId).then(() => {
                // Disconnect SSE after fetching final results
                disconnectSSE()
              })
            }
          }

          // Handle error events
          if (data.kind === 'error') {
            error.value = data.payload.message || 'An error occurred during analysis'
            // Mark analysis as failed on error
            if (currentAnalysis.value.status === 'running' || currentAnalysis.value.status === 'queued') {
              currentAnalysis.value.status = 'failed'
            }
            // Disconnect SSE after error
            disconnectSSE()
          }
        }
      } catch (err) {
        console.error('Failed to parse SSE event:', err)
      }
    }

    es.onerror = (err) => {
      console.error('SSE error:', err)
      sseConnected.value = false
      disconnectSSE()
    }

    // Listen for close event
    es.addEventListener('close', () => {
      disconnectSSE()
    })

    eventSource.value = es
  }

  function disconnectSSE(): void {
    if (eventSource.value) {
      eventSource.value.close()
      eventSource.value = null
      sseConnected.value = false
    }
  }

  async function submitFeedback(
    analysisId: string,
    section: string,
    isCorrect: boolean,
    comment?: string
  ): Promise<void> {
    try {
      const { token } = useAuthStore()
      if (!token) {
        throw new Error('Not authenticated')
      }

      await $fetch(`/analyses/${analysisId}/feedback`, {
        method: 'POST',
        baseURL: useRuntimeConfig().public.apiBase,
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: {
          section,
          is_correct: isCorrect,
          comment,
        },
      })
    } catch (err: any) {
      console.error('Failed to submit feedback:', err)
      throw err
    }
  }

  function clearError(): void {
    error.value = null
  }

  function clearAnalysis(): void {
    currentAnalysis.value = null
    events.value = []
    disconnectSSE()
  }

  return {
    // State
    currentAnalysis,
    loading,
    error,
    events,
    sseConnected,
    // Computed
    isAnalyzing,
    hasResults,
    latestEvent,
    // Actions
    fetchAnalysis,
    connectSSE,
    disconnectSSE,
    submitFeedback,
    clearError,
    clearAnalysis,
  }
})
