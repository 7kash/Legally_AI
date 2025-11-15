<template>
  <div class="space-y-3">
    <!-- Display limited items initially -->
    <div
      v-for="(item, index) in displayedItems"
      :key="index"
      class="border-l-4 border-blue-200 bg-blue-50 p-4 rounded-r-lg"
    >
      <slot name="item" :item="item" :index="index">
        {{ item }}
      </slot>
    </div>

    <!-- "More" button if there are more items -->
    <button
      v-if="!showAll && items.length > initialCount"
      type="button"
      class="flex w-full items-center justify-center gap-2 rounded-lg border-2 border-gray-200 bg-white px-4 py-3 text-sm font-medium text-gray-700 transition-all hover:border-primary-500 hover:bg-primary-50 hover:text-primary-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-primary-500"
      @click="showAll = true"
    >
      <svg
        class="h-5 w-5"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 20 20"
        fill="currentColor"
      >
        <path
          fill-rule="evenodd"
          d="M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z"
          clip-rule="evenodd"
        />
      </svg>
      <span>Show {{ items.length - initialCount }} more</span>
    </button>

    <!-- "Show Less" button when expanded -->
    <button
      v-if="showAll && items.length > initialCount"
      type="button"
      class="flex w-full items-center justify-center gap-2 rounded-lg border-2 border-gray-200 bg-white px-4 py-3 text-sm font-medium text-gray-700 transition-all hover:border-primary-500 hover:bg-primary-50 hover:text-primary-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-primary-500"
      @click="showAll = false"
    >
      <svg
        class="h-5 w-5"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 20 20"
        fill="currentColor"
      >
        <path
          fill-rule="evenodd"
          d="M14.77 12.79a.75.75 0 01-1.06-.02L10 8.832 6.29 12.77a.75.75 0 11-1.08-1.04l4.25-4.5a.75.75 0 011.08 0l4.25 4.5a.75.75 0 01-.02 1.06z"
          clip-rule="evenodd"
        />
      </svg>
      <span>Show less</span>
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

interface Props {
  items: any[]
  initialCount?: number
}

const props = withDefaults(defineProps<Props>(), {
  initialCount: 5,
})

const showAll = ref(false)

const displayedItems = computed(() => {
  if (showAll.value) {
    return props.items
  }
  return props.items.slice(0, props.initialCount)
})
</script>
