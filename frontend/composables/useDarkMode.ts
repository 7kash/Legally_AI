import { ref, watch, onMounted } from 'vue'
import { useColorMode } from '@vueuse/core'

/**
 * Dark Mode Composable
 * Manages dark mode state with localStorage persistence
 */

export const useDarkMode = () => {
  // Use VueUse's color mode with localStorage persistence
  const colorMode = useColorMode({
    attribute: 'data-theme',
    modes: {
      light: 'light',
      dark: 'dark',
    },
    storageKey: 'legally-ai-theme',
  })

  const isDark = ref(colorMode.value === 'dark')

  // Watch for changes
  watch(colorMode, (newMode) => {
    isDark.value = newMode === 'dark'
  })

  // Toggle function
  const toggle = () => {
    colorMode.value = isDark.value ? 'light' : 'dark'
  }

  // Set specific mode
  const setDark = () => {
    colorMode.value = 'dark'
  }

  const setLight = () => {
    colorMode.value = 'light'
  }

  return {
    isDark,
    colorMode,
    toggle,
    setDark,
    setLight,
  }
}
