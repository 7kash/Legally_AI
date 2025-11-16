<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 py-8">
    <div class="container-custom max-w-4xl">
      <!-- Loading State -->
      <div
        v-if="analysesStore.loading && !analysesStore.currentAnalysis"
        class="flex items-center justify-center py-20"
      >
        <div class="text-center">
          <div class="spinner mx-auto h-12 w-12" aria-hidden="true" />
          <p class="mt-4 text-gray-600">Loading analysis...</p>
        </div>
      </div>

      <!-- Error State -->
      <div
        v-else-if="analysesStore.error && !analysesStore.currentAnalysis"
        role="alert"
        class="alert alert--error"
      >
        <svg
          class="h-5 w-5 flex-shrink-0"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            fill-rule="evenodd"
            d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.28 7.22a.75.75 0 00-1.06 1.06L8.94 10l-1.72 1.72a.75.75 0 101.06 1.06L10 11.06l1.72 1.72a.75.75 0 101.06-1.06L11.06 10l1.72-1.72a.75.75 0 00-1.06-1.06L10 8.94 8.28 7.22z"
            clip-rule="evenodd"
          />
        </svg>
        <span>{{ analysesStore.error }}</span>
      </div>

      <!-- Analysis Content -->
      <template v-else-if="analysesStore.currentAnalysis">
        <!-- Header -->
        <div class="mb-8 text-center">
          <h1 class="text-4xl font-bold text-gray-900 mb-2">
            Contract Analysis
          </h1>
          <p class="text-gray-600">
            AI-powered insights for your contract
          </p>
        </div>

        <!-- Processing State -->
        <div
          v-if="analysesStore.isAnalyzing"
          class="bg-white rounded-xl shadow-lg border border-gray-200 p-8"
        >
          <div class="text-center">
            <div class="spinner mx-auto h-12 w-12 mb-4" />
            <h2 class="text-xl font-semibold text-gray-900 mb-2">
              Analyzing your contract...
            </h2>
            <p class="text-gray-600 mb-6">
              This may take a few moments. Please don't close this page.
            </p>

            <!-- Progress Events -->
            <div v-if="analysesStore.events.length > 0" class="mt-6 space-y-2">
              <h3 class="text-sm font-medium text-gray-700 mb-3">Progress:</h3>
              <div class="space-y-2 max-h-48 overflow-y-auto">
                <div
                  v-for="(event, index) in analysesStore.events"
                  :key="index"
                  class="flex items-start gap-2 text-sm text-left"
                >
                  <svg
                    class="h-5 w-5 text-green-500 flex-shrink-0 mt-0.5"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                  >
                    <path
                      fill-rule="evenodd"
                      d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z"
                      clip-rule="evenodd"
                    />
                  </svg>
                  <span class="text-gray-700">{{ formatEventMessage(event) }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Analysis Results -->
        <div v-else-if="analysesStore.hasResults" class="space-y-6">
          <!-- ELI5 Mode Toggle -->
          <div class="flex items-center justify-center mb-4">
            <button
              type="button"
              class="inline-flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all"
              :class="{
                'bg-purple-600 text-white hover:bg-purple-700': eli5Enabled,
                'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50': !eli5Enabled
              }"
              :disabled="eli5Loading"
              @click="toggleELI5Mode"
            >
              <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              <span v-if="eli5Loading">Simplifying...</span>
              <span v-else-if="eli5Enabled">Simple Mode (ON)</span>
              <span v-else>Explain Like I'm 5</span>
            </button>
          </div>

          <!-- ELI5 Info Banner -->
          <div
            v-if="eli5Enabled"
            class="bg-purple-50 border border-purple-200 rounded-lg p-4 flex items-start gap-3"
          >
            <svg class="h-5 w-5 text-purple-600 flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div>
              <p class="text-sm font-medium text-purple-900">Simple Mode Active</p>
              <p class="text-sm text-purple-700">Legal terms are now explained in everyday language that's easy to understand.</p>
            </div>
          </div>

          <!-- 1. Important Limits Disclaimer -->
          <ImportantLimits />

          <!-- 2. Screening Badge -->
          <ScreeningBadge v-if="screeningResult" :variant="screeningResult" />

          <!-- 3. Confidence Level -->
          <div
            v-if="analysesStore.currentAnalysis?.confidence_score != null && analysesStore.currentAnalysis.confidence_score !== undefined"
            class="bg-white rounded-xl shadow-sm border border-gray-200 p-6"
          >
            <h2 class="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <svg class="h-5 w-5 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Confidence Level
            </h2>
            <div class="flex items-center gap-4 mb-3">
              <div class="flex-1 bg-gray-200 rounded-full h-3">
                <div
                  class="h-3 rounded-full transition-all"
                  :class="{
                    'bg-green-500': analysesStore.currentAnalysis.confidence_score >= 0.8,
                    'bg-yellow-500': analysesStore.currentAnalysis.confidence_score >= 0.6 && analysesStore.currentAnalysis.confidence_score < 0.8,
                    'bg-red-500': analysesStore.currentAnalysis.confidence_score < 0.6,
                  }"
                  :style="{ width: `${analysesStore.currentAnalysis.confidence_score * 100}%` }"
                />
              </div>
              <span class="text-lg font-bold text-gray-900">
                {{ Math.round(analysesStore.currentAnalysis.confidence_score * 100) }}%
              </span>
            </div>
            <p v-if="confidenceReason" class="text-sm text-gray-600">
              {{ confidenceReason }}
            </p>
          </div>

          <!-- 4. About the Contract (Summary only) -->
          <div v-if="getAboutSummary()" class="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl shadow-sm border border-blue-200 p-6">
            <h2 class="text-lg font-semibold text-gray-900 mb-3 flex items-center gap-2">
              <svg class="h-5 w-5 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              About the Contract
            </h2>
            <p class="text-gray-800 leading-relaxed">{{ getAboutSummary() }}</p>
          </div>

          <!-- 5. Agreement Type -->
          <WidgetCard v-if="getAgreementType()" :title="getAgreementTypeTitle()" icon="document">
            <p class="text-gray-800 font-medium">{{ getAgreementType() }}</p>
          </WidgetCard>

          <!-- 6. Parties -->
          <WidgetCard v-if="getParties().length > 0" :title="getPartiesTitle()" icon="users">
            <div class="space-y-3">
              <div
                v-for="(party, index) in getParties()"
                :key="index"
                class="flex items-start gap-3 p-3 bg-gray-50 rounded-lg"
              >
                <div class="flex-1">
                  <p class="font-semibold text-gray-900">{{ party.name || 'Party ' + (index + 1) }}</p>
                  <p v-if="party.role" class="text-sm text-gray-600">{{ party.role }}</p>
                </div>
              </div>
            </div>
          </WidgetCard>

          <!-- 7. Jurisdiction -->
          <WidgetCard v-if="getJurisdiction()" :title="getJurisdictionTitle()" icon="globe">
            <p class="text-gray-800 font-medium">{{ getJurisdiction() }}</p>
          </WidgetCard>

          <!-- 8. Obligations -->
          <WidgetCard v-if="getObligations().length > 0" :title="getObligationsTitle()" icon="clipboard" color="blue">
            <div class="space-y-4">
              <div
                v-for="(item, index) in getObligations()"
                :key="index"
                class="border-l-4 border-blue-500 pl-4 py-3 bg-blue-50 rounded-r-lg"
              >
                <!-- Show simplified text in ELI5 mode -->
                <p v-if="eli5Enabled && item.action_simple" class="text-gray-800 leading-relaxed">{{ item.action_simple }}</p>
                <!-- Show normal text otherwise -->
                <template v-else>
                  <p class="font-semibold text-gray-900">{{ item.action }}</p>
                  <div v-if="item.time_window || item.trigger" class="mt-2 space-y-1">
                    <p v-if="item.trigger" class="text-sm text-gray-700">
                      <span class="font-medium">When:</span> {{ item.trigger }}
                    </p>
                    <p v-if="item.time_window" class="text-sm text-gray-700">
                      <span class="font-medium">Deadline:</span> {{ item.time_window }}
                    </p>
                  </div>
                  <p v-if="item.consequence" class="mt-2 text-sm text-red-700 bg-red-50 p-2 rounded">
                    <span class="font-medium">⚠️ If not done:</span> {{ item.consequence }}
                  </p>
                </template>
                <!-- Source quote toggle button or "Not found" message -->
                <button
                  v-if="hasValidQuote(item)"
                  type="button"
                  class="mt-3 text-xs text-blue-600 hover:text-blue-700 font-medium flex items-center gap-1"
                  @click="toggleQuote('obligation-' + index)"
                >
                  <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  {{ expandedQuotes['obligation-' + index] ? 'Hide source' : 'Tell me more about it' }}
                </button>
                <div
                  v-else
                  class="mt-3 text-xs text-gray-400 font-medium flex items-center gap-1"
                >
                  <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Not found in the document text
                </div>
                <div
                  v-if="expandedQuotes['obligation-' + index] && hasValidQuote(item)"
                  class="mt-2 bg-white border border-gray-300 rounded-lg p-4 text-sm space-y-3"
                >
                  <div>
                    <p class="font-semibold text-gray-900 mb-2 flex items-center gap-1">
                      <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                      Original contract text:
                    </p>
                    <p class="italic text-gray-700 bg-gray-50 p-3 rounded border-l-2 border-blue-400">"{{ item.quote_original || item.quote }}"</p>
                  </div>
                  <div v-if="item.quote_translated && item.quote_translated !== item.quote_original">
                    <p class="font-semibold text-gray-900 mb-2 flex items-center gap-1">
                      <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129" />
                      </svg>
                      Translation:
                    </p>
                    <p class="text-gray-700 bg-blue-50 p-3 rounded border-l-2 border-blue-600">"{{ item.quote_translated }}"</p>
                  </div>
                </div>

                <!-- Feedback buttons -->
                <div class="mt-3 pt-3 border-t border-blue-200 flex items-center gap-2">
                  <span class="text-xs text-gray-600">Was this helpful?</span>
                  <div class="flex gap-2">
                    <button
                      type="button"
                      class="flex items-center gap-1 px-2 py-1 rounded text-xs transition-colors"
                      :class="{
                        'bg-green-100 text-green-700': feedbackSubmitted['obligations-' + index],
                        'bg-gray-100 text-gray-600 hover:bg-green-50 hover:text-green-600': !feedbackSubmitted['obligations-' + index]
                      }"
                      :disabled="feedbackSubmitted['obligations-' + index] || feedbackLoading['obligations-' + index]"
                      @click="submitFeedback('obligations', index, true)"
                    >
                      <svg class="h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M2 10.5a1.5 1.5 0 113 0v6a1.5 1.5 0 01-3 0v-6zM6 10.333v5.43a2 2 0 001.106 1.79l.05.025A4 4 0 008.943 18h5.416a2 2 0 001.962-1.608l1.2-6A2 2 0 0015.56 8H12V4a2 2 0 00-2-2 1 1 0 00-1 1v.667a4 4 0 01-.8 2.4L6.8 7.933a4 4 0 00-.8 2.4z" />
                      </svg>
                      {{ feedbackSubmitted['obligations-' + index] ? 'Thanks!' : 'Yes' }}
                    </button>
                    <button
                      type="button"
                      class="flex items-center gap-1 px-2 py-1 rounded text-xs transition-colors"
                      :class="{
                        'bg-red-100 text-red-700': feedbackSubmitted['obligations-' + index],
                        'bg-gray-100 text-gray-600 hover:bg-red-50 hover:text-red-600': !feedbackSubmitted['obligations-' + index]
                      }"
                      :disabled="feedbackSubmitted['obligations-' + index] || feedbackLoading['obligations-' + index]"
                      @click="submitFeedback('obligations', index, false)"
                    >
                      <svg class="h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M18 9.5a1.5 1.5 0 11-3 0v-6a1.5 1.5 0 013 0v6zM14 9.667v-5.43a2 2 0 00-1.105-1.79l-.05-.025A4 4 0 0011.055 2H5.64a2 2 0 00-1.962 1.608l-1.2 6A2 2 0 004.44 12H8v4a2 2 0 002 2 1 1 0 001-1v-.667a4 4 0 01.8-2.4l1.4-1.866a4 4 0 00.8-2.4z" />
                      </svg>
                      No
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </WidgetCard>

          <!-- 9. Rights -->
          <WidgetCard v-if="getRights().length > 0" :title="getRightsTitle()" icon="shield" color="green">
            <div class="space-y-4">
              <div
                v-for="(item, index) in getRights()"
                :key="index"
                class="border-l-4 border-green-500 pl-4 py-3 bg-green-50 rounded-r-lg"
              >
                <!-- Show simplified text in ELI5 mode -->
                <p v-if="eli5Enabled && item.right_simple" class="text-gray-800 leading-relaxed">{{ item.right_simple }}</p>
                <!-- Show normal text otherwise -->
                <template v-else>
                  <p class="font-semibold text-gray-900">{{ item.right }}</p>
                  <p v-if="item.how_to_exercise" class="mt-2 text-sm text-gray-700">
                    <span class="font-medium">How to exercise:</span> {{ item.how_to_exercise }}
                  </p>
                  <p v-if="item.conditions" class="mt-1 text-sm text-gray-600">
                    <span class="font-medium">Conditions:</span> {{ item.conditions }}
                  </p>
                </template>
                <!-- Source quote toggle button or "Not found" message -->
                <button
                  v-if="hasValidQuote(item)"
                  type="button"
                  class="mt-3 text-xs text-green-600 hover:text-green-700 font-medium flex items-center gap-1"
                  @click="toggleQuote('right-' + index)"
                >
                  <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  {{ expandedQuotes['right-' + index] ? 'Hide source' : 'Tell me more about it' }}
                </button>
                <div
                  v-else
                  class="mt-3 text-xs text-gray-400 font-medium flex items-center gap-1"
                >
                  <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Not found in the document text
                </div>
                <div
                  v-if="expandedQuotes['right-' + index] && hasValidQuote(item)"
                  class="mt-2 bg-white border border-gray-300 rounded-lg p-4 text-sm space-y-3"
                >
                  <div>
                    <p class="font-semibold text-gray-900 mb-2 flex items-center gap-1">
                      <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                      Original contract text:
                    </p>
                    <p class="italic text-gray-700 bg-gray-50 p-3 rounded border-l-2 border-green-400">"{{ item.quote_original || item.quote }}"</p>
                  </div>
                  <div v-if="item.quote_translated && item.quote_translated !== item.quote_original">
                    <p class="font-semibold text-gray-900 mb-2 flex items-center gap-1">
                      <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129" />
                      </svg>
                      Translation:
                    </p>
                    <p class="text-gray-700 bg-green-50 p-3 rounded border-l-2 border-green-600">"{{ item.quote_translated }}"</p>
                  </div>
                </div>

                <!-- Feedback buttons -->
                <div class="mt-3 pt-3 border-t border-green-200 flex items-center gap-2">
                  <span class="text-xs text-gray-600">Was this helpful?</span>
                  <div class="flex gap-2">
                    <button
                      type="button"
                      class="flex items-center gap-1 px-2 py-1 rounded text-xs transition-colors"
                      :class="{
                        'bg-green-100 text-green-700': feedbackSubmitted['rights-' + index],
                        'bg-gray-100 text-gray-600 hover:bg-green-50 hover:text-green-600': !feedbackSubmitted['rights-' + index]
                      }"
                      :disabled="feedbackSubmitted['rights-' + index] || feedbackLoading['rights-' + index]"
                      @click="submitFeedback('rights', index, true)"
                    >
                      <svg class="h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M2 10.5a1.5 1.5 0 113 0v6a1.5 1.5 0 01-3 0v-6zM6 10.333v5.43a2 2 0 001.106 1.79l.05.025A4 4 0 008.943 18h5.416a2 2 0 001.962-1.608l1.2-6A2 2 0 0015.56 8H12V4a2 2 0 00-2-2 1 1 0 00-1 1v.667a4 4 0 01-.8 2.4L6.8 7.933a4 4 0 00-.8 2.4z" />
                      </svg>
                      {{ feedbackSubmitted['rights-' + index] ? 'Thanks!' : 'Yes' }}
                    </button>
                    <button
                      type="button"
                      class="flex items-center gap-1 px-2 py-1 rounded text-xs transition-colors"
                      :class="{
                        'bg-red-100 text-red-700': feedbackSubmitted['rights-' + index],
                        'bg-gray-100 text-gray-600 hover:bg-red-50 hover:text-red-600': !feedbackSubmitted['rights-' + index]
                      }"
                      :disabled="feedbackSubmitted['rights-' + index] || feedbackLoading['rights-' + index]"
                      @click="submitFeedback('rights', index, false)"
                    >
                      <svg class="h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M18 9.5a1.5 1.5 0 11-3 0v-6a1.5 1.5 0 013 0v6zM14 9.667v-5.43a2 2 0 00-1.105-1.79l-.05-.025A4 4 0 0011.055 2H5.64a2 2 0 00-1.962 1.608l-1.2 6A2 2 0 004.44 12H8v4a2 2 0 002 2 1 1 0 001-1v-.667a4 4 0 01.8-2.4l1.4-1.866a4 4 0 00.8-2.4z" />
                      </svg>
                      No
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </WidgetCard>

          <!-- 10. Payment Terms -->
          <WidgetCard v-if="getPaymentTerms().length > 0" :title="getPaymentTermsTitle()" icon="currency" color="emerald">
            <div class="space-y-3">
              <div
                v-for="(term, index) in getPaymentTerms()"
                :key="index"
                class="p-3 bg-emerald-50 border border-emerald-200 rounded-lg"
              >
                <p class="text-gray-800">{{ term }}</p>
              </div>
            </div>
          </WidgetCard>

          <!-- 11. Key Dates & Deadlines -->
          <WidgetCard v-if="getCalendar().length > 0" :title="getCalendarTitle()" icon="calendar" color="purple">
            <div class="space-y-3">
              <div
                v-for="(item, index) in getCalendar()"
                :key="index"
                class="flex items-start gap-4 p-3 bg-purple-50 border border-purple-200 rounded-lg"
              >
                <div class="flex-shrink-0 w-28">
                  <p class="font-bold text-purple-700 text-sm">{{ item.date_or_formula || item.date }}</p>
                </div>
                <div class="flex-1">
                  <p class="text-gray-800">{{ item.event || item.description }}</p>
                </div>
              </div>
            </div>
          </WidgetCard>

          <!-- 12. Risks -->
          <WidgetCard v-if="getRisks().length > 0" :title="getRisksTitle()" icon="warning" color="red">
            <div class="space-y-4">
              <div
                v-for="(item, index) in getRisks()"
                :key="index"
                class="border-l-4 pl-4 py-3 rounded-r-lg"
                :class="{
                  'border-red-500 bg-red-50': item.level === 'high',
                  'border-yellow-500 bg-yellow-50': item.level === 'medium',
                  'border-green-500 bg-green-50': item.level === 'low',
                }"
              >
                <div class="flex items-center gap-2 mb-2">
                  <span
                    class="px-2 py-1 rounded-full text-xs font-bold"
                    :class="{
                      'bg-red-600 text-white': item.level === 'high',
                      'bg-yellow-600 text-white': item.level === 'medium',
                      'bg-green-600 text-white': item.level === 'low',
                    }"
                  >
                    {{ item.level?.toUpperCase() }}
                  </span>
                  <span v-if="item.category" class="text-xs text-gray-600 uppercase tracking-wide">{{ item.category }}</span>
                </div>
                <!-- Show simplified text in ELI5 mode -->
                <p v-if="eli5Enabled && item.description_simple" class="text-gray-800 leading-relaxed">{{ item.description_simple }}</p>
                <!-- Show normal text otherwise -->
                <template v-else>
                  <p class="font-semibold text-gray-900">{{ item.description }}</p>
                  <p v-if="item.recommendation" class="mt-2 text-sm text-blue-700 bg-blue-50 p-2 rounded">
                    <span class="font-medium">💡 Recommendation:</span> {{ item.recommendation }}
                  </p>
                </template>
                <!-- Source quote toggle button or "Not found" message -->
                <button
                  v-if="hasValidQuote(item)"
                  type="button"
                  class="mt-3 text-xs text-blue-600 hover:text-blue-700 font-medium flex items-center gap-1"
                  @click="toggleQuote('risk-' + index)"
                >
                  <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  {{ expandedQuotes['risk-' + index] ? 'Hide source' : 'Tell me more about it' }}
                </button>
                <div
                  v-else
                  class="mt-3 text-xs text-gray-400 font-medium flex items-center gap-1"
                >
                  <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Not found in the document text
                </div>
                <div
                  v-if="expandedQuotes['risk-' + index] && hasValidQuote(item)"
                  class="mt-2 bg-white border border-gray-300 rounded-lg p-4 text-sm space-y-3"
                >
                  <div>
                    <p class="font-semibold text-gray-900 mb-2 flex items-center gap-1">
                      <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                      Original contract text:
                    </p>
                    <p class="italic text-gray-700 bg-gray-50 p-3 rounded border-l-2 border-red-400">"{{ item.quote_original || item.quote }}"</p>
                  </div>
                  <div v-if="item.quote_translated && item.quote_translated !== item.quote_original">
                    <p class="font-semibold text-gray-900 mb-2 flex items-center gap-1">
                      <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129" />
                      </svg>
                      Translation:
                    </p>
                    <p class="text-gray-700 bg-red-50 p-3 rounded border-l-2 border-red-600">"{{ item.quote_translated }}"</p>
                  </div>
                </div>

                <!-- Feedback buttons -->
                <div class="mt-3 pt-3 border-t"
                  :class="{
                    'border-red-200': item.level === 'high',
                    'border-yellow-200': item.level === 'medium',
                    'border-green-200': item.level === 'low',
                  }"
                >
                  <div class="flex items-center gap-2">
                    <span class="text-xs text-gray-600">Was this helpful?</span>
                    <div class="flex gap-2">
                      <button
                        type="button"
                        class="flex items-center gap-1 px-2 py-1 rounded text-xs transition-colors"
                        :class="{
                          'bg-green-100 text-green-700': feedbackSubmitted['risks-' + index],
                          'bg-gray-100 text-gray-600 hover:bg-green-50 hover:text-green-600': !feedbackSubmitted['risks-' + index]
                        }"
                        :disabled="feedbackSubmitted['risks-' + index] || feedbackLoading['risks-' + index]"
                        @click="submitFeedback('risks', index, true)"
                      >
                        <svg class="h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                          <path d="M2 10.5a1.5 1.5 0 113 0v6a1.5 1.5 0 01-3 0v-6zM6 10.333v5.43a2 2 0 001.106 1.79l.05.025A4 4 0 008.943 18h5.416a2 2 0 001.962-1.608l1.2-6A2 2 0 0015.56 8H12V4a2 2 0 00-2-2 1 1 0 00-1 1v.667a4 4 0 01-.8 2.4L6.8 7.933a4 4 0 00-.8 2.4z" />
                        </svg>
                        {{ feedbackSubmitted['risks-' + index] ? 'Thanks!' : 'Yes' }}
                      </button>
                      <button
                        type="button"
                        class="flex items-center gap-1 px-2 py-1 rounded text-xs transition-colors"
                        :class="{
                          'bg-red-100 text-red-700': feedbackSubmitted['risks-' + index],
                          'bg-gray-100 text-gray-600 hover:bg-red-50 hover:text-red-600': !feedbackSubmitted['risks-' + index]
                        }"
                        :disabled="feedbackSubmitted['risks-' + index] || feedbackLoading['risks-' + index]"
                        @click="submitFeedback('risks', index, false)"
                      >
                        <svg class="h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                          <path d="M18 9.5a1.5 1.5 0 11-3 0v-6a1.5 1.5 0 013 0v6zM14 9.667v-5.43a2 2 0 00-1.105-1.79l-.05-.025A4 4 0 0011.055 2H5.64a2 2 0 00-1.962 1.608l-1.2 6A2 2 0 004.44 12H8v4a2 2 0 002 2 1 1 0 001-1v-.667a4 4 0 01.8-2.4l1.4-1.866a4 4 0 00.8-2.4z" />
                        </svg>
                        No
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </WidgetCard>

          <!-- 13. Mitigations -->
          <WidgetCard v-if="getMitigations().length > 0" :title="getMitigationsTitle()" icon="shield-check" color="amber">
            <p class="text-sm text-gray-600 mb-4">
              If you must sign without changes, take these steps to reduce risks:
            </p>
            <div class="space-y-4">
              <div
                v-for="(item, index) in getMitigations()"
                :key="index"
                class="border-l-4 border-amber-500 pl-4 py-3 bg-amber-50 rounded-r-lg"
              >
                <div class="flex items-start gap-3">
                  <svg class="h-5 w-5 text-amber-600 flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <p class="text-gray-800 font-medium">{{ typeof item === 'string' ? item : item.mitigation || item.text || item.description }}</p>
                </div>
                <!-- Source quote toggle button or "Not found" message -->
                <button
                  v-if="(typeof item === 'object') && hasValidQuote(item)"
                  type="button"
                  class="mt-3 ml-8 text-xs text-amber-600 hover:text-amber-700 font-medium flex items-center gap-1"
                  @click="toggleQuote('mitigation-' + index)"
                >
                  <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  {{ expandedQuotes['mitigation-' + index] ? 'Hide related risk' : 'Tell me more about it' }}
                </button>
                <div
                  v-else-if="typeof item === 'object'"
                  class="mt-3 ml-8 text-xs text-gray-400 font-medium flex items-center gap-1"
                >
                  <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Not found in the document text
                </div>
                <div
                  v-if="expandedQuotes['mitigation-' + index] && (typeof item === 'object') && hasValidQuote(item)"
                  class="mt-2 ml-8 bg-white border border-gray-300 rounded-lg p-4 text-sm space-y-3"
                >
                  <div>
                    <p class="font-semibold text-gray-900 mb-2 flex items-center gap-1">
                      <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                      Original contract text (risky clause):
                    </p>
                    <p class="italic text-gray-700 bg-gray-50 p-3 rounded border-l-2 border-amber-400">"{{ item.quote_original || item.related_risk_quote }}"</p>
                  </div>
                  <div v-if="item.quote_translated && item.quote_translated !== item.quote_original">
                    <p class="font-semibold text-gray-900 mb-2 flex items-center gap-1">
                      <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129" />
                      </svg>
                      Translation:
                    </p>
                    <p class="text-gray-700 bg-amber-50 p-3 rounded border-l-2 border-amber-600">"{{ item.quote_translated }}"</p>
                  </div>
                </div>
              </div>
            </div>
          </WidgetCard>

          <!-- Actions -->
          <div class="flex flex-wrap gap-3 pt-4">
            <button
              type="button"
              class="btn btn--primary flex items-center gap-2"
              @click="handleExport"
            >
              <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
              Export Results
            </button>
            <NuxtLink to="/upload" class="btn btn--secondary">
              Analyze Another Contract
            </NuxtLink>
            <NuxtLink to="/history" class="btn btn--secondary">
              View History
            </NuxtLink>
          </div>
        </div>

        <!-- Failed State -->
        <div
          v-else-if="analysesStore.currentAnalysis.status === 'failed'"
          class="bg-white rounded-xl shadow-lg border border-red-200 p-8"
        >
          <div class="text-center">
            <svg
              class="mx-auto h-12 w-12 text-red-500 mb-4"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            <h2 class="text-xl font-semibold text-gray-900 mb-2">
              Analysis Failed
            </h2>
            <p class="text-gray-600 mb-6">
              We encountered an error while analyzing your contract. Please try again.
            </p>
            <NuxtLink to="/upload" class="btn btn--primary">
              Upload New Contract
            </NuxtLink>
          </div>
        </div>
      </template>

      <!-- Export Modal -->
      <ExportModal
        v-model="showExportModal"
        @export="handleExportFormat"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, computed, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useAnalysesStore } from '~/stores/analyses'
