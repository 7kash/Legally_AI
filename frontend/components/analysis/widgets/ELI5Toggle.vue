<template>
  <div class="space-y-4">
    <!-- Toggle Button -->
    <div class="flex items-center justify-center">
      <button
        type="button"
        class="inline-flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all"
        :class="{
          'bg-purple-600 text-white hover:bg-purple-700': modelValue,
          'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50': !modelValue
        }"
        :disabled="loading"
        @click="handleToggle"
      >
        <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
        <span v-if="loading">Simplifying...</span>
        <span v-else-if="modelValue">Simple Mode (ON)</span>
        <span v-else>Explain Like I'm 5</span>
      </button>
    </div>

    <!-- Info Banner (when active) -->
    <div
      v-if="modelValue"
      class="bg-purple-50 border border-purple-200 rounded-lg p-4 flex items-start gap-3"
    >
      <svg class="h-5 w-5 text-purple-600 flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <div>
        <p class="text-sm font-medium text-purple-900">Simple Mode Active</p>
        <p class="text-sm text-purple-700">Legal terms are now explained in everyday language that's easy to understand.</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  modelValue: boolean
  loading?: boolean
}

interface Emits {
  (e: 'update:modelValue', value: boolean): void
  (e: 'toggle'): void
}

defineProps<Props>()
const emit = defineEmits<Emits>()

function handleToggle() {
  emit('toggle')
}
</script>
