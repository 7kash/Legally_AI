<template>
  <Teleport to="body">
    <div
      class="notification-container fixed right-4 top-4 z-50 space-y-2"
      role="region"
      aria-live="polite"
      aria-atomic="true"
    >
      <TransitionGroup name="notification">
        <div
          v-for="notification in notifications"
          :key="notification.id"
          class="notification"
          :class="`notification--${notification.type}`"
          role="alert"
        >
          <div class="flex items-start gap-3">
            <!-- Icon -->
            <div class="flex-shrink-0">
              <!-- Success Icon -->
              <svg
                v-if="notification.type === 'success'"
                class="h-5 w-5"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fill-rule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z"
                  clip-rule="evenodd"
                />
              </svg>

              <!-- Error Icon -->
              <svg
                v-else-if="notification.type === 'error'"
                class="h-5 w-5"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fill-rule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.28 7.22a.75.75 0 00-1.06 1.06L8.94 10l-1.72 1.72a.75.75 0 101.06 1.06L10 11.06l1.72 1.72a.75.75 0 101.06-1.06L11.06 10l1.72-1.72a.75.75 0 00-1.06-1.06L10 8.94 8.28 7.22z"
                  clip-rule="evenodd"
                />
              </svg>

              <!-- Warning Icon -->
              <svg
                v-else-if="notification.type === 'warning'"
                class="h-5 w-5"
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

              <!-- Info Icon -->
              <svg
                v-else
                class="h-5 w-5"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fill-rule="evenodd"
                  d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a.75.75 0 000 1.5h.253a.25.25 0 01.244.304l-.459 2.066A1.75 1.75 0 0010.747 15H11a.75.75 0 000-1.5h-.253a.25.25 0 01-.244-.304l.459-2.066A1.75 1.75 0 009.253 9H9z"
                  clip-rule="evenodd"
                />
              </svg>
            </div>

            <!-- Content -->
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium">
                {{ notification.title }}
              </p>
              <p v-if="notification.message" class="mt-1 text-sm opacity-90">
                {{ notification.message }}
              </p>
            </div>

            <!-- Close button -->
            <button
              type="button"
              class="flex-shrink-0 rounded-lg p-1 hover:bg-black hover:bg-opacity-10 focus:outline-none focus-visible:ring-2 focus-visible:ring-white"
              :aria-label="`Dismiss notification: ${notification.title}`"
              @click="removeNotification(notification.id)"
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
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
/**
 * NotificationContainer Component
 * Displays toast notifications
 */

const { notifications, removeNotification } = useNotifications()
</script>

<style lang="scss" scoped>
.notification {
  @apply max-w-sm rounded-lg border p-4 shadow-lg backdrop-blur-sm;
  min-width: 300px;

  &--success {
    @apply border-green-200 bg-green-50 text-green-900;
  }

  &--error {
    @apply border-red-200 bg-red-50 text-red-900;
  }

  &--warning {
    @apply border-yellow-200 bg-yellow-50 text-yellow-900;
  }

  &--info {
    @apply border-blue-200 bg-blue-50 text-blue-900;
  }
}

// Notification transitions
.notification-enter-active,
.notification-leave-active {
  transition: all 0.3s ease;
}

.notification-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.notification-leave-to {
  opacity: 0;
  transform: translateY(-1rem);
}

.notification-move {
  transition: transform 0.3s ease;
}
</style>