import { useAuthStore } from '~/stores/auth'
import type { AnalysisEvent } from '~/stores/analyses'
import { exportAnalysisToPDF } from '~/utils/exportToPDF'
import { exportAnalysisToDOCX } from '~/utils/exportToDOCX'
import { exportLawyerPackToPDF } from '~/utils/exportLawyerPack'

definePageMeta({
  middleware: 'auth',
})

const route = useRoute()
const analysesStore = useAnalysesStore()
const authStore = useAuthStore()

const analysisId = computed(() => route.params.id as string)
const showExportModal = ref(false)
const expandedQuotes = ref<Record<string, boolean>>({})

// ELI5 Mode state
const eli5Enabled = ref(false)
const eli5Data = ref<any>(null)
const eli5Loading = ref(false)
const eli5Error = ref<string | null>(null)

// Feedback state
const feedbackSubmitted = ref<Record<string, boolean>>({})
const feedbackLoading = ref<Record<string, boolean>>({})

const formattedOutput = computed(() => {
  return analysesStore.currentAnalysis?.formatted_output || {}
})

const screeningResult = computed(() => {
  const prepResult = analysesStore.currentAnalysis?.preparation_result
  const analysisResult = analysesStore.currentAnalysis?.analysis_result

  return (
    prepResult?.screening_result ||
    analysisResult?.screening_result ||
    formattedOutput.value.screening_result ||
    'preliminary_review'
  )
})

