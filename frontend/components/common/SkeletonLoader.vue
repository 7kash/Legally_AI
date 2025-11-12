<template>
  <div
    class="skeleton"
    :class="skeletonClass"
    :style="skeletonStyle"
    aria-busy="true"
    aria-live="polite"
  >
    <span class="sr-only">Loading...</span>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

/**
 * Skeleton Loader Component
 * Shows loading placeholder animation
 */

interface Props {
  variant?: 'text' | 'circle' | 'rect' | 'card'
  width?: string
  height?: string
  count?: number
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'text',
  width: '100%',
  height: undefined,
  count: 1,
})

const skeletonClass = computed(() => {
  const classes = ['skeleton']

  if (props.variant === 'circle') {
    classes.push('skeleton--circle')
  } else if (props.variant === 'text') {
    classes.push('skeleton--text')
  } else if (props.variant === 'card') {
    classes.push('skeleton--card')
  }

  return classes.join(' ')
})

const skeletonStyle = computed(() => {
  const style: Record<string, string> = {
    width: props.width,
  }

  if (props.height) {
    style.height = props.height
  } else if (props.variant === 'circle') {
    style.height = props.width
  } else if (props.variant === 'text') {
    style.height = '1rem'
  } else if (props.variant === 'card') {
    style.height = '200px'
  }

  return style
})
</script>

<style lang="scss" scoped>
.skeleton {
  @apply animate-pulse bg-gray-200 dark:bg-gray-700;
  border-radius: var(--radius-md);

  &--circle {
    border-radius: 50%;
  }

  &--text {
    border-radius: var(--radius-sm);
  }

  &--card {
    border-radius: var(--radius-lg);
  }
}

@keyframes shimmer {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}
</style>
