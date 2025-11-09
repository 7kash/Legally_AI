<template>
  <div class="relative">
    <button
      type="button"
      class="flex items-center gap-2 rounded-lg px-3 py-2 text-sm font-medium text-gray-700 transition-colors hover:bg-gray-100 focus:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 dark:text-gray-300 dark:hover:bg-gray-800"
      aria-label="Change language"
      :aria-expanded="isOpen"
      aria-haspopup="true"
      @click="toggleMenu"
    >
      <svg
        class="h-5 w-5"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 20 20"
        fill="currentColor"
        aria-hidden="true"
      >
        <path
          fill-rule="evenodd"
          d="M7 2a1 1 0 011 1v1h3a1 1 0 110 2H9.578a18.87 18.87 0 01-1.724 4.78c.29.354.596.696.914 1.026a1 1 0 11-1.44 1.389c-.188-.196-.373-.396-.554-.6a19.098 19.098 0 01-3.107 3.567 1 1 0 01-1.334-1.49 17.087 17.087 0 003.13-3.733 18.992 18.992 0 01-1.487-2.494 1 1 0 111.79-.89c.234.47.489.928.764 1.372.417-.934.752-1.913.997-2.927H3a1 1 0 110-2h3V3a1 1 0 011-1zm6 6a1 1 0 01.894.553l2.991 5.982a.869.869 0 01.02.037l.99 1.98a1 1 0 11-1.79.895L15.383 16h-4.764l-.724 1.447a1 1 0 11-1.788-.894l.99-1.98.019-.038 2.99-5.982A1 1 0 0113 8zm-1.382 6h2.764L13 11.236 11.618 14z"
          clip-rule="evenodd"
        />
      </svg>
      <span>{{ currentLanguageLabel }}</span>
      <svg
        class="h-4 w-4"
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

    <!-- Dropdown -->
    <Transition name="dropdown">
      <div
        v-if="isOpen"
        class="absolute right-0 mt-2 w-48 origin-top-right rounded-lg border border-gray-200 bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none dark:border-gray-700 dark:bg-gray-800"
        role="menu"
        aria-orientation="vertical"
      >
        <div class="py-1">
          <button
            v-for="lang in availableLanguages"
            :key="lang.code"
            type="button"
            class="flex w-full items-center gap-3 px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700"
            :class="{ 'bg-gray-50 dark:bg-gray-700': lang.code === currentLocale }"
            role="menuitem"
            @click="changeLanguage(lang.code)"
          >
            <span class="text-lg">{{ lang.flag }}</span>
            <span>{{ lang.name }}</span>
            <svg
              v-if="lang.code === currentLocale"
              class="ml-auto h-5 w-5 text-primary-600"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 20 20"
              fill="currentColor"
              aria-hidden="true"
            >
              <path
                fill-rule="evenodd"
                d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                clip-rule="evenodd"
              />
            </svg>
          </button>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

/**
 * Language Switcher Component
 * Allows users to change the UI language
 */

const { locale } = useI18n()
const isOpen = ref(false)

const availableLanguages = [
  { code: 'en', name: 'English', flag: '🇬🇧' },
  { code: 'ru', name: 'Русский', flag: '🇷🇺' },
  { code: 'fr', name: 'Français', flag: '🇫🇷' },
  { code: 'sr', name: 'Српски', flag: '🇷🇸' },
]

const currentLocale = computed(() => locale.value)

const currentLanguageLabel = computed(() => {
  const lang = availableLanguages.find((l) => l.code === currentLocale.value)
  return lang ? `${lang.flag} ${lang.name}` : 'Language'
})

function toggleMenu() {
  isOpen.value = !isOpen.value
}

function changeLanguage(code: string) {
  locale.value = code
  isOpen.value = false
}

// Close menu when clicking outside
if (import.meta.client) {
  document.addEventListener('click', (event) => {
    const target = event.target as HTMLElement
    if (!target.closest('[aria-haspopup="true"]')) {
      isOpen.value = false
    }
  })
}
</script>

<style lang="scss" scoped>
// Dropdown transition
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s ease;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: scale(0.95);
}
</style>