const confidenceLevel = computed(() => {
  const score = analysesStore.currentAnalysis?.confidence_score
  if (!score) return 'Unknown'
  if (score >= 0.8) return 'High'
  if (score >= 0.6) return 'Medium'
  return 'Low'
})

const confidenceReason = computed(() => {
  const prepResult = analysesStore.currentAnalysis?.preparation_result
  const analysisResult = analysesStore.currentAnalysis?.analysis_result

  return (
    prepResult?.confidence?.reason ||
    analysisResult?.confidence?.reason ||
    formattedOutput.value.confidence_reason
  )
})

// Helper functions
function getAboutSummary(): string {
  const prepResult = analysesStore.currentAnalysis?.preparation_result
  const analysisResult = analysesStore.currentAnalysis?.analysis_result

  return (
    analysisResult?.about_summary ||
    prepResult?.about ||
    formattedOutput.value.about?.description ||
    ''
  )
}

function getAgreementType(): string {
  const prepResult = analysesStore.currentAnalysis?.preparation_result
  const data = formattedOutput.value.agreement_type

  return (
    prepResult?.agreement_type ||
    (typeof data === 'string' ? data : data?.content || '')
  )
}

function getAgreementTypeTitle(): string {
  return formattedOutput.value.agreement_type?.title || 'Agreement Type'
}

