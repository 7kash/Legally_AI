<template>
  <div class="min-h-screen bg-gray-50 py-12">
    <div class="container-custom max-w-4xl">
      <!-- Header -->
      <div class="mb-8 text-center">
        <h1 class="text-4xl font-bold text-gray-900 mb-4">
          Support Center
        </h1>
        <p class="text-lg text-gray-600">
          We're here to help! Get answers to your questions or contact our team.
        </p>
      </div>

      <!-- Content -->
      <div class="space-y-8">
        <!-- Quick Help -->
        <section class="bg-white rounded-lg border border-gray-200 p-6">
          <h2 class="text-2xl font-semibold text-gray-900 mb-4">
            Quick Help
          </h2>
          <div class="grid gap-4 md:grid-cols-3">
            <NuxtLink to="/documentation" class="p-4 border border-gray-200 rounded-lg hover:border-primary-500 transition-colors">
              <div class="text-3xl mb-2">📚</div>
              <h3 class="font-semibold text-gray-900 mb-1">Documentation</h3>
              <p class="text-sm text-gray-600">
                Learn how to use Legally AI
              </p>
            </NuxtLink>
            <NuxtLink to="/api-reference" class="p-4 border border-gray-200 rounded-lg hover:border-primary-500 transition-colors">
              <div class="text-3xl mb-2">⚙️</div>
              <h3 class="font-semibold text-gray-900 mb-1">API Reference</h3>
              <p class="text-sm text-gray-600">
                Developer API documentation
              </p>
            </NuxtLink>
            <div class="p-4 border border-gray-200 rounded-lg">
              <div class="text-3xl mb-2">💬</div>
              <h3 class="font-semibold text-gray-900 mb-1">Community</h3>
              <p class="text-sm text-gray-600">
                Join our Discord community
              </p>
            </div>
          </div>
        </section>

        <!-- Contact Form -->
        <section class="bg-white rounded-lg border border-gray-200 p-6">
          <h2 class="text-2xl font-semibold text-gray-900 mb-4">
            Contact Support
          </h2>
          <form class="space-y-4" @submit.prevent="handleSubmit">
            <!-- Name -->
            <div>
              <label for="name" class="block text-sm font-medium text-gray-700 mb-2">
                Name
              </label>
              <input
                id="name"
                v-model="form.name"
                type="text"
                required
                class="input w-full"
                placeholder="Your name"
              />
            </div>

            <!-- Email -->
            <div>
              <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
                Email
              </label>
              <input
                id="email"
                v-model="form.email"
                type="email"
                required
                class="input w-full"
                placeholder="your@email.com"
              />
            </div>

            <!-- Subject -->
            <div>
              <label for="subject" class="block text-sm font-medium text-gray-700 mb-2">
                Subject
              </label>
              <select id="subject" v-model="form.subject" class="input w-full" required>
                <option value="">Select a topic</option>
                <option value="technical">Technical Issue</option>
                <option value="billing">Billing Question</option>
                <option value="feature">Feature Request</option>
                <option value="feedback">General Feedback</option>
                <option value="other">Other</option>
              </select>
            </div>

            <!-- Message -->
            <div>
              <label for="message" class="block text-sm font-medium text-gray-700 mb-2">
                Message
              </label>
              <textarea
                id="message"
                v-model="form.message"
                rows="5"
                required
                class="input w-full"
                placeholder="How can we help you?"
              />
            </div>

            <!-- Submit -->
            <div class="flex justify-end">
              <button type="submit" class="btn btn--primary" :disabled="isSubmitting">
                <span v-if="!isSubmitting">Send Message</span>
                <span v-else class="flex items-center gap-2">
                  <span class="spinner h-4 w-4" aria-hidden="true" />
                  <span>Sending...</span>
                </span>
              </button>
            </div>
          </form>
        </section>

        <!-- Contact Info -->
        <section class="bg-white rounded-lg border border-gray-200 p-6">
          <h2 class="text-2xl font-semibold text-gray-900 mb-4">
            Other Ways to Reach Us
          </h2>
          <div class="space-y-4">
            <div class="flex items-start gap-3">
              <div class="text-2xl">📧</div>
              <div>
                <h3 class="font-semibold text-gray-900">Email</h3>
                <p class="text-sm text-gray-600">support@legally-ai.com</p>
                <p class="text-xs text-gray-500 mt-1">We respond within 24 hours</p>
              </div>
            </div>
            <div class="flex items-start gap-3">
              <div class="text-2xl">🐦</div>
              <div>
                <h3 class="font-semibold text-gray-900">Twitter</h3>
                <p class="text-sm text-gray-600">@LegallyAI</p>
                <p class="text-xs text-gray-500 mt-1">Follow us for updates</p>
              </div>
            </div>
            <div class="flex items-start gap-3">
              <div class="text-2xl">💼</div>
              <div>
                <h3 class="font-semibold text-gray-900">Enterprise Support</h3>
                <p class="text-sm text-gray-600">enterprise@legally-ai.com</p>
                <p class="text-xs text-gray-500 mt-1">For custom solutions and priority support</p>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

useHead({
  title: 'Support',
})

const form = ref({
  name: '',
  email: '',
  subject: '',
  message: '',
})

const isSubmitting = ref(false)

const handleSubmit = async () => {
  isSubmitting.value = true

  // TODO: Implement actual form submission
  // For now, just simulate a delay
  await new Promise(resolve => setTimeout(resolve, 1000))

  const { success } = useNotifications()
  success('Message sent!', 'We\'ll get back to you within 24 hours.')

  // Reset form
  form.value = {
    name: '',
    email: '',
    subject: '',
    message: '',
  }

  isSubmitting.value = false
}
</script>
