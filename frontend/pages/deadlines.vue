<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="container-custom max-w-6xl">
      <!-- Header -->
      <div class="mb-8">
        <div class="flex items-start justify-between">
          <div>
            <h1 class="text-3xl font-bold text-gray-900">
              Contract Deadlines
            </h1>
            <p class="mt-2 text-gray-600">
              Track important dates and deadlines from your contracts
            </p>
          </div>

          <button
            v-if="deadlines.length > 0"
            @click="exportAllToCalendar"
            :disabled="exportingAll"
            class="btn btn--secondary"
          >
            <svg
              v-if="!exportingAll"
              class="h-5 w-5 mr-2"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fill-rule="evenodd"
                d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z"
                clip-rule="evenodd"
              />
            </svg>
            <div v-else class="spinner h-5 w-5 mr-2" />
            Export All to Calendar
          </button>
        </div>

        <!-- Filters -->
        <div class="mt-6 grid gap-4 sm:grid-cols-4">
          <!-- Type Filter -->
          <div>
            <label for="type-filter" class="sr-only">Filter by type</label>
            <select
              id="type-filter"
              v-model="typeFilter"
              class="input w-full"
              @change="fetchDeadlines"
            >
              <option value="">All Types</option>
              <option value="payment">💰 Payment</option>
              <option value="renewal">🔄 Renewal</option>
              <option value="notice">📢 Notice</option>
              <option value="termination">⚠️ Termination</option>
              <option value="option_exercise">✅ Option Exercise</option>
              <option value="obligation">📋 Obligation</option>
              <option value="other">📌 Other</option>
            </select>
          </div>

          <!-- Date Range Filter -->
          <div>
            <label for="date-filter" class="sr-only">Filter by date</label>
            <select
              id="date-filter"
              v-model="dateRange"
              class="input w-full"
              @change="fetchDeadlines"
            >
              <option value="upcoming">📅 Upcoming (30 days)</option>
              <option value="all">All Deadlines</option>
              <option value="overdue">⏰ Overdue</option>
            </select>
          </div>

          <!-- Completion Filter -->
          <div>
            <label for="status-filter" class="sr-only">Filter by status</label>
            <select
              id="status-filter"
              v-model="statusFilter"
              class="input w-full"
              @change="fetchDeadlines"
            >
              <option value="active">Active</option>
              <option value="all">All</option>
              <option value="completed">Completed</option>
            </select>
          </div>

          <!-- View Mode Toggle -->
          <div>
            <div class="flex rounded-lg border border-gray-300 bg-white">
              <button
                @click="viewMode = 'list'"
                :class="[
                  'flex-1 px-4 py-2 text-sm font-medium rounded-l-lg transition-colors',
                  viewMode === 'list'
                    ? 'bg-sky-500 text-white'
                    : 'text-gray-700 hover:bg-gray-50'
                ]"
              >
                List
              </button>
              <button
                @click="viewMode = 'calendar'"
                :class="[
                  'flex-1 px-4 py-2 text-sm font-medium rounded-r-lg transition-colors',
                  viewMode === 'calendar'
                    ? 'bg-sky-500 text-white'
                    : 'text-gray-700 hover:bg-gray-50'
                ]"
              >
                Timeline
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div
        v-if="loading && deadlines.length === 0"
        class="flex items-center justify-center py-20"
      >
        <div class="text-center">
          <div class="spinner mx-auto h-12 w-12" aria-hidden="true" />
          <p class="mt-4 text-gray-600">Loading deadlines...</p>
        </div>
      </div>

      <!-- Error State -->
      <div
        v-else-if="error"
        class="bg-white rounded-lg border border-red-200 p-12 text-center"
      >
        <svg
          class="mx-auto h-12 w-12 text-red-400 mb-4"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            fill-rule="evenodd"
            d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.28 7.22a.75.75 0 00-1.06 1.06L8.94 10l-1.72 1.72a.75.75 0 101.06 1.06L10 11.06l1.72 1.72a.75.75 0 101.06-1.06L11.06 10l1.72-1.72a.75.75 0 00-1.06-1.06L10 8.94 8.28 7.22z"
            clip-rule="evenodd"
          />
        </svg>
        <h3 class="text-lg font-semibold text-gray-900 mb-2">
          Failed to load deadlines
        </h3>
        <p class="text-gray-600 mb-4">{{ error }}</p>
        <button @click="fetchDeadlines" class="btn btn--primary">
          Try Again
        </button>
      </div>

      <!-- Empty State -->
      <div
        v-else-if="deadlines.length === 0"
        class="bg-white rounded-lg border border-gray-200 p-12 text-center"
      >
        <svg
          class="mx-auto h-12 w-12 text-gray-400 mb-4"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
          />
        </svg>
        <h3 class="text-lg font-semibold text-gray-900 mb-2">
          No deadlines found
        </h3>
        <p class="text-gray-600 mb-4">
          Deadlines are automatically extracted when you analyze contracts.
        </p>
        <NuxtLink to="/upload" class="btn btn--primary">
          Upload a Contract
        </NuxtLink>
      </div>

      <!-- List View -->
      <div v-else-if="viewMode === 'list'" class="space-y-4">
        <div
          v-for="deadline in deadlines"
          :key="deadline.id"
          class="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-md transition-shadow"
        >
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <!-- Type Badge and Title -->
              <div class="flex items-center gap-3 mb-2">
                <span :class="getTypeBadgeClass(deadline.deadline_type)">
                  {{ getTypeIcon(deadline.deadline_type) }} {{ formatType(deadline.deadline_type) }}
                </span>
                <span
                  v-if="deadline.is_recurring"
                  class="px-2 py-1 text-xs font-medium rounded-full bg-purple-100 text-purple-800"
                >
                  🔁 Recurring
                </span>
                <span
                  v-if="deadline.is_completed"
                  class="px-2 py-1 text-xs font-medium rounded-full bg-green-100 text-green-800"
                >
                  ✓ Completed
                </span>
                <span
                  v-else-if="isOverdue(deadline)"
                  class="px-2 py-1 text-xs font-medium rounded-full bg-red-100 text-red-800"
                >
                  ⚠️ Overdue
                </span>
              </div>

              <h3 class="text-lg font-semibold text-gray-900 mb-2">
                {{ deadline.title }}
              </h3>

              <div v-if="deadline.description" class="text-gray-600 mb-3">
                {{ deadline.description }}
              </div>

              <!-- Date Information -->
              <div class="flex items-center gap-4 text-sm text-gray-600">
                <div v-if="deadline.date" class="flex items-center gap-1">
                  <svg
                    class="h-4 w-4"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                  >
                    <path
                      fill-rule="evenodd"
                      d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z"
                      clip-rule="evenodd"
                    />
                  </svg>
                  <span>{{ formatDate(deadline.date) }}</span>
                  <span
                    v-if="!deadline.is_completed && !isOverdue(deadline)"
                    class="text-sky-600 font-medium"
                  >
                    ({{ getDaysUntil(deadline.date) }})
                  </span>
                </div>
                <div v-else-if="deadline.date_formula" class="flex items-center gap-1">
                  <svg
                    class="h-4 w-4"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                  >
                    <path d="M10 2a8 8 0 100 16 8 8 0 000-16zm1 11H9v-2h2v2zm0-4H9V5h2v4z" />
                  </svg>
                  <span>{{ deadline.date_formula }}</span>
                </div>
              </div>
            </div>

            <!-- Actions -->
            <div class="flex items-center gap-2 ml-4">
              <button
                v-if="deadline.date && !deadline.is_completed"
                @click="exportToCalendar(deadline.id)"
                :disabled="exportingIds.has(deadline.id)"
                class="p-2 text-gray-600 hover:text-sky-600 hover:bg-sky-50 rounded-lg transition-colors"
                title="Export to calendar"
              >
                <svg
                  v-if="!exportingIds.has(deadline.id)"
                  class="h-5 w-5"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fill-rule="evenodd"
                    d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z"
                    clip-rule="evenodd"
                  />
                </svg>

