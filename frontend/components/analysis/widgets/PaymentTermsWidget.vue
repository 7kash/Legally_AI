<template>
  <BaseWidget :title="title" icon="currency" color="emerald">
    <div class="space-y-4">
      <div
        v-for="(term, key) in validTerms"
        :key="key"
        class="border-l-4 border-emerald-500 pl-4 py-3 bg-emerald-50 rounded-r-lg"
      >
        <p class="text-sm text-gray-600 font-medium">{{ formatKey(key) }}</p>
        <p class="text-gray-900 font-semibold mt-1">{{ term.value }}</p>

        <!-- Quote Toggle -->
        <QuoteToggle
          v-if="term.quote || term.quote_original || term.quote_translated"
          :quote="term.quote"
          :quote-original="term.quote_original"
          :quote-translated="term.quote_translated"
        />
      </div>

      <div v-if="Object.keys(validTerms).length === 0" class="text-gray-500 italic">
        No payment terms identified
      </div>
    </div>
  </BaseWidget>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import BaseWidget from './BaseWidget.vue'
import QuoteToggle from './QuoteToggle.vue'

interface PaymentTerm {
  value: string
  quote?: string
  quote_original?: string
  quote_translated?: string
}

interface Props {
  title: string
  content: Record<string, any> | { content: Record<string, any> } | any
}

const props = defineProps<Props>()

const validTerms = computed<Record<string, PaymentTerm>>(() => {
  let data = props.content

  // Unwrap {content: ...} structure
  if (data && typeof data === 'object' && 'content' in data) {
    data = data.content
  }

  if (!data || typeof data !== 'object') {
    return {}
  }

  const terms: Record<string, PaymentTerm> = {}

  Object.entries(data).forEach(([key, value]) => {
    // Skip null, undefined, "null" string values
    if (!value || value === 'null' || value === 'undefined') {
      return
    }

    // Skip the taxes_fees_note if it says "not analyzed"
    if (key === 'taxes_fees_note' && typeof value === 'string' && value.toLowerCase().includes('not analyzed')) {
      return
    }

    // If value is a string, use it directly
    if (typeof value === 'string') {
      terms[key] = { value }
    }
    // If value is an object with nested properties
    else if (typeof value === 'object' && value !== null) {
      const valueStr = value.amount || value.value || JSON.stringify(value)
      terms[key] = {
        value: valueStr,
        quote: value.quote,
        quote_original: value.quote_original,
        quote_translated: value.quote_translated
      }
    }
  })

  return terms
})

function formatKey(key: string): string {
  // Convert snake_case to Title Case
  return key
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}
</script>
