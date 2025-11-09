# Phase 4: Backend-Frontend Integration Checklist

## Overview

This document tracks the integration of the Nuxt 3 frontend with the FastAPI backend. All frontend components are complete and ready for integration.

**Current Status**: Phase 3 Complete ✅ | Phase 4 Ready to Start

---

## API Endpoints Integration

### Authentication Endpoints

| Endpoint | Method | Frontend Component | Status | Notes |
|----------|--------|-------------------|--------|-------|
| `/api/auth/register` | POST | `pages/register.vue` | ⏳ TODO | Replace placeholder with actual API call |
| `/api/auth/login` | POST | `pages/login.vue` | ⏳ TODO | Replace placeholder with actual API call |
| `/api/auth/logout` | POST | `stores/auth.ts` | ⏳ TODO | Clear session, redirect to login |
| `/api/auth/me` | GET | `plugins/auth.client.ts` | ⏳ TODO | Load user on app init |
| `/api/auth/forgot-password` | POST | `pages/auth/forgot-password.vue` | ⏳ TODO | Send reset email |
| `/api/auth/reset-password` | POST | `pages/auth/reset-password.vue` | ⏳ TODO | Reset with token from URL |
| `/api/auth/verify-email` | POST | `pages/auth/verify-email.vue` | ⏳ TODO | Verify with token from URL |
| `/api/auth/resend-verification` | POST | `pages/auth/verify-email.vue` | ⏳ TODO | Resend verification email |

### Contract Endpoints

| Endpoint | Method | Frontend Component | Status | Notes |
|----------|--------|-------------------|--------|-------|
| `/api/contracts/upload` | POST | `stores/contracts.ts` | ⏳ TODO | File upload with FormData, progress tracking |
| `/api/contracts` | GET | `pages/history.vue` | ⏳ TODO | List user's contracts with pagination |
| `/api/contracts/{id}` | GET | `pages/history.vue` | ⏳ TODO | Get contract details |
| `/api/contracts/{id}` | DELETE | `pages/history.vue` | ⏳ TODO | Delete contract (soft delete) |
| `/api/contracts/{id}/analyze` | POST | `stores/contracts.ts` | ⏳ TODO | Trigger analysis, returns task_id |

### Analysis Endpoints

| Endpoint | Method | Frontend Component | Status | Notes |
|----------|--------|-------------------|--------|-------|
| `/api/analyses/{id}` | GET | `pages/analysis/[id].vue` | ⏳ TODO | Get analysis results |
| `/api/analyses/{id}/stream` | GET (SSE) | `stores/analyses.ts` | ⏳ TODO | Real-time progress updates |
| `/api/analyses/{id}/feedback` | POST | `pages/analysis/[id].vue` | ⏳ TODO | Submit user feedback on section |
| `/api/analyses/{id}/export/pdf` | GET | `pages/analysis/[id].vue` | ⏳ TODO | Export results as PDF |
| `/api/analyses/{id}/export/docx` | GET | `pages/analysis/[id].vue` | ⏳ TODO | Export results as DOCX |

### Account Endpoints

| Endpoint | Method | Frontend Component | Status | Notes |
|----------|--------|-------------------|--------|-------|
| `/api/account` | GET | `pages/account.vue` | ⏳ TODO | Get account details, usage stats |
| `/api/account` | PATCH | `pages/account.vue` | ⏳ TODO | Update profile settings |
| `/api/account/export` | GET | `pages/account.vue` | ⏳ TODO | GDPR data export |
| `/api/account` | DELETE | `pages/account.vue` | ⏳ TODO | GDPR account deletion |

---

## Frontend Files Needing Updates

### High Priority (Core Functionality)

#### 1. `stores/auth.ts`
**Location**: `/frontend/stores/auth.ts`

**TODO Items**:
```typescript
// Line ~35: async function login(credentials: LoginCredentials)
// TODO: Replace mock with actual API call
await $fetch('/auth/login', {
  method: 'POST',
  body: credentials,
  baseURL: useRuntimeConfig().public.apiBase,
})

// Line ~55: async function register(data: RegisterData)
// TODO: Replace mock with actual API call

// Line ~75: async function logout()
// TODO: Call /auth/logout endpoint

// Line ~95: async function checkAuth()
// TODO: Call /auth/me to validate token
```

