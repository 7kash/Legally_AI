<template>
  <div class="flex flex-col">
    <!-- Hero Section -->
    <section class="relative bg-gradient-to-b from-primary-50 to-white py-20 sm:py-32">
      <div class="container-custom">
        <div class="mx-auto max-w-3xl text-center">
          <h1 class="text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl lg:text-6xl">
            AI-Powered Contract Analysis
          </h1>
          <p class="mt-6 text-lg leading-8 text-gray-600 sm:text-xl">
            Understand legal documents instantly with AI. Upload your contracts in Russian, Serbian,
            French, or English and get comprehensive analysis in seconds.
          </p>
          <div class="mt-10 flex items-center justify-center gap-4">
            <NuxtLink
              to="/register"
              class="btn btn--primary text-base px-6 py-3"
            >
              Get Started Free
            </NuxtLink>
            <NuxtLink
              to="/login"
              class="btn btn--secondary text-base px-6 py-3"
            >
              Sign In
            </NuxtLink>
          </div>
          <p class="mt-4 text-sm text-gray-500">
            Free tier: 3 contract analyses • No credit card required
          </p>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section
      id="features"
      class="py-20 sm:py-24"
    >
      <div class="container-custom">
        <div class="mx-auto max-w-2xl text-center">
          <h2 class="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
            Everything you need to understand contracts
          </h2>
          <p class="mt-4 text-lg text-gray-600">
            Powered by advanced AI to give you clear, actionable insights
          </p>
        </div>

        <div class="mx-auto mt-16 grid max-w-5xl gap-8 sm:grid-cols-2 lg:grid-cols-3">
          <!-- Feature 1: Multilingual -->
          <div class="card">
            <div
              class="flex h-12 w-12 items-center justify-center rounded-lg bg-primary-100"
              aria-hidden="true"
            >
              <svg
                class="h-6 w-6 text-primary-600"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129"
                />
              </svg>
            </div>
            <h3 class="mt-4 text-xl font-semibold text-gray-900">
              Multilingual Support
            </h3>
            <p class="mt-2 text-gray-600">
              Analyze contracts in Russian, Serbian, French, and English. Get results in your
              preferred language.
            </p>
          </div>

          <!-- Feature 2: Quick Analysis -->
          <div class="card">
            <div
              class="flex h-12 w-12 items-center justify-center rounded-lg bg-primary-100"
              aria-hidden="true"
            >
              <svg
                class="h-6 w-6 text-primary-600"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M13 10V3L4 14h7v7l9-11h-7z"
                />
              </svg>
            </div>
            <h3 class="mt-4 text-xl font-semibold text-gray-900">
              Instant Analysis
            </h3>
            <p class="mt-2 text-gray-600">
              Upload your contract and receive comprehensive analysis in seconds. No waiting, no
              hassle.
            </p>
          </div>

          <!-- Feature 3: Comprehensive Insights -->
          <div class="card">
            <div
              class="flex h-12 w-12 items-center justify-center rounded-lg bg-primary-100"
              aria-hidden="true"
            >
              <svg
                class="h-6 w-6 text-primary-600"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                />
              </svg>
            </div>
            <h3 class="mt-4 text-xl font-semibold text-gray-900">
              Detailed Breakdown
            </h3>
            <p class="mt-2 text-gray-600">
              Get plain language summaries, key clauses, obligations, rights, and risk analysis.
            </p>
          </div>

          <!-- Feature 4: Risk Detection -->
          <div class="card">
            <div
              class="flex h-12 w-12 items-center justify-center rounded-lg bg-primary-100"
              aria-hidden="true"
            >
              <svg
                class="h-6 w-6 text-primary-600"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                />
              </svg>
            </div>
            <h3 class="mt-4 text-xl font-semibold text-gray-900">
              Risk Assessment
            </h3>
            <p class="mt-2 text-gray-600">
              Identify potential risks and red flags in your contracts before signing.
            </p>
          </div>

          <!-- Feature 5: Q&A -->
          <div class="card">
            <div
              class="flex h-12 w-12 items-center justify-center rounded-lg bg-primary-100"
              aria-hidden="true"
            >
              <svg
                class="h-6 w-6 text-primary-600"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
                />
              </svg>
            </div>
            <h3 class="mt-4 text-xl font-semibold text-gray-900">
              Interactive Q&A
            </h3>
            <p class="mt-2 text-gray-600">
              Ask questions about your contract and get instant answers from AI.
            </p>
          </div>

          <!-- Feature 6: Secure -->
          <div class="card">
            <div
              class="flex h-12 w-12 items-center justify-center rounded-lg bg-primary-100"
              aria-hidden="true"
            >
              <svg
                class="h-6 w-6 text-primary-600"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
                />
              </svg>
            </div>
            <h3 class="mt-4 text-xl font-semibold text-gray-900">
              Secure & Private
            </h3>
            <p class="mt-2 text-gray-600">
              Your contracts are encrypted and secure. We never share your data with third parties.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="bg-primary-600 py-16 sm:py-20">
      <div class="container-custom">
        <div class="mx-auto max-w-2xl text-center">
          <h2 class="text-3xl font-bold tracking-tight text-white sm:text-4xl">
            Ready to analyze your first contract?
          </h2>
          <p class="mt-4 text-lg text-primary-100">
            Join thousands of users who trust Legally AI for their contract analysis needs.
          </p>
          <div class="mt-8">
            <NuxtLink
              to="/register"
              class="inline-flex items-center rounded-lg bg-white px-6 py-3 text-base font-semibold text-primary-600 shadow-sm transition-colors hover:bg-primary-50 focus:outline-none focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-offset-2 focus-visible:ring-offset-primary-600"
            >
              Start Free Trial
            </NuxtLink>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
/**
 * Homepage / Landing Page
 * Main entry point for unauthenticated users
 */

// Set page metadata
useHead({
  title: 'AI-Powered Contract Analysis',
})
</script>