function getParties(): any[] {
  const prepResult = analysesStore.currentAnalysis?.preparation_result
  const data = formattedOutput.value.parties

  if (prepResult?.parties && Array.isArray(prepResult.parties)) {
    return prepResult.parties
  }
  if (!data) return []
  if (Array.isArray(data)) return data
  if (data.content && Array.isArray(data.content)) return data.content
  return []
}

function getPartiesTitle(): string {
  return formattedOutput.value.parties?.title || 'Parties'
}

function getJurisdiction(): string {
  const prepResult = analysesStore.currentAnalysis?.preparation_result
  const data = formattedOutput.value.jurisdiction

  return (
    prepResult?.detected_jurisdiction ||
    prepResult?.jurisdiction ||
    (typeof data === 'string' ? data : data?.content || '')
  )
}

function getObligations(): any[] {
  const currentData = getCurrentData()

  // Check for simplified data first
  if (eli5Enabled.value && currentData.obligations_simplified) {
    return Array.isArray(currentData.obligations_simplified)
      ? currentData.obligations_simplified
      : []
  }

  // Fall back to normal obligations
  const data = currentData.obligations
  if (!data) return []
  if (Array.isArray(data)) return data
  if (data.content && Array.isArray(data.content)) return data.content
  return []
}

function getRights(): any[] {
  const currentData = getCurrentData()

  // Check for simplified data first
  if (eli5Enabled.value && currentData.rights_simplified) {
    return Array.isArray(currentData.rights_simplified)
      ? currentData.rights_simplified
      : []
  }

  // Fall back to normal rights
  const data = currentData.rights
  if (!data) return []
  if (Array.isArray(data)) return data
  if (data.content && Array.isArray(data.content)) return data.content
  return []
}

