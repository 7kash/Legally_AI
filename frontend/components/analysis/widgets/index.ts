/**
 * Widget Registry
 * Maps backend section keys to their corresponding Vue components
 */

import type { Component } from 'vue'
import SimpleTextWidget from './SimpleTextWidget.vue'
import PartiesWidget from './PartiesWidget.vue'
import PaymentTermsWidget from './PaymentTermsWidget.vue'
import CalendarWidget from './CalendarWidget.vue'
import ObligationsWidget from './ObligationsWidget.vue'
import RightsWidget from './RightsWidget.vue'
import RisksWidget from './RisksWidget.vue'
import MitigationsWidget from './MitigationsWidget.vue'

export interface WidgetConfig {
  component: Component
  icon: string
  color?: 'blue' | 'green' | 'red' | 'purple' | 'amber' | 'emerald'
}

export interface WidgetRegistry {
  [key: string]: WidgetConfig
}

/**
 * Widget registry mapping backend keys to Vue components
 */
export const WIDGET_REGISTRY: WidgetRegistry = {
  agreement_type: {
    component: SimpleTextWidget,
    icon: 'document',
    color: undefined
  },
  parties: {
    component: PartiesWidget,
    icon: 'users',
    color: undefined
  },
  jurisdiction: {
    component: SimpleTextWidget,
    icon: 'globe',
    color: undefined
  },
  obligations: {
    component: ObligationsWidget,
    icon: 'clipboard',
    color: 'blue'
  },
  rights: {
    component: RightsWidget,
    icon: 'shield',
    color: 'green'
  },
  risks: {
    component: RisksWidget,
    icon: 'warning',
    color: 'red'
  },
  payment_terms: {
    component: PaymentTermsWidget,
    icon: 'currency',
    color: 'emerald'
  },
  calendar: {
    component: CalendarWidget,
    icon: 'calendar',
    color: 'purple'
  },
  mitigations: {
    component: MitigationsWidget,
    icon: 'shield-check',
    color: 'amber'
  }
}

/**
 * Get widget configuration for a given section key
 * @param key - Backend section key (e.g., 'obligations', 'rights')
 * @returns Widget configuration or undefined if not found
 */
export function getWidgetConfig(key: string): WidgetConfig | undefined {
  return WIDGET_REGISTRY[key]
}

/**
 * Check if content exists and is not empty
 * @param section - Section data from backend
 * @returns true if section has displayable content
 */
export function hasContent(section: any): boolean {
  if (!section) return false

  const content = section.content !== undefined ? section.content : section

  if (Array.isArray(content)) {
    return content.length > 0
  }

  if (typeof content === 'object' && content !== null) {
    return Object.keys(content).length > 0
  }

  if (typeof content === 'string') {
    return content.trim().length > 0
  }

  return false
}
