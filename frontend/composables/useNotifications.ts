import { ref } from 'vue'

/**
 * Notification/Toast System
 * Global composable for showing notifications
 */

export type NotificationType = 'success' | 'error' | 'warning' | 'info'

export interface Notification {
  id: string
  type: NotificationType
  title: string
  message?: string
  duration?: number
}

const notifications = ref<Notification[]>([])
let notificationId = 0

export const useNotifications = () => {
  const addNotification = (
    type: NotificationType,
    title: string,
    message?: string,
    duration: number = 5000
  ): string => {
    const id = `notification-${++notificationId}`

    const notification: Notification = {
      id,
      type,
      title,
      message,
      duration,
    }

    notifications.value.push(notification)

    // Auto-remove after duration
    if (duration > 0) {
      setTimeout(() => {
        removeNotification(id)
      }, duration)
    }

    return id
  }

  const removeNotification = (id: string): void => {
    const index = notifications.value.findIndex((n) => n.id === id)
    if (index !== -1) {
      notifications.value.splice(index, 1)
    }
  }

  const clearAll = (): void => {
    notifications.value = []
  }

  // Convenience methods
  const success = (title: string, message?: string, duration?: number): string => {
    return addNotification('success', title, message, duration)
  }

  const error = (title: string, message?: string, duration?: number): string => {
    return addNotification('error', title, message, duration)
  }

  const warning = (title: string, message?: string, duration?: number): string => {
    return addNotification('warning', title, message, duration)
  }

  const info = (title: string, message?: string, duration?: number): string => {
    return addNotification('info', title, message, duration)
  }

  return {
    notifications,
    addNotification,
    removeNotification,
    clearAll,
    success,
    error,
    warning,
    info,
  }
}