function getPaymentTerms(): string[] {
  const data = formattedOutput.value.payment_terms
  if (!data) return []

  if (Array.isArray(data)) return data
  if (data.content) {
    if (Array.isArray(data.content)) return data.content
    if (typeof data.content === 'object') {
      const terms: string[] = []
      Object.entries(data.content).forEach(([key, value]) => {
        if (value && typeof value === 'string') {
          terms.push(`${key.replace(/_/g, ' ')}: ${value}`)
        }
      })
      return terms
    }
  }
  return []
}

function getRisks(): any[] {
  const currentData = getCurrentData()

  // Check for simplified data first
  if (eli5Enabled.value && currentData.risks_simplified) {
    return Array.isArray(currentData.risks_simplified)
      ? currentData.risks_simplified
      : []
  }

  // Fall back to normal risks
  const data = currentData.risks
  if (!data) return []
  if (Array.isArray(data)) return data
  if (data.content && Array.isArray(data.content)) return data.content
  return []
}

function getCalendar(): any[] {
  const data = formattedOutput.value.calendar
  if (!data) return []
  if (Array.isArray(data)) return data
  if (data.content && Array.isArray(data.content)) return data.content
  return []
}

function getMitigations(): any[] {
  const data = formattedOutput.value.mitigations
  if (!data) return []
  if (Array.isArray(data)) return data
  if (data.content && Array.isArray(data.content)) return data.content
  return []
}

