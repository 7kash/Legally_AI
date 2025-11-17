<template>
  <BaseWidget :title="title" icon="shield-check" color="amber">
    <p class="text-sm text-gray-600 mb-4">
      If you must sign without changes, take these steps to reduce risks:
    </p>

    <div class="space-y-4">
      <div
        v-for="(item, index) in mitigations"
        :key="index"
        class="border-l-4 border-amber-500 pl-4 py-3 bg-amber-50 rounded-r-lg"
      >
        <!-- ELI5 Mode - Show simplified text -->
        <p v-if="eli5Enabled && typeof item === 'object' && item.mitigation_simple" class="text-gray-800 leading-relaxed whitespace-pre-line">
          {{ item.mitigation_simple }}
        </p>

        <!-- Normal Mode - Show full details -->
        <template v-else>
          <p class="font-semibold text-gray-900">{{ item.mitigation || item.action || item }}</p>

          <p v-if="typeof item === 'object' && item.rationale" class="mt-2 text-sm text-gray-700">
            <span class="font-medium">Why:</span> {{ item.rationale }}
          </p>

          <p v-if="typeof item === 'object' && item.when" class="mt-1 text-sm text-gray-700">
            <span class="font-medium">When:</span> {{ item.when }}
          </p>
        </template>

        <!-- Quote Toggle (supports both regular quote and related_risk_quote) -->
        <QuoteToggle
          v-if="typeof item === 'object'"
          :quote="item.quote"
          :quote-original="item.quote_original"
          :quote-translated="item.quote_translated"
          :related-risk-quote="item.related_risk_quote"
        />
      </div>

      <div v-if="mitigations.length === 0" class="text-gray-500 italic">
        No mitigations needed
      </div>
    </div>
  </BaseWidget>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import BaseWidget from './BaseWidget.vue'
import QuoteToggle from './QuoteToggle.vue'

interface Mitigation {
  mitigation?: string
  mitigation_simple?: string
  action?: string
  rationale?: string
  when?: string
  quote?: string
  quote_original?: string
  quote_translated?: string
  related_risk_quote?: string
}

interface Props {
  title: string
  content: (Mitigation | string)[] | { content: (Mitigation | string)[] } | any
  eli5Enabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  eli5Enabled: false,
})

const mitigations = computed<(Mitigation | string)[]>(() => {
  let data = props.content

  // Unwrap {content: ...} structure
  if (data && typeof data === 'object' && 'content' in data) {
    data = data.content
  }

  // If it's already an array, return it
  if (Array.isArray(data)) {
    return data
  }

  return []
})
</script>
