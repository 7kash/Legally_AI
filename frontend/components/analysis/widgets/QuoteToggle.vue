<template>
  <div>
    <!-- Clickable "Tell me more" button when quote exists -->
    <button
      v-if="hasValidQuote"
      type="button"
      class="mt-3 text-xs text-blue-600 hover:text-blue-700 font-medium flex items-center gap-1 cursor-pointer"
      @click="toggleExpanded"
    >
      <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      {{ isExpanded ? 'Hide source' : 'Tell me more about it' }}
    </button>

    <!-- Non-clickable "Not found" message when no quote -->
    <div
      v-else
      class="mt-3 text-xs text-gray-400 font-medium flex items-center gap-1"
    >
      <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      Not found in the document text
    </div>

    <!-- Expanded quote display -->
    <div
      v-if="isExpanded && hasValidQuote"
      class="mt-2 bg-white border border-gray-300 rounded-lg p-4 text-sm space-y-3"
    >
      <!-- Original quote -->
      <div v-if="quote || quoteOriginal">
        <p class="font-semibold text-gray-900 mb-2 flex items-center gap-1">
          <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          Original contract text:
        </p>
        <p class="italic text-gray-700 bg-gray-50 p-3 rounded border-l-2 border-blue-400">
          "{{ quoteOriginal || quote }}"
        </p>
      </div>

      <!-- Translated quote (if different from original) -->
      <div v-if="quoteTranslated && quoteTranslated !== quoteOriginal && quoteTranslated !== quote">
        <p class="font-semibold text-gray-900 mb-2 flex items-center gap-1">
          <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129" />
          </svg>
          English translation:
        </p>
        <p class="text-gray-700 bg-amber-50 p-3 rounded border-l-2 border-amber-600">
          "{{ quoteTranslated }}"
        </p>
      </div>

      <!-- Related risk quote (for mitigations) -->
      <div v-if="relatedRiskQuote">
        <p class="font-semibold text-gray-900 mb-2 flex items-center gap-1">
          <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          Related risk from contract:
        </p>
        <p class="italic text-gray-700 bg-red-50 p-3 rounded border-l-2 border-red-400">
          "{{ relatedRiskQuote }}"
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

interface Props {
  quote?: string | null
  quoteOriginal?: string | null
  quoteTranslated?: string | null
  relatedRiskQuote?: string | null
}

const props = defineProps<Props>()

const isExpanded = ref(false)

const hasValidQuote = computed(() => {
  const checkQuote = (q: string | null | undefined): boolean => {
    if (!q) return false
    if (typeof q !== 'string') return false
    const trimmed = q.trim().toLowerCase()
    if (trimmed === '' || trimmed === 'null' || trimmed === 'undefined' || trimmed === 'none') return false
    // Treat "Not explicitly stated" as no quote
    if (trimmed.includes('not explicitly stated') || trimmed.includes('not stated')) return false
    return true
  }

  return (
    checkQuote(props.quote) ||
    checkQuote(props.quoteOriginal) ||
    checkQuote(props.relatedRiskQuote)
  )
})

function toggleExpanded() {
  isExpanded.value = !isExpanded.value
}
</script>