// Title getter functions
function getJurisdictionTitle(): string {
  return formattedOutput.value.jurisdiction?.title || 'Jurisdiction'
}

function getObligationsTitle(): string {
  return formattedOutput.value.obligations?.title || 'Your Obligations'
}

function getRightsTitle(): string {
  return formattedOutput.value.rights?.title || 'Your Rights'
}

function getPaymentTermsTitle(): string {
  return formattedOutput.value.payment_terms?.title || 'Payment Terms'
}

function getRisksTitle(): string {
  return formattedOutput.value.risks?.title || 'Risks & Concerns'
}

function getCalendarTitle(): string {
  return formattedOutput.value.calendar?.title || 'Key Dates & Deadlines'
}

function getMitigationsTitle(): string {
  return formattedOutput.value.mitigations?.title || 'Risk Mitigations'
}

function toggleQuote(key: string): void {
  expandedQuotes.value[key] = !expandedQuotes.value[key]
}

// Helper function to check if a quote is valid and should be shown
function hasValidQuote(item: any): boolean {
  const checkQuote = (quote: any): boolean => {
    if (!quote) return false
    if (typeof quote !== 'string') return false
    const trimmed = quote.trim()
    if (trimmed === '' || trimmed === 'null' || trimmed === 'undefined' || trimmed === 'None') return false
    return true
  }

  return checkQuote(item.quote_original) || checkQuote(item.quote) || checkQuote(item.related_risk_quote)
}

