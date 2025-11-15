<template>
  <div
    class="rounded-lg border-2 border-amber-300 bg-amber-50 p-5"
    role="alert"
    aria-labelledby="disclaimer-title"
  >
    <div class="flex items-start gap-3">
      <!-- Warning Icon -->
      <svg
        class="mt-0.5 h-6 w-6 flex-shrink-0 text-amber-600"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 20 20"
        fill="currentColor"
        aria-hidden="true"
      >
        <path
          fill-rule="evenodd"
          d="M8.485 2.495c.673-1.167 2.357-1.167 3.03 0l6.28 10.875c.673 1.167-.17 2.625-1.516 2.625H3.72c-1.347 0-2.189-1.458-1.515-2.625L8.485 2.495zM10 5a.75.75 0 01.75.75v3.5a.75.75 0 01-1.5 0v-3.5A.75.75 0 0110 5zm0 9a1 1 0 100-2 1 1 0 000 2z"
          clip-rule="evenodd"
        />
      </svg>

      <!-- Content -->
      <div>
        <h4
          id="disclaimer-title"
          class="mb-2 font-semibold text-amber-900"
        >
          Important Limits
        </h4>
        <div class="space-y-2 text-sm text-amber-800">
          <p>
            <strong>This is an AI-powered informational screening</strong> — not legal advice, not a law-firm review, and it does not create an attorney–client relationship.
          </p>
          <p>
            We flag risks and highlight terms based on patterns, but we don't know your specific situation. Always consult a qualified lawyer before signing any contract, especially if money, property, or legal obligations are involved.
          </p>
          <p>
            <strong>Use this summary to ask better questions</strong>, not as a substitute for professional legal counsel.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
/**
 * Important Limits Disclaimer Component
 * Displays the mandatory disclaimer per the lawyer's specification
 */
</script>