#### 2. `stores/contracts.ts`
**Location**: `/frontend/stores/contracts.ts`

**TODO Items**:
```typescript
// Line ~40: async function uploadContract(file: File)
// TODO: Replace FormData upload mock with actual API
// IMPORTANT: Include Authorization header with JWT token

// Line ~65: async function fetchContracts()
// TODO: Fetch user's contract list from /api/contracts

// Line ~85: async function deleteContract(id: string)
// TODO: Call DELETE /api/contracts/{id}
```

#### 3. `stores/analyses.ts`
**Location**: `/frontend/stores/analyses.ts`

**TODO Items**:
```typescript
// Line ~50: function connectSSE(analysisId: string)
// TODO: Update SSE URL to actual backend endpoint
// Example: const url = `${baseURL}/analyses/${analysisId}/stream?token=${token}`

// Line ~90: async function fetchAnalysis(id: string)
// TODO: Fetch analysis results from /api/analyses/{id}

// Line ~110: async function submitFeedback(...)
// TODO: POST feedback to /api/analyses/{id}/feedback
```

#### 4. `pages/analysis/[id].vue`
**Location**: `/frontend/pages/analysis/[id].vue`

**TODO Items**:
```typescript
// Line ~120: async function handleExport()
// TODO: Replace exportToPDF mock with actual API call
// Call GET /api/analyses/{id}/export/pdf

// Line ~140: async function handleFeedback(data)
// TODO: Ensure feedback submission is connected to API
```

### Medium Priority (Auth Flows)

#### 5. `pages/auth/forgot-password.vue`
**Location**: `/frontend/pages/auth/forgot-password.vue`

**TODO Items**:
```typescript
// Line ~45: async function handleSubmit()
// TODO: Call POST /api/auth/forgot-password
await $fetch('/auth/forgot-password', {
  method: 'POST',
  body: { email: email.value },
  baseURL: useRuntimeConfig().public.apiBase,
})
```

#### 6. `pages/auth/reset-password.vue`
**Location**: `/frontend/pages/auth/reset-password.vue`

**TODO Items**:
```typescript
// Line ~60: async function handleSubmit()
// TODO: Call POST /api/auth/reset-password
await $fetch('/auth/reset-password', {
  method: 'POST',
  body: {
    token: token.value,
    new_password: password.value,
  },
  baseURL: useRuntimeConfig().public.apiBase,
})
```

#### 7. `pages/auth/verify-email.vue`
**Location**: `/frontend/pages/auth/verify-email.vue`

**TODO Items**:
```typescript
// Line ~50: async function verifyEmail()
// TODO: Call POST /api/auth/verify-email
await $fetch('/auth/verify-email', {
  method: 'POST',
  body: { token: token.value },
  baseURL: useRuntimeConfig().public.apiBase,
})

// Line ~70: async function resendVerification()
// TODO: Call POST /api/auth/resend-verification
```

### Low Priority (Enhancements)

#### 8. `utils/exportToPDF.ts`
**Location**: `/frontend/utils/exportToPDF.ts`

**TODO Items**:
```typescript
// Replace .txt export with actual PDF generation using jsPDF or pdfmake
// Option 1: Use jsPDF for client-side PDF generation
// Option 2: Call backend endpoint for server-side PDF generation (recommended)
```

#### 9. `plugins/analytics.client.ts`
**Location**: `/frontend/plugins/analytics.client.ts`

**TODO Items**:
```typescript
// Add actual analytics service integration
// Options: Google Analytics 4, Plausible, PostHog
// Check runtime config: useRuntimeConfig().public.enableAnalytics
```

---

## Testing Checklist

### Unit Tests (Vitest)

