<template>
  <Teleport to="body">
    <Transition name="modal">
      <div
        v-if="modelValue"
        class="fixed inset-0 z-50 overflow-y-auto"
        aria-labelledby="modal-title"
        role="dialog"
        aria-modal="true"
      >
        <!-- Backdrop -->
        <div
          class="fixed inset-0 bg-gray-900 bg-opacity-75 transition-opacity"
          @click="close"
        />

        <!-- Modal container -->
        <div class="flex min-h-full items-center justify-center p-4">
          <div
            class="relative w-full max-w-lg transform overflow-hidden rounded-xl bg-white shadow-2xl transition-all"
          >
            <!-- Header -->
            <div class="border-b border-gray-200 px-6 py-4">
              <div class="flex items-center justify-between">
                <h3
                  id="modal-title"
                  class="text-xl font-semibold text-gray-900"
                >
                  Export Analysis
                </h3>
                <button
                  type="button"
                  class="rounded-lg p-1 text-gray-400 hover:bg-gray-100 hover:text-gray-600 focus:outline-none focus-visible:ring-2 focus-visible:ring-primary-500"
                  @click="close"
                >
                  <span class="sr-only">Close</span>
                  <svg
                    class="h-6 w-6"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M6 18L18 6M6 6l12 12"
                    />
                  </svg>
                </button>
              </div>
            </div>

            <!-- Body -->
            <div class="px-6 py-4">
              <p class="mb-6 text-sm text-gray-600">
                Choose a format to download your contract analysis results.
              </p>

              <!-- Export options -->
              <div class="space-y-3">
                <!-- PDF Export -->
                <button
                  type="button"
                  class="flex w-full items-center justify-between rounded-lg border-2 border-gray-200 p-4 text-left transition-all hover:border-primary-500 hover:bg-primary-50 focus:outline-none focus-visible:ring-2 focus-visible:ring-primary-500"
                  :disabled="exporting"
                  @click="exportFormat('pdf')"
                >
                  <div class="flex items-center gap-3">
                    <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-red-100">
                      <svg
                        class="h-6 w-6 text-red-600"
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          stroke-width="2"
                          d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"
                        />
                      </svg>
                    </div>
                    <div>
                      <div class="font-semibold text-gray-900">
                        PDF Document
                      </div>
                      <div class="text-sm text-gray-600">
                        Professional, print-ready format
                      </div>
                    </div>
                  </div>
                  <svg
                    class="h-5 w-5 text-gray-400"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                  >
                    <path
                      fill-rule="evenodd"
                      d="M7.21 14.77a.75.75 0 01.02-1.06L11.168 10 7.23 6.29a.75.75 0 111.04-1.08l4.5 4.25a.75.75 0 010 1.08l-4.5 4.25a.75.75 0 01-1.06-.02z"
                      clip-rule="evenodd"
                    />
                  </svg>
                </button>

                <!-- DOCX Export -->
                <button
                  type="button"
                  class="flex w-full items-center justify-between rounded-lg border-2 border-gray-200 p-4 text-left transition-all hover:border-primary-500 hover:bg-primary-50 focus:outline-none focus-visible:ring-2 focus-visible:ring-primary-500"
                  :disabled="exporting"
                  @click="exportFormat('docx')"
                >
                  <div class="flex items-center gap-3">
                    <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-100">
                      <svg
                        class="h-6 w-6 text-blue-600"
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          stroke-width="2"
                          d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                        />
                      </svg>
                    </div>
                    <div>
                      <div class="font-semibold text-gray-900">
                        Word Document
                      </div>
                      <div class="text-sm text-gray-600">
                        Editable format for notes
                      </div>
                    </div>
                  </div>
                  <svg
                    class="h-5 w-5 text-gray-400"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                  >
                    <path
                      fill-rule="evenodd"
                      d="M7.21 14.77a.75.75 0 01.02-1.06L11.168 10 7.23 6.29a.75.75 0 111.04-1.08l4.5 4.25a.75.75 0 010 1.08l-4.5 4.25a.75.75 0 01-1.06-.02z"
                      clip-rule="evenodd"
                    />
                  </svg>
                </button>

                <!-- Lawyer Pack Export (AF-003) -->
                <button
                  type="button"
                  class="flex w-full items-center justify-between rounded-lg border-2 border-purple-200 bg-purple-50 p-4 text-left transition-all hover:border-purple-500 hover:bg-purple-100 focus:outline-none focus-visible:ring-2 focus-visible:ring-purple-500"
                  :disabled="exporting"
                  @click="exportFormat('lawyer-pack')"
                >
                  <div class="flex items-center gap-3">
                    <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-purple-600">
                      <svg
                        class="h-6 w-6 text-white"
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          stroke-width="2"
                          d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
                        />
                      </svg>
                    </div>
                    <div>
                      <div class="font-semibold text-gray-900">
                        Lawyer Handoff Pack
                      </div>
                      <div class="text-sm text-gray-600">
                        Comprehensive report for legal counsel
                      </div>
                    </div>
                  </div>
                  <svg
                    class="h-5 w-5 text-purple-600"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                  >
                    <path
                      fill-rule="evenodd"
                      d="M7.21 14.77a.75.75 0 01.02-1.06L11.168 10 7.23 6.29a.75.75 0 111.04-1.08l4.5 4.25a.75.75 0 010 1.08l-4.5 4.25a.75.75 0 01-1.06-.02z"
                      clip-rule="evenodd"
                    />
                  </svg>
                </button>

                <!-- JSON Export -->
                <button
                  type="button"
                  class="flex w-full items-center justify-between rounded-lg border-2 border-gray-200 p-4 text-left transition-all hover:border-primary-500 hover:bg-primary-50 focus:outline-none focus-visible:ring-2 focus-visible:ring-primary-500"
                  :disabled="exporting"
                  @click="exportFormat('json')"
                >
                  <div class="flex items-center gap-3">
                    <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-green-100">
                      <svg
                        class="h-6 w-6 text-green-600"
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          stroke-width="2"
                          d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"
                        />
                      </svg>
                    </div>
                    <div>
                      <div class="font-semibold text-gray-900">
                        JSON Data
                      </div>
                      <div class="text-sm text-gray-600">
                        Raw data for developers
                      </div>
                    </div>
                  </div>
                  <svg
                    class="h-5 w-5 text-gray-400"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                  >
                    <path
                      fill-rule="evenodd"
                      d="M7.21 14.77a.75.75 0 01.02-1.06L11.168 10 7.23 6.29a.75.75 0 111.04-1.08l4.5 4.25a.75.75 0 010 1.08l-4.5 4.25a.75.75 0 01-1.06-.02z"
                      clip-rule="evenodd"
                    />
                  </svg>
                </button>
              </div>

              <!-- Loading state -->
              <div
                v-if="exporting"
                class="mt-4 flex items-center justify-center gap-2 text-sm text-gray-600"
              >
                <div class="spinner h-4 w-4" />
                <span>Generating export...</span>
              </div>
            </div>

            <!-- Footer -->
            <div class="border-t border-gray-200 bg-gray-50 px-6 py-3">
              <div class="flex justify-end">
                <button
                  type="button"
                  class="btn btn--secondary"
                  :disabled="exporting"
                  @click="close"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Props {
  modelValue: boolean
}

interface Emits {
  (e: 'update:modelValue', value: boolean): void
  (e: 'export', format: 'pdf' | 'docx' | 'json' | 'lawyer-pack'): void
}

defineProps<Props>()
const emit = defineEmits<Emits>()

const exporting = ref(false)

function close(): void {
  if (!exporting.value) {
    emit('update:modelValue', false)
  }
}

async function exportFormat(format: 'pdf' | 'docx' | 'json' | 'lawyer-pack'): Promise<void> {
  exporting.value = true
  try {
    emit('export', format)
    // Keep modal open briefly to show loading state
    await new Promise((resolve) => setTimeout(resolve, 500))
    close()
  } finally {
    exporting.value = false
  }
}
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .modal-container,
.modal-leave-active .modal-container {
  transition: transform 0.3s ease;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
  transform: scale(0.95);
}

.spinner {
  border: 2px solid #e5e7eb;
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
