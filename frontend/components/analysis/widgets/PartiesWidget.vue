<template>
  <BaseWidget :title="title" icon="users">
    <div class="space-y-3">
      <div
        v-for="(party, index) in parties"
        :key="index"
        class="flex items-start gap-3 p-3 bg-gray-50 rounded-lg"
      >
        <div class="flex-1">
          <p class="font-semibold text-gray-900">
            {{ party.name || `Party ${index + 1}` }}
          </p>
          <p v-if="party.role" class="text-sm text-gray-600">
            {{ party.role }}
          </p>
        </div>
      </div>
    </div>
  </BaseWidget>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import BaseWidget from './BaseWidget.vue'

interface Party {
  name?: string
  role?: string
}

interface Props {
  title: string
  content: Party[] | { content: Party[] } | any
}

const props = defineProps<Props>()

const parties = computed<Party[]>(() => {
  // Handle different content formats
  if (Array.isArray(props.content)) {
    return props.content
  }

  if (props.content && typeof props.content === 'object' && 'content' in props.content) {
    if (Array.isArray(props.content.content)) {
      return props.content.content
    }
  }

  return []
})
</script>