// ELI5 Mode functions
async function toggleELI5Mode(): Promise<void> {
  if (eli5Enabled.value) {
    // Turn off ELI5 mode
    eli5Enabled.value = false
    return
  }

  // Turn on ELI5 mode
  if (eli5Data.value) {
    // Already have simplified data, just enable it
    eli5Enabled.value = true
    return
  }

  // Fetch simplified data
  try {
    eli5Loading.value = true
    eli5Error.value = null

    const config = useRuntimeConfig()
    const response = await fetch(
      `${config.public.apiBase}/analyses/${analysisId.value}/simplify`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authStore.token}`,
        },
        credentials: 'include',
      }
    )

    if (!response.ok) {
      throw new Error('Failed to simplify analysis')
    }

    const data = await response.json()
    eli5Data.value = data.simplified_analysis
    eli5Enabled.value = true
  } catch (error: any) {
    console.error('Failed to simplify analysis:', error)
    eli5Error.value = error.message || 'Failed to simplify analysis'
    const { error: showError } = useNotifications()
    showError('Simplification failed', 'Please try again later.')
  } finally {
    eli5Loading.value = false
  }
}

// Get data based on ELI5 mode
function getCurrentData(): any {
  if (eli5Enabled.value && eli5Data.value) {
    return eli5Data.value
  }
  return formattedOutput.value
}

// Feedback functions
async function submitFeedback(
  section: string,
  itemIndex: number,
  isAccurate: boolean
): Promise<void> {
  const feedbackKey = `${section}-${itemIndex}`

  // Prevent duplicate submissions
  if (feedbackSubmitted.value[feedbackKey]) {
    return
  }

  const contractId = analysesStore.currentAnalysis?.contract_id
  if (!contractId) {
    const { error } = useNotifications()
    error('Cannot submit feedback', 'Analysis data is missing')
    return
  }

  try {
    feedbackLoading.value[feedbackKey] = true

    const config = useRuntimeConfig()
    const response = await fetch(
      `${config.public.apiBase}/feedback`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authStore.token}`,
        },
        credentials: 'include',
        body: JSON.stringify({
          analysis_id: analysisId.value,
          contract_id: contractId,
          feedback_type: 'accuracy',
          section: section,
          item_index: itemIndex,
          is_accurate: isAccurate,
        }),
      }
    )

    if (!response.ok) {
      throw new Error('Failed to submit feedback')
    }

    feedbackSubmitted.value[feedbackKey] = true
    const { success } = useNotifications()
    success('Thank you!', 'Your feedback helps us improve our analysis.')
  } catch (error: any) {
    console.error('Failed to submit feedback:', error)
    const { error: showError } = useNotifications()
    showError('Feedback failed', 'Please try again later.')
  } finally {
    feedbackLoading.value[feedbackKey] = false
  }
}

