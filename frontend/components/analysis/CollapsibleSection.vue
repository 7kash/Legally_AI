<template>
  <div class="rounded-lg border border-gray-300 bg-white overflow-hidden">
    <!-- Header (clickable) -->
    <button
      type="button"
      class="flex w-full items-center justify-between bg-gray-50 px-6 py-4 text-left transition-colors hover:bg-gray-100 focus:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-primary-500"
      :aria-expanded="isOpen"
      @click="toggle"
    >
      <div>
        <h3 class="text-lg font-semibold text-gray-900">
          {{ title }}
        </h3>
        <p v-if="subtitle" class="mt-1 text-sm text-gray-600">
          {{ subtitle }}
        </p>
      </div>

      <!-- Chevron icon -->
      <svg
        class="h-5 w-5 text-gray-500 transition-transform"
        :class="{ 'rotate-180': isOpen }"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 20 20"
        fill="currentColor"
        aria-hidden="true"
      >
        <path
          fill-rule="evenodd"
          d="M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z"
          clip-rule="evenodd"
        />
      </svg>
    </button>

    <!-- Content (collapsible) -->
    <Transition
      name="collapse"
      @enter="onEnter"
      @after-enter="onAfterEnter"
      @leave="onLeave"
    >
      <div v-if="isOpen" class="overflow-hidden">
        <div class="px-6 py-4 border-t border-gray-200">
          <slot />
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Props {
  title: string
  subtitle?: string
  defaultOpen?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  defaultOpen: false,
})

const isOpen = ref(props.defaultOpen)

function toggle(): void {
  isOpen.value = !isOpen.value
}

// Animation helpers
function onEnter(el: Element): void {
  const element = el as HTMLElement
  element.style.height = '0'
  // Force reflow
  element.offsetHeight
  element.style.height = element.scrollHeight + 'px'
}

function onAfterEnter(el: Element): void {
  const element = el as HTMLElement
  element.style.height = 'auto'
}

function onLeave(el: Element): void {
  const element = el as HTMLElement
  element.style.height = element.scrollHeight + 'px'
  // Force reflow
  element.offsetHeight
  element.style.height = '0'
}
</script>

<style scoped>
.collapse-enter-active,
.collapse-leave-active {
  transition: height 0.3s ease;
}

.collapse-enter-from,
.collapse-leave-to {
  height: 0;
}
</style>