definePageMeta({
  middleware: 'auth',
})
                <div v-else class="spinner h-5 w-5" />
              </button>

              <button
                v-if="!deadline.is_completed"
                @click="markAsComplete(deadline.id)"
                class="p-2 text-gray-600 hover:text-green-600 hover:bg-green-50 rounded-lg transition-colors"
                title="Mark as complete"
              >
                <svg
                  class="h-5 w-5"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fill-rule="evenodd"
                    d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                    clip-rule="evenodd"
                  />
                </svg>
              </button>

              <button
                v-else
                @click="markAsIncomplete(deadline.id)"
                class="p-2 text-green-600 hover:text-gray-600 hover:bg-gray-50 rounded-lg transition-colors"
                title="Mark as incomplete"
              >
                <svg
                  class="h-5 w-5"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fill-rule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                    clip-rule="evenodd"
                  />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Timeline View -->
      <div v-else-if="viewMode === 'calendar'" class="bg-white rounded-lg border border-gray-200 p-6">
        <div class="space-y-8">
          <div
            v-for="(group, dateKey) in groupedByDate"
            :key="dateKey"
            class="relative"
          >
            <!-- Date Header -->
            <div class="flex items-center gap-4 mb-4">
              <div class="flex-shrink-0 w-32">
                <div class="text-sm font-medium text-gray-500">
                  {{ formatDateHeader(dateKey) }}
                </div>
              </div>
              <div class="flex-1 h-px bg-gray-200"></div>
            </div>

            <!-- Timeline Items -->
            <div class="ml-36 space-y-3">
              <div
                v-for="deadline in group"
                :key="deadline.id"
                class="relative pl-6 pb-4 border-l-2"
                :class="deadline.is_completed ? 'border-green-300' : isOverdue(deadline) ? 'border-red-300' : 'border-sky-300'"
              >
                <!-- Timeline Dot -->
                <div
                  class="absolute left-0 top-0 -ml-2 w-4 h-4 rounded-full border-2 bg-white"
                  :class="deadline.is_completed ? 'border-green-500' : isOverdue(deadline) ? 'border-red-500' : 'border-sky-500'"
                ></div>

                <!-- Content -->
                <div class="bg-gray-50 rounded-lg p-4 hover:shadow-md transition-shadow">
                  <div class="flex items-start justify-between">
                    <div class="flex-1">
                      <div class="flex items-center gap-2 mb-2">
                        <span :class="getTypeBadgeClass(deadline.deadline_type)">
                          {{ getTypeIcon(deadline.deadline_type) }} {{ formatType(deadline.deadline_type) }}
                        </span>
                        <span
                          v-if="deadline.is_recurring"
                          class="px-2 py-1 text-xs font-medium rounded-full bg-purple-100 text-purple-800"
                        >
                          🔁
                        </span>
                      </div>
                      <h4 class="font-semibold text-gray-900 mb-1">
                        {{ deadline.title }}
                      </h4>
                      <p v-if="deadline.description" class="text-sm text-gray-600">
                        {{ deadline.description }}
                      </p>
                    </div>

                    <div class="flex items-center gap-2 ml-4">
                      <button
                        v-if="deadline.date && !deadline.is_completed"
                        @click="exportToCalendar(deadline.id)"
                        class="p-1.5 text-gray-600 hover:text-sky-600 hover:bg-sky-50 rounded transition-colors"
                        title="Export to calendar"
                      >
                        <svg class="h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                          <path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd" />
                        </svg>
                      </button>
                      <button
                        v-if="!deadline.is_completed"
                        @click="markAsComplete(deadline.id)"
                        class="p-1.5 text-gray-600 hover:text-green-600 hover:bg-green-50 rounded transition-colors"
                        title="Complete"
                      >
                        <svg class="h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                          <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                        </svg>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRuntimeConfig, useRouter } from '#app'

