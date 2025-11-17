<template>
  <BaseWidget :title="title" icon="warning" color="red">
    <div class="space-y-4">
      <div
        v-for="(item, index) in risks"
        :key="index"
        class="border-l-4 pl-4 py-3 rounded-r-lg"
        :class="getRiskBorderColor(item.level)"
      >
        <!-- Risk level badge and category -->
        <div class="flex items-center gap-2 mb-2">
          <span
            class="px-2 py-1 rounded text-xs font-medium uppercase"
            :class="getRiskBadgeColor(item.level)"
          >
            {{ item.level || 'unknown' }}
          </span>
          <span v-if="item.category" class="text-sm text-gray-600">
            {{ item.category }}
          </span>
        </div>

        <!-- ELI5 Mode - Show simplified description -->
        <p v-if="eli5Enabled && item.description_simple" class="text-gray-800 leading-relaxed whitespace-pre-line">
          {{ item.description_simple }}
        </p>

        <!-- Normal Mode - Show full description -->
        <template v-else>
          <p class="text-gray-900">{{ item.description }}</p>

          <!-- Recommendation -->
          <p v-if="item.recommendation" class="mt-2 text-sm text-blue-700 bg-blue-50 p-2 rounded">
            <span class="font-medium">💡 Recommendation:</span> {{ item.recommendation }}
          </p>
        </template>

        <!-- Quote Toggle -->
        <QuoteToggle
          :quote="item.quote"
          :quote-original="item.quote_original"
          :quote-translated="item.quote_translated"
        />
      </div>

      <div v-if="risks.length === 0" class="text-gray-500 italic">
        No risks identified
      </div>
    </div>
  </BaseWidget>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import BaseWidget from './BaseWidget.vue'
import QuoteToggle from './QuoteToggle.vue'

interface Risk {
  level?: string
  category?: string
  description: string
  description_simple?: string
  recommendation?: string
  quote?: string
  quote_original?: string
  quote_translated?: string
}

interface Props {
  title: string
  content: Risk[] | { content: Risk[] } | any
  eli5Enabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  eli5Enabled: false,
})

const risks = computed<Risk[]>(() => {
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

function getRiskBadgeColor(level?: string): string {
  const levelLower = (level || 'unknown').toLowerCase()

  const colors: Record<string, string> = {
    high: 'bg-red-100 text-red-800',
    medium: 'bg-yellow-100 text-yellow-800',
    low: 'bg-green-100 text-green-800',
  }

  return colors[levelLower] || 'bg-gray-100 text-gray-800'
}

function getRiskBorderColor(level?: string): string {
  const levelLower = (level || 'unknown').toLowerCase()

  const colors: Record<string, string> = {
    high: 'border-red-500 bg-red-50',
    medium: 'border-yellow-500 bg-yellow-50',
    low: 'border-green-500 bg-green-50',
  }

  return colors[levelLower] || 'border-gray-500 bg-gray-50'
}
</script>