- [ ] `stores/auth.ts` - Test login, register, logout flows
- [ ] `stores/contracts.ts` - Test upload, fetch, delete
- [ ] `stores/analyses.ts` - Test SSE connection, fetch, feedback
- [ ] `composables/useDarkMode.ts` - Test theme toggle
- [ ] `composables/useNotifications.ts` - Test notification system

**Command**: `npm run test`

### E2E Tests (Playwright)

- [ ] User registration flow
- [ ] User login flow
- [ ] Password reset flow
- [ ] Email verification flow
- [ ] Contract upload flow
- [ ] Analysis results page (wait for SSE completion)
- [ ] History page navigation
- [ ] Account settings update
- [ ] Dark mode toggle
- [ ] Language switcher

**Command**: `npm run test:e2e`

### Accessibility Tests (Lighthouse CI)

- [ ] Landing page (score >90)
- [ ] Login page (score >90)
- [ ] Upload page (score >90)
- [ ] Analysis page (score >90)
- [ ] History page (score >90)
- [ ] Account page (score >90)
- [ ] All pages meet WCAG 2.1 AA

**Command**: `npm run test:a11y`

### Manual Testing

#### Authentication Flow
- [ ] Register new account with email/password
- [ ] Verify email validation on registration form
- [ ] Login with valid credentials
- [ ] Login with invalid credentials (show error)
- [ ] Logout successfully
- [ ] Request password reset email
- [ ] Reset password with token
- [ ] Verify email with token
- [ ] Resend verification email

#### Contract Upload & Analysis
- [ ] Upload PDF file (<10MB)
- [ ] Upload DOCX file (<10MB)
- [ ] Reject files >10MB (show error)
- [ ] Reject invalid file types (show error)
- [ ] See upload progress bar
- [ ] Trigger analysis on upload
- [ ] Receive real-time SSE updates
- [ ] See progress timeline update
- [ ] View completed analysis results
- [ ] Export analysis as PDF
- [ ] Submit feedback on analysis sections

#### History & Navigation
- [ ] View list of past analyses
- [ ] Click analysis to view details
- [ ] Delete analysis (confirm modal)
- [ ] Pagination works (if >10 results)
- [ ] Search/filter analyses (if implemented)

#### Account Settings
- [ ] View current profile info
- [ ] Update email address
- [ ] Update password
- [ ] View usage statistics
- [ ] Request GDPR data export
- [ ] Delete account (confirm modal)

#### UI & UX
- [ ] Dark mode toggle works
- [ ] Theme persists on page reload
- [ ] Language switcher works (EN, RU, FR, SR)
- [ ] Locale persists on page reload
- [ ] Notifications appear and dismiss
- [ ] Loading skeletons show during data fetch
- [ ] Mobile responsive (test on 320px, 768px, 1024px)
- [ ] Touch targets ≥44px on mobile
- [ ] Keyboard navigation works
- [ ] Focus indicators visible

#### PWA
- [ ] App installable on desktop (Chrome, Edge)
- [ ] App installable on mobile (iOS Safari, Android Chrome)
- [ ] Offline shell loads when no internet
- [ ] Service worker caches API responses
- [ ] Service worker caches images
- [ ] App updates automatically on new version

---

## Performance Optimization

### Bundle Analysis

```bash
# Analyze bundle size
npm run build
npx nuxt analyze
```

**Targets**:
- [ ] Main bundle <250KB gzipped
- [ ] Each route chunk <100KB gzipped
- [ ] Total bundle <500KB gzipped

### Lighthouse Performance

```bash
npm run build
npm run preview
# Open Chrome DevTools > Lighthouse > Run audit
```

**Targets**:
- [ ] Performance score >90
- [ ] First Contentful Paint <1.5s
- [ ] Time to Interactive <3s
- [ ] Largest Contentful Paint <2.5s
- [ ] Cumulative Layout Shift <0.1

### Image Optimization

- [ ] All images lazy loaded
- [ ] Images use modern formats (WebP, AVIF)
- [ ] PWA icons optimized (192x192, 512x512)
- [ ] No unused images in bundle

---

## Security Review

### Frontend Security