// Lifecycle
onMounted(async () => {
  try {
    await analysesStore.fetchAnalysis(analysisId.value)
    if (analysesStore.isAnalyzing) {
      analysesStore.connectSSE(analysisId.value)
    }
  } catch (error) {
    console.error('Failed to load analysis:', error)
  }
})

onUnmounted(() => {
  analysesStore.disconnectSSE()
})

// Methods
function formatEventMessage(event: AnalysisEvent): string {
  if (event.payload?.message) {
    return event.payload.message
  }

  switch (event.kind) {
    case 'status_change':
      return event.payload?.status === 'running' ? 'Analysis started' : 'Status changed'
    case 'progress':
      return 'Processing...'
    case 'succeeded':
      return 'Analysis completed successfully!'
    case 'failed':
      return 'Analysis failed'
    case 'error':
      return 'An error occurred'
    default:
      return event.kind || 'Processing...'
  }
}

function handleExport(): void {
  showExportModal.value = true
}

async function handleExportFormat(format: 'pdf' | 'docx' | 'json' | 'lawyer-pack'): Promise<void> {
  try {
    const { success } = useNotifications()
    const metadata = {
      contractName: `Analysis ${analysisId.value}`,
      analysisDate: new Date(analysesStore.currentAnalysis?.created_at || '').toLocaleDateString(),
      confidenceScore: analysesStore.currentAnalysis?.confidence_score || undefined,
    }

    if (format === 'pdf') {
      await exportAnalysisToPDF({
        title: 'Contract Analysis',
        content: formattedOutput.value,
        metadata,
      })
      success('PDF exported successfully', 'Your analysis has been downloaded as a PDF.')
    } else if (format === 'docx') {
      await exportAnalysisToDOCX({
        title: 'Contract Analysis',
        content: formattedOutput.value,
        metadata,
      })
      success('DOCX exported successfully', 'Your analysis has been downloaded as a Word document.')
    } else if (format === 'lawyer-pack') {
      await exportLawyerPackToPDF({
        title: 'Lawyer Handoff Pack',
        content: formattedOutput.value,
        metadata,
        analysisData: {
          screening_result: screeningResult.value,
          preparation_result: analysesStore.currentAnalysis?.preparation_result,
          analysis_result: analysesStore.currentAnalysis?.analysis_result,
        },
      })
      success('Lawyer Pack exported!', 'Comprehensive report for legal counsel has been downloaded.')
    } else if (format === 'json') {
      const data = {
        analysisId: analysisId.value,
        metadata,
        analysis: analysesStore.currentAnalysis,
      }
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `analysis_${analysisId.value}.json`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      URL.revokeObjectURL(url)
      success('JSON exported successfully', 'Your analysis data has been downloaded.')
    }
  } catch (error) {
    console.error('Failed to export analysis:', error)
    const { error: showError } = useNotifications()
    showError('Export failed', 'Please try again later.')
  }
}

useHead({
  title: 'Analysis Results',
})
</script>
