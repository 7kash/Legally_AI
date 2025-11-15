<template>
  <div class="min-h-screen bg-gray-50 py-12">
    <div class="container-custom max-w-4xl">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-4xl font-bold text-gray-900 mb-4">
          Documentation
        </h1>
        <p class="text-lg text-gray-600">
          Learn how to use Legally AI to analyze your contracts and understand legal documents.
        </p>
      </div>

      <!-- Content -->
      <div class="space-y-8">
        <!-- Getting Started -->
        <section class="bg-white rounded-lg border border-gray-200 p-6">
          <h2 class="text-2xl font-semibold text-gray-900 mb-4">
            Getting Started
          </h2>
          <div class="prose prose-sm max-w-none">
            <p class="text-gray-700 mb-4">
              Legally AI helps you understand contracts by analyzing them with advanced AI technology.
              Here's how to get started:
            </p>
            <ol class="list-decimal list-inside space-y-2 text-gray-700">
              <li>Create an account or log in</li>
              <li>Upload a contract (PDF or DOCX format)</li>
              <li>Select your preferred output language</li>
              <li>Wait for the AI analysis to complete</li>
              <li>Review the results and export if needed</li>
            </ol>
          </div>
        </section>

        <!-- Features -->
        <section class="bg-white rounded-lg border border-gray-200 p-6">
          <h2 class="text-2xl font-semibold text-gray-900 mb-4">
            Features
          </h2>
          <div class="grid gap-4 md:grid-cols-2">
            <div class="p-4 border border-gray-200 rounded-lg">
              <h3 class="font-semibold text-gray-900 mb-2">Contract Analysis</h3>
              <p class="text-sm text-gray-600">
                AI-powered analysis of obligations, rights, risks, and payment terms.
              </p>
            </div>
            <div class="p-4 border border-gray-200 rounded-lg">
              <h3 class="font-semibold text-gray-900 mb-2">Multi-language Support</h3>
              <p class="text-sm text-gray-600">
                Analyze contracts in English, Russian, Serbian, or French.
              </p>
            </div>
            <div class="p-4 border border-gray-200 rounded-lg">
              <h3 class="font-semibold text-gray-900 mb-2">Export Options</h3>
              <p class="text-sm text-gray-600">
                Export analysis results as PDF, DOCX, or JSON.
              </p>
            </div>
            <div class="p-4 border border-gray-200 rounded-lg">
              <h3 class="font-semibold text-gray-900 mb-2">GDPR Compliant</h3>
              <p class="text-sm text-gray-600">
                Full GDPR compliance with PII redaction and data export options.
              </p>
            </div>
          </div>
        </section>

        <!-- FAQ -->
        <section class="bg-white rounded-lg border border-gray-200 p-6">
          <h2 class="text-2xl font-semibold text-gray-900 mb-4">
            Frequently Asked Questions
          </h2>
          <div class="space-y-4">
            <div>
              <h3 class="font-semibold text-gray-900 mb-2">What file formats are supported?</h3>
              <p class="text-sm text-gray-600">
                We support PDF and DOCX (Microsoft Word) files. Files should not be password-protected.
              </p>
            </div>
            <div>
              <h3 class="font-semibold text-gray-900 mb-2">How long does analysis take?</h3>
              <p class="text-sm text-gray-600">
                Most contracts are analyzed within 30-60 seconds, depending on length and complexity.
              </p>
            </div>
            <div>
              <h3 class="font-semibold text-gray-900 mb-2">Is my data secure?</h3>
              <p class="text-sm text-gray-600">
                Yes! We use PII redaction, encryption, and follow GDPR compliance standards.
              </p>
            </div>
            <div>
              <h3 class="font-semibold text-gray-900 mb-2">Can I delete my data?</h3>
              <p class="text-sm text-gray-600">
                Absolutely. Go to your Account page to export or delete all your data at any time.
              </p>
            </div>
          </div>
        </section>

        <!-- CTA -->
        <div class="text-center">
          <NuxtLink to="/upload" class="btn btn--primary">
            Start Analyzing Contracts
          </NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
useHead({
  title: 'Documentation',
})
</script>
