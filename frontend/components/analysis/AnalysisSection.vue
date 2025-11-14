<template>
  <section class="bg-white rounded-lg border border-gray-200 p-6">
    <!-- Section Header -->
    <div class="flex items-start justify-between mb-4">
      <h2 class="text-xl font-semibold text-gray-900">
        {{ title }}
      </h2>

      <!-- Feedback buttons -->
      <div class="flex items-center gap-2">
        <button
          type="button"
          class="p-2 rounded-lg text-gray-400 hover:bg-green-50 hover:text-green-600 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-green-500"
          :class="{ 'bg-green-50 text-green-600': feedbackGiven && isCorrect }"
          :aria-label="`Mark ${title} as correct`"
          :aria-pressed="feedbackGiven && isCorrect"
          @click="handleFeedback(true)"
        >
          <svg
            class="h-5 w-5"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 20 20"
            fill="currentColor"
            aria-hidden="true"
          >
            <path
              d="M1 8.25a1.25 1.25 0 112.5 0v7.5a1.25 1.25 0 11-2.5 0v-7.5zM11 3V1.7c0-.268.14-.526.395-.607A2 2 0 0114 3c0 .995-.182 1.948-.514 2.826-.204.54.166 1.174.744 1.174h2.52c1.243 0 2.261 1.01 2.146 2.247a23.864 23.864 0 01-1.341 5.974C17.153 16.323 16.072 17 14.9 17h-3.192a3 3 0 01-1.341-.317l-2.734-1.366A3 3 0 006.292 15H5V8h.963c.685 0 1.258-.483 1.612-1.068a4.011 4.011 0 012.166-1.73c.432-.143.853-.386 1.011-.814.16-.432.248-.9.248-1.388z"
            />
          </svg>
        </button>
        <button
          type="button"
          class="p-2 rounded-lg text-gray-400 hover:bg-red-50 hover:text-red-600 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-red-500"
          :class="{ 'bg-red-50 text-red-600': feedbackGiven && !isCorrect }"
          :aria-label="`Mark ${title} as incorrect`"
          :aria-pressed="feedbackGiven && !isCorrect"
          @click="handleFeedback(false)"
        >
          <svg
            class="h-5 w-5"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 20 20"
            fill="currentColor"
            aria-hidden="true"
          >
            <path
              d="M18.905 12.75a1.25 1.25 0 01-2.5 0v-7.5a1.25 1.25 0 112.5 0v7.5zM8.905 17v1.3c0 .268-.14.526-.395.607A2 2 0 015.905 17c0-.995.182-1.948.514-2.826.204-.54-.166-1.174-.744-1.174h-2.52c-1.243 0-2.261-1.01-2.146-2.247.193-2.08.651-4.082 1.341-5.974C2.752 3.678 3.833 3 5.005 3h3.192a3 3 0 011.341.317l2.734 1.366A3 3 0 0013.613 5h1.292v7h-.963c-.685 0-1.258.482-1.612 1.068a4.01 4.01 0 01-2.166 1.73c-.432.143-.853.386-1.011.814-.16.432-.248.9-.248 1.388z"
            />
          </svg>
        </button>
      </div>
    </div>

    <!-- Section Content -->
    <div class="prose prose-sm max-w-none">
      <!-- Render as list if array -->
      <ul v-if="Array.isArray(content)" class="space-y-2 list-disc list-inside">
        <li
          v-for="(item, index) in content"
          :key="index"
          class="text-gray-700"
        >
          {{ item }}
        </li>
      </ul>

      <!-- Render as text if string -->
      <div
        v-else-if="typeof content === 'string'"
        class="text-gray-700 whitespace-pre-wrap"
      >
        {{ content }}
      </div>

      <!-- Render as key-value pairs if object -->
      <dl v-else-if="typeof content === 'object' && content !== null" class="space-y-3">
        <div
          v-for="(value, key) in content"
          :key="key"
          class="border-l-4 border-primary-200 pl-4"
        >
          <dt class="text-sm font-medium text-gray-900">
            {{ formatKey(key) }}
          </dt>
          <dd class="mt-1 text-gray-700">
            <!-- Recursive rendering for nested objects/arrays -->
            <ul v-if="Array.isArray(value)" class="mt-1 space-y-1 list-disc list-inside">
              <li
                v-for="(item, idx) in value"
                :key="idx"
              >
                {{ item }}
              </li>
            </ul>
            <span v-else>{{ value }}</span>
          </dd>
        </div>
      </dl>

      <!-- Fallback -->
      <p v-else class="text-gray-500 italic">
        No data available for this section
      </p>
    </div>

    <!-- Feedback comment (shown after giving feedback) -->
    <div v-if="showCommentInput" class="mt-4 pt-4 border-t border-gray-200">
      <label
        for="feedback-comment"
        class="block text-sm font-medium text-gray-700 mb-2"
      >
        Additional comments (optional)
      </label>
      <textarea
        id="feedback-comment"
        v-model="comment"
        rows="3"
        class="input w-full"
        placeholder="Tell us more about your feedback..."
      />
      <div class="mt-2 flex gap-2">
        <button
          type="button"
          class="btn btn--primary btn-sm"
          @click="submitComment"
        >
          Submit Feedback
        </button>
        <button
          type="button"
          class="btn btn--secondary btn-sm"
          @click="cancelComment"
        >
          Cancel
        </button>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'

/**
 * AnalysisSection Component
 * Displays a single section of the analysis with feedback options
 */

interface Props {
  title: string
  content: any
  sectionKey: string
}

interface Emits {
  (e: 'feedback', data: { sectionKey: string; isCorrect: boolean; comment?: string }): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

// State
const feedbackGiven = ref(false)
const isCorrect = ref(false)
const showCommentInput = ref(false)
const comment = ref('')

// Methods
function handleFeedback(correct: boolean): void {
  feedbackGiven.value = true
  isCorrect.value = correct
  showCommentInput.value = true
}

function submitComment(): void {
  emit('feedback', {
    sectionKey: props.sectionKey,
    isCorrect: isCorrect.value,
    comment: comment.value || undefined,
  })

  showCommentInput.value = false
  comment.value = ''
}

function cancelComment(): void {
  showCommentInput.value = false
  comment.value = ''
  feedbackGiven.value = false
}

function formatKey(key: string | number): string {
  if (typeof key === 'number') return `${key + 1}`

  // Convert snake_case to Title Case
  return String(key)
    .split('_')
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}
</script>

<style lang="scss" scoped>
.btn-sm {
  @apply px-3 py-1.5 text-sm;
}
</style>
