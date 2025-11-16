<template>
  <div class="min-h-screen bg-gray-50 py-12">
    <div class="container-custom max-w-4xl">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-4xl font-bold text-gray-900 mb-4">
          API Reference
        </h1>
        <p class="text-lg text-gray-600">
          Developer documentation for integrating Legally AI into your applications.
        </p>
      </div>

      <!-- Content -->
      <div class="space-y-8">
        <!-- Overview -->
        <section class="bg-white rounded-lg border border-gray-200 p-6">
          <h2 class="text-2xl font-semibold text-gray-900 mb-4">
            API Overview
          </h2>
          <p class="text-gray-700 mb-4">
            The Legally AI API allows you to programmatically analyze contracts and retrieve results.
            All API requests require authentication using JWT tokens.
          </p>
          <div class="bg-gray-50 border border-gray-200 rounded-lg p-4">
            <p class="text-sm font-mono text-gray-800">
              Base URL: <span class="text-primary-600">https://api.legally-ai.com/v1</span>
            </p>
          </div>
        </section>

        <!-- Authentication -->
        <section class="bg-white rounded-lg border border-gray-200 p-6">
          <h2 class="text-2xl font-semibold text-gray-900 mb-4">
            Authentication
          </h2>
          <p class="text-gray-700 mb-4">
            All API requests must include a Bearer token in the Authorization header:
          </p>
          <div class="bg-gray-900 text-gray-100 rounded-lg p-4 font-mono text-sm overflow-x-auto">
            <pre>Authorization: Bearer YOUR_JWT_TOKEN</pre>
          </div>
        </section>

        <!-- Endpoints -->
        <section class="bg-white rounded-lg border border-gray-200 p-6">
          <h2 class="text-2xl font-semibold text-gray-900 mb-4">
            Key Endpoints
          </h2>
          <div class="space-y-6">
            <!-- Upload Contract -->
            <div class="border-l-4 border-blue-500 pl-4">
              <h3 class="font-semibold text-gray-900 mb-2">
                <span class="inline-block bg-blue-100 text-blue-800 text-xs font-semibold px-2 py-1 rounded mr-2">POST</span>
                /contracts/upload
              </h3>
              <p class="text-sm text-gray-600 mb-2">Upload a contract for analysis</p>
              <div class="bg-gray-900 text-gray-100 rounded-lg p-4 font-mono text-xs overflow-x-auto">
                <pre>{
  "file": "base64_encoded_file",
  "filename": "contract.pdf"
}</pre>
              </div>
            </div>

            <!-- Create Analysis -->
            <div class="border-l-4 border-green-500 pl-4">
              <h3 class="font-semibold text-gray-900 mb-2">
                <span class="inline-block bg-green-100 text-green-800 text-xs font-semibold px-2 py-1 rounded mr-2">POST</span>
                /analyses
              </h3>
              <p class="text-sm text-gray-600 mb-2">Create a new contract analysis</p>
              <div class="bg-gray-900 text-gray-100 rounded-lg p-4 font-mono text-xs overflow-x-auto">
                <pre>{
  "contract_id": "uuid",
  "output_language": "english"
}</pre>
              </div>
            </div>

            <!-- Get Analysis -->
            <div class="border-l-4 border-purple-500 pl-4">
              <h3 class="font-semibold text-gray-900 mb-2">
                <span class="inline-block bg-purple-100 text-purple-800 text-xs font-semibold px-2 py-1 rounded mr-2">GET</span>
                /analyses/:id
              </h3>
              <p class="text-sm text-gray-600 mb-2">Retrieve analysis results</p>
              <div class="bg-gray-900 text-gray-100 rounded-lg p-4 font-mono text-xs overflow-x-auto">
                <pre>GET /analyses/550e8400-e29b-41d4-a716-446655440000</pre>
              </div>
            </div>
          </div>
        </section>

        <!-- Rate Limits -->
        <section class="bg-white rounded-lg border border-gray-200 p-6">
          <h2 class="text-2xl font-semibold text-gray-900 mb-4">
            Rate Limits
          </h2>
          <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <p class="text-sm text-yellow-800">
              <strong>Free Tier:</strong> 10 analyses per month<br>
              <strong>Pro Tier:</strong> 100 analyses per month<br>
              <strong>Enterprise:</strong> Custom limits
            </p>
          </div>
        </section>

        <!-- CTA -->
        <div class="text-center">
          <p class="text-gray-600 mb-4">Need API access?</p>
          <NuxtLink to="/support" class="btn btn--primary">
            Contact Support
          </NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
useHead({
  title: 'API Reference',
})
</script>
