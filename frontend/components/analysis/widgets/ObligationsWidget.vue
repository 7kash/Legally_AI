<template>
  <BaseWidget :title="title" icon="clipboard" color="blue">
    <div class="space-y-4">
      <div
        v-for="(item, index) in obligations"
        :key="index"
        class="border-l-4 border-blue-500 pl-4 py-3 bg-blue-50 rounded-r-lg"
      >
        <!-- ELI5 Mode - Show simplified text -->
        <p v-if="eli5Enabled && item.action_simple" class="text-gray-800 leading-relaxed">
          {{ item.action_simple }}
        </p>

        <!-- Normal Mode - Show full details -->
        <template v-else>
          <p class="font-semibold text-gray-900">{{ item.action }}</p>

          <!-- Time window and trigger -->
          <div v-if="item.time_window || item.trigger" class="mt-2 space-y-1">
            <p v-if="item.trigger" class="text-sm text-gray-700">
              <span class="font-medium">When:</span> {{ item.trigger }}
            </p>
            <p v-if="item.time_window" class="text-sm text-gray-700">
              <span class="font-medium">Deadline:</span> {{ item.time_window }}
            </p>
          </div>

          <!-- Consequence warning -->
          <p v-if="item.consequence" class="mt-2 text-sm text-red-700 bg-red-50 p-2 rounded">
            <span class="font-medium">⚠️ If not done:</span> {{ item.consequence }}
          </p>
        </template>

        <!-- Quote Toggle -->
        <QuoteToggle
          :quote="item.quote"
          :quote-original="item.quote_original"
          :quote-translated="item.quote_translated"
        />
      </div>

      <div v-if="obligations.length === 0" class="text-gray-500 italic">
        No obligations identified
      </div>
    </div>
  </BaseWidget>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import BaseWidget from './BaseWidget.vue'
import QuoteToggle from './QuoteToggle.vue'

interface Obligation {
  action: string
  action_simple?: string
  time_window?: string
  trigger?: string
  consequence?: string
  quote?: string
  quote_original?: string
  quote_translated?: string
}

interface Props {
  title: string
  content: Obligation[] | { content: Obligation[] } | any
  eli5Enabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  eli5Enabled: false,
})

const obligations = computed<Obligation[]>(() => {
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
