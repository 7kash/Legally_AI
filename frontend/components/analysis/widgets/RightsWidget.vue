<template>
  <BaseWidget :title="title" icon="shield" color="green">
    <div class="space-y-4">
      <div
        v-for="(item, index) in rights"
        :key="index"
        class="border-l-4 border-green-500 pl-4 py-3 bg-green-50 rounded-r-lg"
      >
        <!-- ELI5 Mode - Show simplified text -->
        <p v-if="eli5Enabled && item.right_simple" class="text-gray-800 leading-relaxed whitespace-pre-line">
          {{ item.right_simple }}
        </p>

        <!-- Normal Mode - Show full details -->
        <template v-else>
          <p class="font-semibold text-gray-900">{{ item.right }}</p>

          <!-- How to exercise and conditions -->
          <div v-if="item.how_to_exercise || item.conditions" class="mt-2 space-y-1">
            <p v-if="item.how_to_exercise" class="text-sm text-gray-700">
              <span class="font-medium">How to use:</span> {{ item.how_to_exercise }}
            </p>
            <p v-if="item.conditions" class="text-sm text-gray-700">
              <span class="font-medium">Conditions:</span> {{ item.conditions }}
            </p>
          </div>
        </template>

        <!-- Quote Toggle -->
        <QuoteToggle
          :quote="item.quote"
          :quote-original="item.quote_original"
          :quote-translated="item.quote_translated"
        />
      </div>

      <div v-if="rights.length === 0" class="text-gray-500 italic">
        No rights identified
      </div>
    </div>
  </BaseWidget>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import BaseWidget from './BaseWidget.vue'
import QuoteToggle from './QuoteToggle.vue'

interface Right {
  right: string
  right_simple?: string
  how_to_exercise?: string
  conditions?: string
  quote?: string
  quote_original?: string
  quote_translated?: string
}

interface Props {
  title: string
  content: Right[] | { content: Right[] } | any
  eli5Enabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  eli5Enabled: false,
})

const rights = computed<Right[]>(() => {
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
