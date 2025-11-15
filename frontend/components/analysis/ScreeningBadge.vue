<template>
  <div
    class="rounded-lg border-2 p-6"
    :class="badgeStyles[variant].container"
    role="status"
    aria-live="polite"
  >
    <div class="flex items-start gap-4">
      <!-- Icon -->
      <div
        class="flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-full"
        :class="badgeStyles[variant].iconBg"
      >
        <component :is="badgeStyles[variant].icon" class="h-6 w-6" :class="badgeStyles[variant].iconColor" />
      </div>

      <!-- Content -->
      <div class="flex-1">
        <h3 class="mb-2 text-lg font-semibold" :class="badgeStyles[variant].titleColor">
          {{ badgeStyles[variant].title }}
        </h3>
        <p class="text-sm" :class="badgeStyles[variant].textColor">
          {{ badgeStyles[variant].message }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { h } from 'vue'

interface Props {
  variant: 'no_major_issues' | 'recommended_to_address' | 'high_risk' | 'preliminary_review'
}

defineProps<Props>()

const badgeStyles = {
  no_major_issues: {
    container: 'border-green-300 bg-green-50',
    iconBg: 'bg-green-100',
    iconColor: 'text-green-600',
    titleColor: 'text-green-900',
    textColor: 'text-green-800',
    title: 'No Major Issues Detected',
    message:
      'Based only on what you shared, we didn\'t see major red flags. That doesn\'t mean the agreement is risk-free — just that no glaring issues jumped out. Always review any contract yourself or with legal counsel before signing.',
    icon: () =>
      h(
        'svg',
        {
          xmlns: 'http://www.w3.org/2000/svg',
          viewBox: '0 0 20 20',
          fill: 'currentColor',
        },
        [
          h('path', {
            'fill-rule': 'evenodd',
            d: 'M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z',
            'clip-rule': 'evenodd',
          }),
        ]
      ),
  },
  recommended_to_address: {
    container: 'border-yellow-300 bg-yellow-50',
    iconBg: 'bg-yellow-100',
    iconColor: 'text-yellow-600',
    titleColor: 'text-yellow-900',
    textColor: 'text-yellow-800',
    title: 'Recommended to Address Flagged Items',
    message:
      'The draft can work if the listed issues are fixed or clarified. We recommend raising these points before you commit. If you can\'t negotiate changes, at least understand the risks you\'re accepting.',
    icon: () =>
      h(
        'svg',
        {
          xmlns: 'http://www.w3.org/2000/svg',
          viewBox: '0 0 20 20',
          fill: 'currentColor',
        },
        [
          h('path', {
            'fill-rule': 'evenodd',
            d: 'M8.485 2.495c.673-1.167 2.357-1.167 3.03 0l6.28 10.875c.673 1.167-.17 2.625-1.516 2.625H3.72c-1.347 0-2.189-1.458-1.515-2.625L8.485 2.495zM10 5a.75.75 0 01.75.75v3.5a.75.75 0 01-1.5 0v-3.5A.75.75 0 0110 5zm0 9a1 1 0 100-2 1 1 0 000 2z',
            'clip-rule': 'evenodd',
          }),
        ]
      ),
  },
  high_risk: {
    container: 'border-red-300 bg-red-50',
    iconBg: 'bg-red-100',
    iconColor: 'text-red-600',
    titleColor: 'text-red-900',
    textColor: 'text-red-800',
    title: 'High Risk — Do Not Proceed Without Legal Review',
    message:
      'As written, some provisions may be unlawful, unenforceable, or heavily one-sided. Signing could expose you to significant legal or financial risk. We strongly recommend a qualified lawyer review this before you commit.',
    icon: () =>
      h(
        'svg',
        {
          xmlns: 'http://www.w3.org/2000/svg',
          viewBox: '0 0 20 20',
          fill: 'currentColor',
        },
        [
          h('path', {
            'fill-rule': 'evenodd',
            d: 'M10 18a8 8 0 100-16 8 8 0 000 16zM8.28 7.22a.75.75 0 00-1.06 1.06L8.94 10l-1.72 1.72a.75.75 0 101.06 1.06L10 11.06l1.72 1.72a.75.75 0 101.06-1.06L11.06 10l1.72-1.72a.75.75 0 00-1.06-1.06L10 8.94 8.28 7.22z',
            'clip-rule': 'evenodd',
          }),
        ]
      ),
  },
  preliminary_review: {
    container: 'border-gray-300 bg-gray-50',
    iconBg: 'bg-gray-100',
    iconColor: 'text-gray-600',
    titleColor: 'text-gray-900',
    textColor: 'text-gray-700',
    title: 'Preliminary Review (Low Confidence)',
    message:
      'We can\'t reliably assess this draft due to poor scan quality, missing pages, or other issues. Consider uploading a clearer version or getting a manual legal review.',
    icon: () =>
      h(
        'svg',
        {
          xmlns: 'http://www.w3.org/2000/svg',
          viewBox: '0 0 20 20',
          fill: 'currentColor',
        },
        [
          h('path', {
            'fill-rule': 'evenodd',
            d: 'M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a.75.75 0 000 1.5h.253a.25.25 0 01.244.304l-.459 2.066A1.75 1.75 0 0010.747 15H11a.75.75 0 000-1.5h-.253a.25.25 0 01-.244-.304l.459-2.066A1.75 1.75 0 009.253 9H9z',
            'clip-rule': 'evenodd',
          }),
        ]
      ),
  },
}
</script>
