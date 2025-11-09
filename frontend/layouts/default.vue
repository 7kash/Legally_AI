<template>
  <div class="layout-default flex min-h-screen flex-col">
    <!-- Main Navigation Header -->
    <header role="banner" class="sticky top-0 z-40 border-b border-gray-200 bg-white shadow-sm">
      <nav
        role="navigation"
        aria-label="Main navigation"
        class="container-custom flex h-16 items-center justify-between"
      >
        <!-- Logo -->
        <NuxtLink
          to="/"
          class="flex items-center gap-2 text-xl font-bold text-primary-600 transition-colors hover:text-primary-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2"
        >
          <!-- Logo SVG would go here -->
          <span>Legally AI</span>
        </NuxtLink>

        <!-- Desktop Navigation -->
        <div class="hidden items-center gap-6 md:flex">
          <NuxtLink
            v-if="isAuthenticated"
            to="/upload"
            class="nav-link"
          >
            Upload Contract
          </NuxtLink>
          <NuxtLink
            v-if="isAuthenticated"
            to="/history"
            class="nav-link"
          >
            History
          </NuxtLink>
          <NuxtLink
            v-if="isAuthenticated"
            to="/account"
            class="nav-link"
          >
            Account
          </NuxtLink>

          <!-- Auth buttons -->
          <div v-if="!isAuthenticated" class="flex items-center gap-3">
            <NuxtLink
              to="/login"
              class="btn btn--secondary"
            >
              Login
            </NuxtLink>
            <NuxtLink
              to="/register"
              class="btn btn--primary"
            >
              Get Started
            </NuxtLink>
          </div>

          <!-- User menu -->
          <div v-else class="relative">
            <button
              type="button"
              class="flex items-center gap-2 rounded-lg px-3 py-2 text-sm font-medium text-gray-700 transition-colors hover:bg-gray-100 focus:outline-none focus-visible:ring-2 focus-visible:ring-primary-500"
              aria-haspopup="true"
              :aria-expanded="isUserMenuOpen"
              @click="toggleUserMenu"
            >
              <span class="sr-only">Open user menu</span>
              <div class="flex h-8 w-8 items-center justify-center rounded-full bg-primary-100 text-primary-700">
                {{ userInitials }}
              </div>
              <svg
                class="h-5 w-5"
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

            <!-- Dropdown menu -->
            <Transition name="dropdown">
              <div
                v-if="isUserMenuOpen"
                class="absolute right-0 mt-2 w-48 origin-top-right rounded-lg border border-gray-200 bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
                role="menu"
                aria-orientation="vertical"
              >
                <div class="py-1">
                  <button
                    type="button"
                    class="block w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-100"
                    role="menuitem"
                    @click="handleLogout"
                  >
                    Logout
                  </button>
                </div>
              </div>
            </Transition>
          </div>
        </div>

        <!-- Mobile menu button -->
        <button
          type="button"
          class="md:hidden rounded-lg p-2 text-gray-600 hover:bg-gray-100 focus:outline-none focus-visible:ring-2 focus-visible:ring-primary-500"
          aria-label="Toggle mobile menu"
          :aria-expanded="isMobileMenuOpen"
          @click="toggleMobileMenu"
        >
          <svg
            class="h-6 w-6"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            aria-hidden="true"
          >
            <path
              v-if="!isMobileMenuOpen"
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M4 6h16M4 12h16M4 18h16"
            />
            <path
              v-else
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </nav>

      <!-- Mobile Navigation -->
      <Transition name="slide-down">
        <nav
          v-if="isMobileMenuOpen"
          class="border-t border-gray-200 bg-white md:hidden"
          role="navigation"
          aria-label="Mobile navigation"
        >
          <div class="container-custom space-y-1 py-3">
            <NuxtLink
              v-if="isAuthenticated"
              to="/upload"
              class="block rounded-lg px-3 py-2 text-base font-medium text-gray-700 hover:bg-gray-100"
              @click="closeMobileMenu"
            >
              Upload Contract
            </NuxtLink>
            <NuxtLink
              v-if="isAuthenticated"
              to="/history"
              class="block rounded-lg px-3 py-2 text-base font-medium text-gray-700 hover:bg-gray-100"
              @click="closeMobileMenu"
            >
              History
            </NuxtLink>
            <NuxtLink
              v-if="isAuthenticated"
              to="/account"
              class="block rounded-lg px-3 py-2 text-base font-medium text-gray-700 hover:bg-gray-100"
              @click="closeMobileMenu"
            >
              Account
            </NuxtLink>

            <div v-if="!isAuthenticated" class="flex flex-col gap-2 pt-2">
              <NuxtLink
                to="/login"
                class="btn btn--secondary"
                @click="closeMobileMenu"
              >
                Login
              </NuxtLink>
              <NuxtLink
                to="/register"
                class="btn btn--primary"
                @click="closeMobileMenu"
              >
                Get Started
              </NuxtLink>
            </div>

            <div v-else class="border-t border-gray-200 pt-2">
              <button
                type="button"
                class="block w-full rounded-lg px-3 py-2 text-left text-base font-medium text-gray-700 hover:bg-gray-100"
                @click="handleLogout"
              >
                Logout
              </button>
            </div>
          </div>
        </nav>
      </Transition>
    </header>

    <!-- Main Content Area -->
    <main id="main-content" role="main" class="flex-1" tabindex="-1">
      <slot />
    </main>

    <!-- Footer -->
    <footer role="contentinfo" class="border-t border-gray-200 bg-gray-50">
      <div class="container-custom py-8">
        <div class="grid gap-8 md:grid-cols-3">
          <!-- Company info -->
          <div>
            <h2 class="text-lg font-semibold text-gray-900">Legally AI</h2>
            <p class="mt-2 text-sm text-gray-600">
              AI-powered contract analysis to help you understand legal documents.
            </p>
          </div>

          <!-- Links -->
          <div>
            <h3 class="text-sm font-semibold text-gray-900">Resources</h3>
            <ul class="mt-2 space-y-2">
              <li>
                <a href="#" class="text-sm text-gray-600 hover:text-primary-600">
                  Documentation
                </a>
              </li>
              <li>
                <a href="#" class="text-sm text-gray-600 hover:text-primary-600">
                  API Reference
                </a>
              </li>
              <li>
                <a href="#" class="text-sm text-gray-600 hover:text-primary-600">
                  Support
                </a>
              </li>
            </ul>
          </div>

          <!-- Legal -->
          <div>
            <h3 class="text-sm font-semibold text-gray-900">Legal</h3>
            <ul class="mt-2 space-y-2">
              <li>
                <a href="#" class="text-sm text-gray-600 hover:text-primary-600">
                  Privacy Policy
                </a>
              </li>
              <li>
                <a href="#" class="text-sm text-gray-600 hover:text-primary-600">
                  Terms of Service
                </a>
              </li>
            </ul>
          </div>
        </div>

        <div class="mt-8 border-t border-gray-200 pt-6 text-center text-sm text-gray-600">
          &copy; {{ currentYear }} Legally AI. All rights reserved.
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '~/stores/auth'

