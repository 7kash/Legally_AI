import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useAuthStore } from './auth'

/**
 * Contracts Store
 * Manages contract uploads and contract list
 */

export interface Contract {
  id: string
  user_id: string
  filename: string
  file_size: number
  file_path: string
  mime_type: string
  extracted_text: string | null
  page_count: number | null
  detected_language: string | null
  jurisdiction: string | null
  uploaded_at: string
  updated_at: string
  latest_analysis_id: string | null
  latest_analysis_date: string | null
}

export interface ContractListResponse {
  contracts: Contract[]
  total: number
  page: number
  page_size: number
}

export interface UploadResponse {
  contract_id: string
  filename: string
  status: string
}

export const useContractsStore = defineStore('contracts', () => {
  // State
  const contracts = ref<Contract[]>([])
  const currentContract = ref<Contract | null>(null)
  const loading = ref(false)
  const uploading = ref(false)
  const error = ref<string | null>(null)
  const uploadProgress = ref(0)
  const total = ref(0)
  const currentPage = ref(1)
  const perPage = ref(10)

  // Computed
  const hasContracts = computed(() => contracts.value.length > 0)
  const totalPages = computed(() => Math.ceil(total.value / perPage.value))

  // Actions
  async function uploadContract(file: File): Promise<string> {
    uploading.value = true
    uploadProgress.value = 0
    error.value = null

    try {
      // Validate file
      const validationError = validateFile(file)
      if (validationError) {
        throw new Error(validationError)
      }

      // Prepare form data
      const formData = new FormData()
      formData.append('file', file)

      // Get auth token
      const { token } = useAuthStore()
      if (!token) {
        throw new Error('Not authenticated')
      }

      // Upload file
      const response = await $fetch<UploadResponse>('/contracts/upload', {
        method: 'POST',
        body: formData,
        baseURL: useRuntimeConfig().public.apiBase,
        headers: {
          Authorization: `Bearer ${token}`,
        },
        onUploadProgress: (progressEvent) => {
          if (progressEvent.total) {
            uploadProgress.value = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total
            )
          }
        },
      })

      // Fetch the updated contract to get full details
      await fetchContract(response.contract_id)

      return response.contract_id
    } catch (err: any) {
      error.value = err.message || err.data?.detail || 'Upload failed'
      throw err
    } finally {
      uploading.value = false
      uploadProgress.value = 0
    }
  }

  async function fetchContracts(page: number = 1): Promise<void> {
    loading.value = true
    error.value = null

    try {
      const { token } = useAuthStore()
      if (!token) {
        throw new Error('Not authenticated')
      }

      const response = await $fetch<ContractListResponse>('/contracts', {
        method: 'GET',
        baseURL: useRuntimeConfig().public.apiBase,
        headers: {
          Authorization: `Bearer ${token}`,
        },
        query: {
          page,
          page_size: perPage.value,
        },
      })

      contracts.value = response.contracts || []
      total.value = response.total || 0
      currentPage.value = response.page || page
      error.value = null // Clear any previous errors on success
    } catch (err: any) {
      console.error('Failed to fetch contracts:', err)
      // Set error message but don't show error state for empty results
      // If it's actually a server error, we'll show it, but if user just has no contracts, show empty state
      error.value = err.data?.detail || err.message || 'Failed to fetch contracts'

      // Initialize with empty values on error
      contracts.value = []
      total.value = 0
      currentPage.value = 1

      // Don't throw - let the component handle the error state
      // This prevents showing error when user simply has no contracts
    } finally {
      loading.value = false
    }
  }

  async function fetchContract(contractId: string): Promise<void> {
    loading.value = true
    error.value = null

    try {
      const { token } = useAuthStore()
      if (!token) {
        throw new Error('Not authenticated')
      }

      const response = await $fetch<Contract>(`/contracts/${contractId}`, {
        method: 'GET',
        baseURL: useRuntimeConfig().public.apiBase,
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      currentContract.value = response

      // Also update in contracts list if it exists
      const index = contracts.value.findIndex((c) => c.id === contractId)
      if (index !== -1) {
        contracts.value[index] = response
      }
    } catch (err: any) {
      error.value = err.data?.detail || 'Failed to fetch contract'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteContract(contractId: string): Promise<void> {
    loading.value = true
    error.value = null

    try {
      const { token } = useAuthStore()
      if (!token) {
        throw new Error('Not authenticated')
      }

      await $fetch(`/contracts/${contractId}`, {
        method: 'DELETE',
        baseURL: useRuntimeConfig().public.apiBase,
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      // Remove from local state
      contracts.value = contracts.value.filter((c) => c.id !== contractId)
      if (currentContract.value?.id === contractId) {
        currentContract.value = null
      }
      total.value -= 1
    } catch (err: any) {
      error.value = err.data?.detail || 'Failed to delete contract'
      throw err
    } finally {
      loading.value = false
    }
  }

  function validateFile(file: File): string | null {
    // Check file type
    const allowedTypes = [
      'application/pdf',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    ]
    if (!allowedTypes.includes(file.type)) {
      return 'Invalid file type. Please upload a PDF or DOCX file.'
    }

    // Check file size (10MB limit)
    const maxSize = 10 * 1024 * 1024 // 10MB in bytes
    if (file.size > maxSize) {
      return 'File size exceeds 10MB limit.'
    }

    return null
  }

  function clearError(): void {
    error.value = null
  }

  function clearCurrentContract(): void {
    currentContract.value = null
  }

  return {
    // State
    contracts,
    currentContract,
    loading,
    uploading,
    error,
    uploadProgress,
    total,
    currentPage,
    perPage,
    // Computed
    hasContracts,
    totalPages,
    // Actions
    uploadContract,
    fetchContracts,
    fetchContract,
    deleteContract,
    validateFile,
    clearError,
    clearCurrentContract,
  }
})