- [ ] No API keys in frontend code
- [ ] JWT token stored securely (httpOnly cookie or secure localStorage)
- [ ] CSRF protection enabled
- [ ] XSS prevention (Vue auto-escapes by default)
- [ ] Input validation on all forms
- [ ] File upload size/type validation
- [ ] No sensitive data in console logs (production mode)
- [ ] Content Security Policy headers set

### API Integration Security

- [ ] All API calls use HTTPS (production)
- [ ] Authorization header includes JWT token
- [ ] Token refresh on expiration
- [ ] Logout clears all tokens
- [ ] Rate limiting respected (frontend shows error if 429)
- [ ] Error messages don't leak sensitive info

---

## Environment Variables

### Development

```bash
# frontend/.env.development
NUXT_PUBLIC_API_BASE=http://localhost:8000/api
NUXT_PUBLIC_ENABLE_ANALYTICS=false
```

### Production

```bash
# Vercel environment variables
NUXT_PUBLIC_API_BASE=https://api.legallyai.com/api
NUXT_PUBLIC_ENABLE_ANALYTICS=true
```

**Setup**:
- [ ] Create `.env.development` file
- [ ] Configure Vercel environment variables
- [ ] Test with production API URL

---

## Deployment Checklist

### Pre-Deployment

- [ ] All tests passing (unit, E2E, accessibility)
- [ ] Bundle size within targets
- [ ] Lighthouse scores >90
- [ ] PWA icons generated
- [ ] Environment variables configured
- [ ] API integration complete and tested
- [ ] Error handling tested (network failures, API errors)
- [ ] Loading states verified

### Vercel Deployment

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy to preview
vercel

# Deploy to production
vercel --prod
```

**Steps**:
- [ ] Link Vercel project to GitHub repo
- [ ] Configure build settings (nuxt build)
- [ ] Set environment variables in Vercel dashboard
- [ ] Enable preview deployments for PRs
- [ ] Configure custom domain (if applicable)
- [ ] Test preview deployment
- [ ] Deploy to production

### Post-Deployment

- [ ] Verify all pages load correctly
- [ ] Test authentication flow on production
- [ ] Test file upload on production
- [ ] Verify SSE connection works
- [ ] Test PWA installation
- [ ] Check error tracking (Sentry, if configured)
- [ ] Monitor performance metrics
- [ ] Test on real mobile devices

---

## Integration Timeline

### Week 1: Core Integration (High Priority)
- Day 1-2: Authentication endpoints (login, register, logout)
- Day 3-4: Contract upload and analysis trigger
- Day 5-6: SSE real-time updates
- Day 7: Testing and bug fixes

### Week 2: Complete Integration (Medium Priority)
- Day 1-2: Auth flows (password reset, email verification)
- Day 3-4: Export functionality (PDF/DOCX)
- Day 5-6: Account settings endpoints
- Day 7: Testing and bug fixes

### Week 3: Polish & Testing (Low Priority)
- Day 1-2: Analytics integration
- Day 3-4: E2E tests
- Day 5-6: Performance optimization
- Day 7: Final QA and deployment prep

---

## Known Issues & Blockers

### Current Blockers
- [ ] Backend API not deployed/accessible
- [ ] No test API credentials
- [ ] CORS not configured on backend

### Open Questions
- [ ] What is the production API base URL?
- [ ] Is backend deployed to staging environment?
- [ ] Are backend endpoints matching frontend expectations?
- [ ] Is SSE endpoint tested and working?
- [ ] Is file upload size limit enforced on backend?

---

## Success Criteria

**Phase 4 is complete when**:
- ✅ All API endpoints integrated and tested
- ✅ All tests passing (unit, E2E, accessibility)
- ✅ Performance targets met (Lighthouse >90)
- ✅ PWA fully functional (installable, offline support)
- ✅ Deployed to production and verified
- ✅ Zero critical bugs
- ✅ Ready for Phase 5 (Payments & Polish)

---

**Last Updated**: 2025-11-09
**Phase**: 4 - Integration (Ready to Start)
**Next Steps**: Begin with authentication endpoint integration
