# Phase 4: Backend-Frontend Integration Checklist

## Overview

This document tracks the integration of the Nuxt 3 frontend with the FastAPI backend. All frontend components are complete and ready for integration.

**Current Status**: Phase 3 Complete ✅ | Phase 4 Ready to Start

---

## API Endpoints Integration

### Authentication Endpoints

| Endpoint | Method | Frontend Component | Status | Notes |
|----------|--------|-------------------|--------|-------|
| `/api/auth/register` | POST | `stores/auth.ts` | ✅ DONE | Real API integration complete |
| `/api/auth/login` | POST | `stores/auth.ts` | ✅ DONE | Real API integration complete |
| `/api/auth/logout` | POST | `stores/auth.ts` | ✅ DONE | Real API integration complete |
| `/api/auth/me` | GET | `stores/auth.ts` | ✅ DONE | Real API integration complete |
| `/api/auth/forgot-password` | POST | `pages/auth/forgot-password.vue` | ✅ DONE | Send reset email |
| `/api/auth/reset-password` | POST | `pages/auth/reset-password.vue` | ✅ DONE | Reset with token from URL |
| `/api/auth/verify-email` | POST | `pages/auth/verify-email.vue` | ✅ DONE | Verify with token from URL |
| `/api/auth/resend-verification` | POST | `pages/auth/verify-email.vue` | ✅ DONE | Resend verification email |

### Contract Endpoints

| Endpoint | Method | Frontend Component | Status | Notes |
|----------|--------|-------------------|--------|-------|
| `/api/contracts/upload` | POST | `stores/contracts.ts` | ✅ DONE | Real API integration complete |
| `/api/contracts` | GET | `stores/contracts.ts` | ✅ DONE | Real API integration complete |
| `/api/contracts/{id}` | GET | `stores/contracts.ts` | ✅ DONE | Real API integration complete |
| `/api/contracts/{id}` | DELETE | `stores/contracts.ts` | ✅ DONE | Real API integration complete |
| `/api/contracts/{id}/analyze` | POST | `stores/contracts.ts` | ✅ DONE | Real API integration complete |

### Analysis Endpoints

| Endpoint | Method | Frontend Component | Status | Notes |
|----------|--------|-------------------|--------|-------|
| `/api/analyses/{id}` | GET | `stores/analyses.ts` | ✅ DONE | Real API integration complete |
| `/api/analyses/{id}/stream` | GET (SSE) | `stores/analyses.ts` | ✅ DONE | Real SSE integration complete |
| `/api/analyses/{id}/feedback` | POST | `stores/analyses.ts` | ✅ DONE | Real API integration complete |
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

#### 1. `stores/auth.ts` ✅ COMPLETE
**Location**: `/frontend/stores/auth.ts`

**Status**: Real API integration complete for all endpoints
```typescript
// Lines 51-75: async function login(credentials: LoginCredentials)
const response = await $fetch<AuthResponse>('/auth/login', {
  method: 'POST',
  body: credentials,
  baseURL: useRuntimeConfig().public.apiBase,
})

// Lines 77-101: async function register(data: RegisterData)
// Real API integration complete

// Lines 103-121: async function logout()
// Real API integration complete

// Lines 137-149: async function initializeAuth()
// Calls /auth/me to validate token - Real API integration complete
```

#### 2. `stores/contracts.ts` ✅ COMPLETE
**Location**: `/frontend/stores/contracts.ts`

**Status**: Real API integration complete for all endpoints
```typescript
// Lines 51-76: async function uploadContract(file: File)
const response = await $fetch<UploadResponse>('/contracts/upload', {
  method: 'POST',
  body: formData,
  baseURL: useRuntimeConfig().public.apiBase,
  headers: { Authorization: `Bearer ${token}` },
  onUploadProgress: (progressEvent) => { ... }
})

// Lines 93-117: async function fetchContracts()
// Real API integration complete

// Lines 133-153: async function deleteContract(id: string)
// Real API integration complete
```

#### 3. `stores/analyses.ts` ✅ COMPLETE
**Location**: `/frontend/stores/analyses.ts`

**Status**: Real API integration complete for SSE and all endpoints
```typescript
// Lines 79-107: function connectSSE(analysisId: string)
const baseURL = useRuntimeConfig().public.apiBase
const url = `${baseURL}/analyses/${analysisId}/stream`
const es = new EventSource(`${url}?token=${token}`)

// Lines 121-145: async function fetchAnalysis(id: string)
// Real API integration complete

// Lines 162-182: async function submitFeedback(...)
// Real API integration complete
```

#### 4. `pages/analysis/[id].vue` ⏳ PENDING
**Location**: `/frontend/pages/analysis/[id].vue`

**TODO Items**:
```typescript
// Export functionality still uses placeholder
// TODO: Replace exportToPDF mock with actual API call
// Call GET /api/analyses/{id}/export/pdf or /api/analyses/{id}/export/docx
```

### Medium Priority (Auth Flows)

#### 5. `pages/auth/forgot-password.vue` ✅ COMPLETE (Frontend + Backend)
**Location**: `/frontend/pages/auth/forgot-password.vue`

**Frontend Status**: Real API integration complete
```typescript
// Line 167-172: async function handleSubmit()
await $fetch('/auth/forgot-password', {
  method: 'POST',
  body: { email: email.value },
  baseURL: useRuntimeConfig().public.apiBase,
})
```

**Backend Status**: Endpoint implemented in `backend/app/api/auth.py` (lines 175-211)
- Validates email, generates 1-hour reset token, sends email via SendGrid
- Prevents email enumeration by always returning success

#### 6. `pages/auth/reset-password.vue` ✅ COMPLETE (Frontend + Backend)
**Location**: `/frontend/pages/auth/reset-password.vue`

**Frontend Status**: Real API integration complete
```typescript
// Line 209-217: async function handleSubmit()
await $fetch('/auth/reset-password', {
  method: 'POST',
  body: {
    token: token.value,
    password: password.value,
  },
  baseURL: useRuntimeConfig().public.apiBase,
})
```

**Backend Status**: Endpoint implemented in `backend/app/api/auth.py` (lines 214-265)
- Verifies token, validates user, updates password with bcrypt hash

#### 7. `pages/auth/verify-email.vue` ✅ COMPLETE (Frontend + Backend)
**Location**: `/frontend/pages/auth/verify-email.vue`

**Frontend Status**: Real API integration complete
```typescript
// Line 183-188: async function verifyEmail()
await $fetch('/auth/verify-email', {
  method: 'POST',
  body: { token: token.value },
  baseURL: useRuntimeConfig().public.apiBase,
})

// Line 210-214: async function resendVerification()
await $fetch('/auth/resend-verification', {
  method: 'POST',
  baseURL: useRuntimeConfig().public.apiBase,
})
```

**Backend Status**: Both endpoints implemented in `backend/app/api/auth.py`
- /verify-email (lines 268-312): Verifies token, sets user.is_verified = True
- /resend-verification (lines 314-345): Requires auth, sends new 24-hour token

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
