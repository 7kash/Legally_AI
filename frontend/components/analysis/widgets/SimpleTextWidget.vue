<template>
  <BaseWidget :title="title" :icon="icon" :color="color">
    <p class="text-gray-800 font-medium">{{ displayContent }}</p>
  </BaseWidget>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import BaseWidget from './BaseWidget.vue'

interface Props {
  title: string
  content: string | { content: string } | any
  icon?: string
  color?: 'blue' | 'green' | 'red' | 'purple' | 'amber' | 'emerald'
}

const props = withDefaults(defineProps<Props>(), {
  icon: 'document',
  color: undefined,
})

const displayContent = computed(() => {
  // Handle different content formats
  if (typeof props.content === 'string') {
    return props.content
  }

  if (props.content && typeof props.content === 'object') {
    if ('content' in props.content && typeof props.content.content === 'string') {
      return props.content.content
    }
  }

  return String(props.content || '')
})
</script>