/**
 * Default Layout Component
 * Provides main navigation, header, footer, and responsive mobile menu
 * WCAG 2.1 AA compliant with proper ARIA labels and keyboard navigation
 */

const router = useRouter()
const authStore = useAuthStore()

// State
const isUserMenuOpen = ref(false)
const isMobileMenuOpen = ref(false)

// Computed
const currentYear = computed(() => new Date().getFullYear())
const isAuthenticated = computed(() => authStore.isAuthenticated)
const userInitials = computed(() => {
  const email = authStore.user?.email
  return email ? email.charAt(0).toUpperCase() : 'U'
})

// Methods
const toggleUserMenu = () => {
  isUserMenuOpen.value = !isUserMenuOpen.value
}

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false
}

const handleLogout = async () => {
  try {
    await authStore.logout()
    isUserMenuOpen.value = false
    isMobileMenuOpen.value = false
    await router.push('/login')
  } catch (error) {
    console.error('Logout error:', error)
  }
}

// Close dropdowns when clicking outside
if (import.meta.client) {
  document.addEventListener('click', (event) => {
    const target = event.target as HTMLElement
    if (!target.closest('[aria-haspopup="true"]')) {
      isUserMenuOpen.value = false
    }
  })
}
</script>

<style lang="scss" scoped>
.nav-link {
  @apply text-gray-700 font-medium transition-colors hover:text-primary-600 focus:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 rounded-lg px-3 py-2;
}

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
