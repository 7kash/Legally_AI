<template>
  <BaseWidget :title="title" icon="calendar" color="purple">
    <div class="space-y-3">
      <div
        v-for="(event, index) in events"
        :key="index"
        class="flex items-start gap-3 p-3 bg-purple-50 rounded-lg border-l-2 border-purple-500"
      >
        <div class="flex-1">
          <p class="font-semibold text-gray-900">{{ event.date_or_formula || event.date || event.formula }}</p>
          <p class="text-sm text-gray-700 mt-1">
            {{ event.event || event.title || 'Event' }}
          </p>
        </div>
      </div>
      <div v-if="events.length === 0" class="text-gray-500 italic">
        No key dates identified
      </div>
    </div>
  </BaseWidget>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import BaseWidget from './BaseWidget.vue'

interface CalendarEvent {
  date_or_formula?: string
  event?: string
  title?: string
  date?: string
  formula?: string
}

interface Props {
  title: string
  content: CalendarEvent[] | { content: CalendarEvent[] } | any
}

const props = defineProps<Props>()

const events = computed<CalendarEvent[]>(() => {
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
