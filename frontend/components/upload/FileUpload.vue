<template>
  <div class="file-upload">
    <!-- Drop zone -->
    <div
      class="file-upload__dropzone"
      :class="{
        'file-upload__dropzone--active': isDragging,
        'file-upload__dropzone--error': hasError,
      }"
      @drop.prevent="handleDrop"
      @dragover.prevent="isDragging = true"
      @dragleave.prevent="isDragging = false"
      @dragenter.prevent="isDragging = true"
    >
      <input
        id="file-input"
        ref="fileInput"
        type="file"
        accept=".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        class="sr-only"
        :aria-describedby="hasError ? 'file-error' : 'file-description'"
        :aria-invalid="hasError"
        @change="handleFileChange"
      >

      <!-- Upload icon and text -->
      <div v-if="!selectedFile" class="text-center">
        <svg
          class="mx-auto h-12 w-12 text-gray-400"
          stroke="currentColor"
          fill="none"
          viewBox="0 0 48 48"
          aria-hidden="true"
        >
          <path
            d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>

        <div class="mt-4">
          <label
            for="file-input"
            class="cursor-pointer rounded-md font-medium text-primary-600 hover:text-primary-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-primary-500 focus-within:ring-offset-2"
          >
            <span>Upload a file</span>
          </label>
          <p class="pl-1 inline text-gray-500">or drag and drop</p>
        </div>
        <p
          id="file-description"
          class="mt-2 text-xs text-gray-500"
        >
          PDF or DOCX up to 10MB
        </p>
      </div>

      <!-- Selected file preview -->
      <div v-else class="flex items-center justify-between">
        <div class="flex items-center gap-3">
          <!-- File icon -->
          <div
            class="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-lg bg-primary-100"
            aria-hidden="true"
          >
            <svg
              class="h-6 w-6 text-primary-600"
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

          <!-- File info -->
          <div class="flex-1 min-w-0">
            <p class="text-sm font-medium text-gray-900 truncate">
              {{ selectedFile.name }}
            </p>
            <p class="text-sm text-gray-500">
              {{ formatFileSize(selectedFile.size) }}
            </p>
          </div>
        </div>

        <!-- Remove button -->
        <button
          type="button"
          class="ml-4 flex-shrink-0 rounded-lg p-2 text-gray-400 hover:bg-gray-100 hover:text-gray-500 focus:outline-none focus-visible:ring-2 focus-visible:ring-primary-500"
          aria-label="Remove file"
          @click="removeFile"
        >
          <svg
            class="h-5 w-5"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 20 20"
            fill="currentColor"
            aria-hidden="true"
          >
            <path
              d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z"
            />
          </svg>
        </button>
      </div>
    </div>

    <!-- Error message -->
    <p
      v-if="errorMessage"
      id="file-error"
      class="mt-2 text-sm text-red-600"
      role="alert"
    >
      {{ errorMessage }}
    </p>

    <!-- Upload button -->
    <div v-if="selectedFile && !hideUploadButton" class="mt-4">
      <button
        type="button"
        class="btn btn--primary w-full"
        :disabled="uploading"
        :aria-busy="uploading"
        @click="handleUpload"
      >
        <span v-if="!uploading">Upload and Analyze</span>
        <span
          v-else
          class="flex items-center justify-center gap-2"
        >
          <span class="spinner" aria-hidden="true" />
          <span>Uploading... {{ uploadProgress }}%</span>
        </span>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

/**
 * FileUpload Component
 * Drag-and-drop file upload with validation
 * WCAG 2.1 AA compliant
 */

interface Props {
  uploading?: boolean
  uploadProgress?: number
  hideUploadButton?: boolean
}

interface Emits {
  (e: 'file-selected', file: File): void
  (e: 'upload', file: File): void
  (e: 'error', error: string): void
}

const props = withDefaults(defineProps<Props>(), {
  uploading: false,
  uploadProgress: 0,
  hideUploadButton: false,
})

const emit = defineEmits<Emits>()

// State
const fileInput = ref<HTMLInputElement | null>(null)
const selectedFile = ref<File | null>(null)
const isDragging = ref(false)
const errorMessage = ref<string | null>(null)

// Computed
const hasError = computed(() => !!errorMessage.value)

// Methods
function handleFileChange(event: Event): void {
  const target = event.target as HTMLInputElement
  const files = target.files

  if (files && files.length > 0) {
    selectFile(files[0])
  }
}

function handleDrop(event: DragEvent): void {
  isDragging.value = false

  const files = event.dataTransfer?.files
  if (files && files.length > 0) {
    selectFile(files[0])
  }
}

function selectFile(file: File): void {
  errorMessage.value = null

  // Validate file type
  const allowedTypes = [
    'application/pdf',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  ]

  if (!allowedTypes.includes(file.type)) {
    const error = 'Invalid file type. Please upload a PDF or DOCX file.'
    errorMessage.value = error
    emit('error', error)
    return
  }

  // Validate file size (10MB)
  const maxSize = 10 * 1024 * 1024
  if (file.size > maxSize) {
    const error = 'File size exceeds 10MB limit.'
    errorMessage.value = error
    emit('error', error)
    return
  }

  selectedFile.value = file
  emit('file-selected', file)
}

function removeFile(): void {
  selectedFile.value = null
  errorMessage.value = null

  // Reset file input
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

function handleUpload(): void {
  if (selectedFile.value) {
    emit('upload', selectedFile.value)
  }
}

function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Bytes'

  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))

  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}

// Expose methods for parent component
defineExpose({
  removeFile,
})
</script>

<style lang="scss" scoped>
.file-upload {
  &__dropzone {
    @apply relative border-2 border-dashed border-gray-300 rounded-lg p-8 transition-colors;

    &:hover {
      @apply border-gray-400 bg-gray-50;
    }

    &--active {
      @apply border-primary-500 bg-primary-50;
    }

    &--error {
      @apply border-red-300 bg-red-50;
    }
  }
}
</style>
