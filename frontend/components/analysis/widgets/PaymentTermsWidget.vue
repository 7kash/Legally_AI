<template>
  <BaseWidget :title="title" icon="currency" color="emerald">
    <div class="space-y-3">
      <div
        v-for="(term, index) in terms"
        :key="index"
        class="flex items-start gap-3 p-3 bg-emerald-50 rounded-lg border-l-2 border-emerald-500"
      >
        <p class="text-gray-800">{{ term }}</p>
      </div>
      <div v-if="terms.length === 0" class="text-gray-500 italic">
        No payment terms identified
      </div>
    </div>
  </BaseWidget>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import BaseWidget from './BaseWidget.vue'

interface Props {
  title: string
  content: string[] | { content: string[] | object } | object | any
}

const props = defineProps<Props>()

const terms = computed<string[]>(() => {
  let data = props.content

  // Unwrap {content: ...} structure
  if (data && typeof data === 'object' && 'content' in data) {
    data = data.content
  }

  // If it's already an array of strings, return it
  if (Array.isArray(data)) {
    return data.filter(item => typeof item === 'string')
  }

  // If it's an object, convert to key-value strings
  if (data && typeof data === 'object') {
    const termStrings: string[] = []
    Object.entries(data).forEach(([key, value]) => {
      if (value && typeof value === 'string') {
        const formattedKey = key.replace(/_/g, ' ')
        termStrings.push(`${formattedKey}: ${value}`)
      }
    })
    return termStrings
  }

  return []
})
</script>