// Types
interface Deadline {
  id: string
  contract_id: string
  analysis_id: string | null
  deadline_type: string
  title: string
  description: string | null
  date: string | null
  date_formula: string | null
  is_recurring: boolean
  is_completed: boolean
  completed_at: string | null
  source_section: string | null
  created_at: string
}

// State
const config = useRuntimeConfig()
const router = useRouter()

const deadlines = ref<Deadline[]>([])
const loading = ref(true)
const error = ref<string | null>(null)
const typeFilter = ref('')
const dateRange = ref('upcoming')
const statusFilter = ref('active')
const viewMode = ref<'list' | 'calendar'>('list')
const exportingIds = ref(new Set<string>())
const exportingAll = ref(false)

// Computed
const groupedByDate = computed(() => {
  const groups: Record<string, Deadline[]> = {}

  deadlines.value
    .filter(d => d.date)
    .sort((a, b) => {
      const dateA = new Date(a.date!)
      const dateB = new Date(b.date!)
      return dateA.getTime() - dateB.getTime()
    })
    .forEach(deadline => {
      const dateKey = deadline.date!.split('T')[0]
      if (!groups[dateKey]) {
        groups[dateKey] = []
      }
      groups[dateKey].push(deadline)
    })

  return groups
})

// Methods
async function fetchDeadlines() {
  loading.value = true
  error.value = null

  try {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    const params = new URLSearchParams()

    // Type filter
    if (typeFilter.value) {
      params.append('deadline_type', typeFilter.value)
    }

    // Date range filter
    if (dateRange.value === 'upcoming') {
      params.append('upcoming_only', 'true')
      params.append('days_ahead', '30')
    }

    // Status filter
    if (statusFilter.value === 'active') {
      params.append('is_completed', 'false')
    } else if (statusFilter.value === 'completed') {
      params.append('is_completed', 'true')
    }

    const response = await fetch(
      `${config.public.apiBase}/deadlines?${params.toString()}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    if (!response.ok) {
      throw new Error('Failed to fetch deadlines')
    }

    deadlines.value = await response.json()

    // If overdue filter is active, filter client-side
    if (dateRange.value === 'overdue') {
      const now = new Date()
      deadlines.value = deadlines.value.filter(d => {
        if (!d.date || d.is_completed) return false
        return new Date(d.date) < now
      })
    }
  } catch (err: any) {
    error.value = err.message || 'An error occurred'
  } finally {
    loading.value = false
  }
}

async function markAsComplete(deadlineId: string) {
  try {
    const token = localStorage.getItem('token')
    const response = await fetch(
      `${config.public.apiBase}/deadlines/${deadlineId}`,
      {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ is_completed: true }),
      }
    )

    if (!response.ok) {
      throw new Error('Failed to mark as complete')
    }

    // Update local state
    const index = deadlines.value.findIndex(d => d.id === deadlineId)
    if (index !== -1) {
      deadlines.value[index].is_completed = true
      deadlines.value[index].completed_at = new Date().toISOString()
    }
  } catch (err: any) {
    alert(err.message || 'Failed to update deadline')
  }
}

async function markAsIncomplete(deadlineId: string) {
  try {
    const token = localStorage.getItem('token')
    const response = await fetch(
      `${config.public.apiBase}/deadlines/${deadlineId}`,
      {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ is_completed: false }),
      }
    )

    if (!response.ok) {
      throw new Error('Failed to mark as incomplete')
    }

    // Update local state
    const index = deadlines.value.findIndex(d => d.id === deadlineId)
    if (index !== -1) {
      deadlines.value[index].is_completed = false
      deadlines.value[index].completed_at = null
    }
  } catch (err: any) {
    alert(err.message || 'Failed to update deadline')
  }
}

async function exportToCalendar(deadlineId: string) {
  exportingIds.value.add(deadlineId)

  try {
    const token = localStorage.getItem('token')
    const response = await fetch(
      `${config.public.apiBase}/deadlines/${deadlineId}/ics`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    if (!response.ok) {
      throw new Error('Failed to export deadline')
    }

    const blob = await response.blob()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `deadline_${deadlineId}.ics`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    window.URL.revokeObjectURL(url)
  } catch (err: any) {
    alert(err.message || 'Failed to export deadline')
  } finally {
    exportingIds.value.delete(deadlineId)
  }
}

async function exportAllToCalendar() {
  exportingAll.value = true

  try {
    const token = localStorage.getItem('token')
    const response = await fetch(
      `${config.public.apiBase}/deadlines/export/all-ics?upcoming_only=true&days_ahead=90`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    if (!response.ok) {
      throw new Error('Failed to export deadlines')
    }

    const blob = await response.blob()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'contract_deadlines.ics'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    window.URL.revokeObjectURL(url)
  } catch (err: any) {
    alert(err.message || 'Failed to export deadlines')
  } finally {
    exportingAll.value = false
  }
}

function formatDate(dateString: string): string {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    weekday: 'short',
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}

function formatDateHeader(dateString: string): string {
  const date = new Date(dateString)
  const today = new Date()
  const tomorrow = new Date(today)
  tomorrow.setDate(tomorrow.getDate() + 1)

  if (date.toDateString() === today.toDateString()) {
    return 'Today'
  } else if (date.toDateString() === tomorrow.toDateString()) {
    return 'Tomorrow'
  } else {
    return date.toLocaleDateString('en-US', {
      weekday: 'long',
      month: 'long',
      day: 'numeric',
    })
  }
}

function getDaysUntil(dateString: string): string {
  const date = new Date(dateString)
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  date.setHours(0, 0, 0, 0)

  const diffTime = date.getTime() - today.getTime()
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

  if (diffDays === 0) return 'Today'
  if (diffDays === 1) return 'Tomorrow'
  if (diffDays < 0) return `${Math.abs(diffDays)} days ago`
  return `in ${diffDays} days`
}

function isOverdue(deadline: Deadline): boolean {
  if (!deadline.date || deadline.is_completed) return false
  const date = new Date(deadline.date)
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  return date < today
}

function getTypeIcon(type: string): string {
  const icons: Record<string, string> = {
    payment: '💰',
    renewal: '🔄',
    notice: '📢',
    termination: '⚠️',
    option_exercise: '✅',
    obligation: '📋',
    other: '📌',
  }
  return icons[type] || '📌'
}

function formatType(type: string): string {
  return type
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

function getTypeBadgeClass(type: string): string {
  const classes: Record<string, string> = {
    payment: 'px-2 py-1 text-xs font-medium rounded-full bg-green-100 text-green-800',
    renewal: 'px-2 py-1 text-xs font-medium rounded-full bg-blue-100 text-blue-800',
    notice: 'px-2 py-1 text-xs font-medium rounded-full bg-yellow-100 text-yellow-800',
    termination: 'px-2 py-1 text-xs font-medium rounded-full bg-red-100 text-red-800',
    option_exercise: 'px-2 py-1 text-xs font-medium rounded-full bg-purple-100 text-purple-800',
    obligation: 'px-2 py-1 text-xs font-medium rounded-full bg-indigo-100 text-indigo-800',
    other: 'px-2 py-1 text-xs font-medium rounded-full bg-gray-100 text-gray-800',
  }
  return classes[type] || classes.other
}

// Lifecycle
onMounted(() => {
  fetchDeadlines()
})
</script>
