# Legally AI - Comprehensive Development Plan

## Executive Summary

**Vision**: Build a multilingual (Russian, Serbian, French, English) contract analysis web application that makes legal agreements understandable for everyone.

**Approach**: Prototype on Hugging Face Spaces (free) → Get lawyer feedback → Build production MVP (<$50/month)

**Timeline**: 8 weeks (1 week prototype + 1 week feedback + 6 weeks MVP)

**Target Market**: Individuals and small businesses dealing with foreign-language contracts

---

## Phase 0: HF Spaces Prototype (Week 1)

### Objective
Create a working prototype to validate accuracy and usefulness with a real lawyer who works with Russian/Serbian/French contracts.

### Tech Stack
- **UI**: Gradio 4.x
- **Backend**: Python 3.11 (same process)
- **LLM**: Groq API (free tier) - llama-3.3-70b-versatile
- **Parsers**: pdfplumber, python-docx, textract
- **Language Detection**: langdetect
- **Hosting**: Hugging Face Spaces (free CPU)

### Features

#### Core Analysis
- [x] Upload PDF or DOCX
- [x] Auto-detect language (Russian, Serbian, French, English)
- [x] User selects output language
- [x] Step 1: Preparation analysis
  - File classification
  - Text normalization
  - Governing language check
  - Coverage discovery
  - Quality scoring (0-1)
  - Version detection
  - Agreement type classification
  - User role identification
  - Negotiability assessment
- [x] Step 2: Text analysis
  - Structure mapping
  - Core field extraction
  - Obligations extraction (with quotes ≤12 words)
  - Rights extraction (with quotes ≤12 words)
  - Risk detection and scoring
  - Calendar building (deadlines, renewals)
  - Screening result

#### Output Sections (Per Spec)
- [x] Summary
  - Screening result (4 variants)
  - Important limits disclaimer
  - Confidence level
- [x] About the contract
- [x] What you pay and when
- [x] What you agree to do
- [x] Check these terms
- [x] Also think about
- [x] Ask for these changes (if negotiable)
- [x] If you decide to sign "As Is"
- [x] Act now (action buttons)
- [x] All key terms (collapsed)

#### Multilingual Features
- [x] Side-by-side view: original language + translation
- [x] Key quotes in both languages
- [x] Jurisdiction-specific context
- [x] Legal term glossary
- [x] Translation quality notes

### File Structure

```
legally-ai-prototype/
├── app.py                          # Main Gradio application
├── requirements.txt
├── README.md
├── .env.example
├── src/
│   ├── __init__.py
│   ├── parsers.py                  # PDF/DOCX extraction
│   ├── language.py                 # Detection, translation
│   ├── quality.py                  # Confidence scoring
│   ├── step1_preparation.py        # Preparation analysis
│   ├── step2_analysis.py           # Text analysis
│   ├── formatter.py                # Output formatting
│   ├── llm_router.py               # LLM provider abstraction
│   └── constants.py                # UI strings per language
├── prompts/
│   ├── preparation_en.txt
│   ├── preparation_ru.txt
│   ├── preparation_sr.txt
│   ├── preparation_fr.txt
│   ├── analysis_en.txt
│   ├── analysis_ru.txt
│   ├── analysis_sr.txt
│   ├── analysis_fr.txt
│   ├── lease_en.txt                # Type-specific prompts
│   ├── lease_ru.txt
│   ├── nda_en.txt
│   └── ...
└── tests/
    └── test_contracts/              # Sample contracts for testing
```

### Development Schedule

**Days 1-2: Foundation**
- [x] Create HF Space repository
- [ ] Set up Groq API integration
- [ ] Implement document parsers
- [ ] Implement language detection
- [ ] Create basic LLM router

**Days 3-4: Analysis Logic**
- [ ] Implement Step 1 (Preparation)
- [ ] Implement Step 2 (Analysis)
- [ ] Create prompts for all 4 languages
- [ ] Add jurisdiction-specific context

**Days 5-6: Multilingual & UI**
- [ ] Translation functions
- [ ] Side-by-side view
- [ ] Legal term glossary
- [ ] Gradio interface
- [ ] All output sections

**Day 7: Polish & Deploy**
- [ ] Testing with sample contracts
- [ ] Error handling
- [ ] Loading states
- [ ] Deploy to HF Spaces
- [ ] Share with lawyer

### Success Criteria
- [ ] Analyzes contracts in all 4 languages
- [ ] Output follows spec exactly
- [ ] Confidence scoring works correctly
- [ ] Lawyer can provide meaningful feedback
- [ ] No critical bugs

---

## Phase 1: Lawyer Feedback & Iteration (Week 2)

### Objective
Get real-world validation from lawyer testing with actual contracts.

### Feedback Framework

#### Accuracy Checklist
- [ ] Agreement type correctly identified?
- [ ] All key dates extracted accurately?
- [ ] All monetary amounts correct?
- [ ] Parties identified correctly?
- [ ] User role identified correctly?
- [ ] Governing law/jurisdiction correct?

#### Completeness Checklist
- [ ] All major obligations listed?
- [ ] All user rights captured?
- [ ] Critical risks flagged?
- [ ] Important deadlines noted?
- [ ] Missing annexes detected?

#### Risk Assessment Quality
- [ ] High-risk items correctly prioritized?
- [ ] False positives (non-risky items flagged)?
- [ ] False negatives (risky items missed)?
- [ ] Risk wording clear and actionable?

#### Multilingual Quality
- [ ] Legal terms translated correctly?
- [ ] Cultural context preserved?
- [ ] Jurisdiction-specific issues noted?
- [ ] Translation quality acceptable?

#### Usability
- [ ] Output easy to understand?
- [ ] Actions clear and helpful?
- [ ] Layout intuitive?
- [ ] What's missing?
- [ ] What's confusing?

### Iteration Tasks
- [ ] Fix accuracy issues identified
- [ ] Add missing features requested
- [ ] Refine prompts based on feedback
- [ ] Improve risk detection
- [ ] Enhance multilingual handling
- [ ] Update UI based on usability feedback

### Deliverable
- Validated prototype
- Feedback report document
- List of MVP priorities

---

## Phase 2: MVP Backend (Week 3)

### Objective
Build production-ready backend with authentication, database, and async processing.

### Tech Stack
- **Framework**: FastAPI 0.110+
- **Database**: PostgreSQL 16
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic
- **Auth**: FastAPI-Users + JWT
- **Jobs**: Celery 5.x
- **Queue**: Redis 7.x
- **LLM**: Groq API (with fallback providers)
- **Storage**: Fly.io volumes (for files)

### Database Schema

```sql
-- Users
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    tier TEXT NOT NULL DEFAULT 'free',  -- 'free' | 'premium'
    contracts_analyzed INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    stripe_customer_id TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE
);

-- Contracts
CREATE TABLE contracts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    filename TEXT NOT NULL,
    mime_type TEXT NOT NULL,
    file_size_bytes INTEGER,
    file_path TEXT NOT NULL,
    pages INTEGER,
    detected_language TEXT,  -- 'russian' | 'serbian' | 'french' | 'english'
    quality_score FLOAT,
    coverage_score FLOAT,
    confidence_level TEXT,  -- 'High' | 'Medium' | 'Low'
    confidence_reason TEXT,
    status TEXT DEFAULT 'uploaded',  -- 'uploaded' | 'analyzing' | 'completed' | 'failed'
    created_at TIMESTAMPTZ DEFAULT NOW(),
    INDEX idx_user_created (user_id, created_at DESC)
);

-- Analyses
CREATE TABLE analyses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    contract_id UUID REFERENCES contracts(id) ON DELETE CASCADE,
    step1_data JSONB,
    step2_data JSONB,
    formatted_output JSONB,
    model_used TEXT,
    tokens_used INTEGER,
    cost_cents INTEGER,
    confidence_score FLOAT,
    status TEXT DEFAULT 'queued',  -- 'queued' | 'running' | 'succeeded' | 'failed'
    error_message TEXT,
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Events (audit log)
CREATE TABLE events (
    id BIGSERIAL PRIMARY KEY,
    analysis_id UUID REFERENCES analyses(id) ON DELETE CASCADE,
    kind TEXT NOT NULL,  -- 'parsing' | 'preparation' | 'analysis' | 'formatting'
    payload JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    INDEX idx_analysis_created (analysis_id, created_at)
);

-- Subscriptions
CREATE TABLE subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    stripe_subscription_id TEXT UNIQUE,
    status TEXT,  -- 'active' | 'canceled' | 'past_due' | 'trialing'
    current_period_start TIMESTAMPTZ,
    current_period_end TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Feedback (for confidence calibration)
CREATE TABLE feedback (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    analysis_id UUID REFERENCES analyses(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    section TEXT NOT NULL,  -- Which section the feedback is about
    is_correct BOOLEAN,
    comment TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Deadlines (from Deadline Radar feature)
CREATE TABLE deadlines (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    contract_id UUID REFERENCES contracts(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    type TEXT NOT NULL,  -- 'renewal' | 'notice' | 'payment' | 'termination'
    title TEXT NOT NULL,
    description TEXT,
    deadline_date DATE,
    deadline_formula TEXT,  -- For recurring deadlines
    is_recurring BOOLEAN DEFAULT FALSE,
    reminder_sent BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    INDEX idx_user_deadline (user_id, deadline_date)
);

-- Document Sets (for Cross-Document Consistency Check)
CREATE TABLE document_sets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    primary_contract_id UUID REFERENCES contracts(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE document_set_members (
    document_set_id UUID REFERENCES document_sets(id) ON DELETE CASCADE,
    contract_id UUID REFERENCES contracts(id) ON DELETE CASCADE,
    role TEXT NOT NULL,  -- 'primary' | 'context' | 'exhibit'
    PRIMARY KEY (document_set_id, contract_id)
);

-- Conflicts (from Cross-Document Consistency Check)
CREATE TABLE conflicts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_set_id UUID REFERENCES document_sets(id) ON DELETE CASCADE,
    contract_id_1 UUID REFERENCES contracts(id),
    contract_id_2 UUID REFERENCES contracts(id),
    severity TEXT,  -- 'critical' | 'high' | 'medium' | 'low'
    category TEXT,  -- 'term_conflict' | 'missing_exhibit' | 'override' | 'inconsistency'
    description TEXT NOT NULL,
    source_of_truth_id UUID REFERENCES contracts(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### API Endpoints

```python
# Authentication
POST   /api/auth/register
POST   /api/auth/login
POST   /api/auth/logout
GET    /api/auth/me
POST   /api/auth/forgot-password
POST   /api/auth/reset-password

# Contracts
POST   /api/contracts/upload
GET    /api/contracts
GET    /api/contracts/{id}
DELETE /api/contracts/{id}
POST   /api/contracts/{id}/analyze
GET    /api/contracts/{id}/download

# Analyses
GET    /api/analyses/{id}
GET    /api/analyses/{id}/stream  # SSE for progress
POST   /api/analyses/{id}/feedback

# Document Sets (Cross-Document)
POST   /api/document-sets
GET    /api/document-sets/{id}
POST   /api/document-sets/{id}/contracts
GET    /api/document-sets/{id}/conflicts

# Deadlines (Deadline Radar)
GET    /api/deadlines
GET    /api/deadlines/upcoming
POST   /api/deadlines/{id}/remind

# Comparison
POST   /api/compare
GET    /api/compare/{id}

# Exports
GET    /api/analyses/{id}/export/pdf
GET    /api/analyses/{id}/export/docx
POST   /api/analyses/{id}/export/email
GET    /api/analyses/{id}/lawyer-handoff

# Billing
POST   /api/billing/create-checkout
GET    /api/billing/portal
POST   /api/webhooks/stripe

# Account
GET    /api/account
PATCH  /api/account
GET    /api/account/export  # GDPR data export
DELETE /api/account  # GDPR account deletion
```

### Tasks

- [ ] FastAPI project structure
- [ ] PostgreSQL connection
- [ ] SQLAlchemy models
- [ ] Alembic migrations
- [ ] User authentication (register, login, JWT)
- [ ] File upload endpoint
- [ ] Celery worker setup
- [ ] Redis connection
- [ ] Analysis task (async)
- [ ] SSE endpoint for progress
- [ ] LLM router implementation
- [ ] Trial limit enforcement
- [ ] Error handling & logging
- [ ] API documentation (automatic with FastAPI)

---

## Phase 3: MVP Frontend (Week 4)

### Objective
Build mobile-first, PWA-capable frontend with delightful UX.

### Tech Stack
- **Framework**: Nuxt 3
- **UI**: Tailwind CSS + Headless UI
- **State**: Pinia
- **Auth**: @sidebase/nuxt-auth
- **PWA**: @vite-pwa/nuxt
- **Forms**: VeeValidate + Zod
- **Charts**: Chart.js (for deadline timeline)
- **PDF Viewer**: Vue-PDF-Embed

### Pages

```
pages/
├── index.vue                    # Landing page
├── login.vue
├── register.vue
├── forgot-password.vue
├── upload.vue                   # Upload contract(s)
├── analysis/
│   └── [id].vue                 # Analysis results
├── history.vue                  # Past analyses
├── deadlines.vue                # Deadline Radar
├── document-sets/
│   ├── index.vue                # List document sets
│   └── [id].vue                 # Document set details + conflicts
├── compare/
│   └── [id].vue                 # Comparison view
├── account/
│   ├── index.vue                # Account settings
│   ├── subscription.vue         # Manage subscription
│   ├── export.vue               # GDPR data export
│   └── delete.vue               # GDPR account deletion
└── pricing.vue                  # Pricing plans
```

### Components

```
components/
├── layout/
│   ├── Header.vue
│   ├── Footer.vue
│   ├── Sidebar.vue
│   └── MobileNav.vue
├── upload/
│   ├── UploadBox.vue
│   ├── FileList.vue
│   └── UploadProgress.vue
├── analysis/
│   ├── ResultBadge.vue          # 4 screening variants
│   ├── ImportantLimits.vue      # Disclaimer
│   ├── ConfidenceNote.vue
│   ├── SectionCard.vue
│   ├── MoreButton.vue           # "Helpful, what else?"
│   ├── KeyTermsAccordion.vue
│   ├── ObligationCard.vue
│   ├── RightCard.vue
│   ├── RiskCard.vue
│   ├── RedFlagAlert.vue         # Prominent warnings
│   ├── ActionButton.vue
│   └── ELI5Toggle.vue           # "Explain like I'm 5" mode
├── multilingual/
│   ├── LanguageSelector.vue
│   ├── MirrorView.vue           # Side-by-side translation
│   ├── TranslationToggle.vue
│   └── GlossaryPopover.vue
├── deadlines/
│   ├── DeadlineCard.vue
│   ├── DeadlineTimeline.vue
│   ├── ReminderSettings.vue
│   └── CalendarExport.vue
├── document-sets/
│   ├── DocumentSetCard.vue
│   ├── ConflictCard.vue
│   ├── SourceOfTruthBadge.vue
│   └── AddDocumentModal.vue
├── comparison/
│   ├── ComparisonTable.vue
│   ├── DiffHighlight.vue
│   └── RecommendationCard.vue
├── export/
│   ├── ExportOptions.vue
│   ├── LawyerHandoffPreview.vue
│   └── EmailForm.vue
├── feedback/
│   └── FeedbackForm.vue         # Confidence calibration
├── billing/
│   ├── PricingCard.vue
│   ├── UpgradeModal.vue
│   └── UsageStats.vue
└── common/
    ├── Button.vue
    ├── Input.vue
    ├── Select.vue
    ├── Checkbox.vue
    ├── Modal.vue
    ├── Toast.vue
    ├── Skeleton.vue
    └── ProgressBar.vue
```

### Stores

```typescript
// stores/auth.ts
export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: null,
  }),
  actions: {
    async login(email, password),
    async register(email, password),
    async logout(),
    async fetchUser(),
  },
});

// stores/upload.ts
export const useUploadStore = defineStore('upload', {
  state: () => ({
    files: [],
    uploadProgress: {},
  }),
  actions: {
    async uploadFile(file),
    async uploadMultiple(files),
    removeFile(index),
  },
});

// stores/analysis.ts
export const useAnalysisStore = defineStore('analysis', {
  state: () => ({
    current: null,
    history: [],
    progress: 0,
    status: 'idle',
  }),
  actions: {
    async startAnalysis(contractId),
    connectSSE(analysisId),
    async fetchAnalysis(id),
    async fetchHistory(),
  },
});

// stores/deadlines.ts
export const useDeadlineStore = defineStore('deadlines', {
  state: () => ({
    deadlines: [],
    upcoming: [],
  }),
  actions: {
    async fetchDeadlines(),
    async fetchUpcoming(),
    async setReminder(deadlineId),
  },
});

// stores/documentSets.ts
export const useDocumentSetStore = defineStore('documentSets', {
  state: () => ({
    sets: [],
    current: null,
    conflicts: [],
  }),
  actions: {
    async createSet(name, contracts),
    async fetchSets(),
    async fetchConflicts(setId),
  },
});
```

### Tasks

- [x] Nuxt 3 project setup
- [x] Tailwind CSS configuration
- [x] PWA configuration (Workbox with offline caching)
- [x] Authentication flow (login, register, forgot password, email verification)
- [x] Landing page
- [x] Upload page (single + multiple file support)
- [x] Analysis results page (all sections with real-time SSE)
- [x] History page
- [x] Account settings page
- [x] Mobile-responsive layouts (WCAG 2.1 AA compliant)
- [x] Dark mode support (with theme persistence)
- [x] Loading states & skeletons
- [x] Error handling & toasts (global notification system)
- [x] Multi-language support (EN, RU, FR, SR)
- [x] Analytics tracking plugin
- [x] PDF export functionality
- [ ] Deadlines page (pending backend integration)
- [ ] Document sets pages (pending backend integration)
- [ ] Comparison page (pending backend integration)
- [ ] Pricing page (pending Stripe integration)

---

## Phase 4: Integration & Features (Week 5)

### Objective
Connect frontend to backend, implement advanced features.

### Tasks

#### Basic Integration
- [ ] API client setup (axios)
- [ ] Auth token management
- [ ] SSE connection for analysis progress
- [ ] File upload with progress bar
- [ ] Error handling & retry logic

#### Trial System
- [ ] Enforce 3-contract limit
- [ ] Show usage stats (X of 3 used)
- [ ] Upgrade prompts after 3rd contract
- [ ] Grace period handling

#### Renewal & Deadline Radar
- [ ] Extract deadlines from analysis
- [ ] Store in database
- [ ] Display timeline view
- [ ] Upcoming deadlines dashboard
- [ ] Calendar export (.ics file)
- [ ] Email reminders (optional for MVP)

#### Cross-Document Consistency Check
- [ ] Upload multiple documents
- [ ] Create document set
- [ ] Detect conflicts between documents
- [ ] Categorize conflicts (critical/high/medium/low)
- [ ] Show "source of truth" for each term
- [ ] Flag missing exhibits
- [ ] Detect overrides

#### Lawyer Handoff Pack
- [ ] Generate summary
- [ ] Extract key fields into table
- [ ] Highlight important sections
- [ ] List open questions
- [ ] Generate redline suggestions
- [ ] Export as formatted PDF
- [ ] Email to lawyer function

#### Privacy "Do-Not-Store" Mode
- [ ] Toggle in upload page
- [ ] Skip database storage
- [ ] In-memory processing only
- [ ] Scrub text after analysis
- [ ] Redact PII in exports
- [ ] Show data retention badge
- [ ] Clear session data after download

#### Multilingual Mirror View
- [ ] Side-by-side layout
- [ ] Sentence alignment
- [ ] Highlight differences
- [ ] Sync scrolling
- [ ] Switch between languages
- [ ] Show original legal terms

#### Contract Type Detection Training
- [ ] Load type-specific prompts
- [ ] Train on contract type patterns
- [ ] Improve classification accuracy
- [ ] Add more contract types (TBD)

#### "Explain Like I'm 5" Mode
- [ ] Toggle in results page
- [ ] Simplify legal language
- [ ] Add examples
- [ ] Use everyday words
- [ ] Short sentences

#### Comparison Feature
- [ ] Select 2 contracts
- [ ] Side-by-side comparison
- [ ] Highlight differences
- [ ] Show which is more favorable
- [ ] Generate negotiation points

#### Red Flag Alerts
- [ ] Detect critical issues
- [ ] Show prominent warnings at top
- [ ] Categorize by severity
- [ ] Provide actionable recommendations
- [ ] Link to relevant sections

#### Export Options
- [ ] PDF export (styled)
- [ ] DOCX export (editable)
- [ ] Email to lawyer
- [ ] Google Docs integration
- [ ] Print-friendly view

#### Confidence Calibration
- [ ] Feedback form on each section
- [ ] "Was this accurate?" buttons
- [ ] Free-text comment field
- [ ] Store feedback in database
- [ ] Analyze feedback patterns
- [ ] Adjust confidence scores over time
- [ ] Dashboard for feedback stats (admin)

---

## Phase 5: Payments & Polish (Week 6)

### Objective
Add monetization, polish UX, prepare for launch.

### Stripe Integration

#### Products
1. **Premium Monthly**: $9.99/month
   - Unlimited analyses
   - Multi-document consistency check
   - No ads
   - Priority support
   - Export options
   - Deadline reminders

2. **Premium Annual**: $99/year (17% discount)
   - Same as monthly
   - 2 months free

#### Implementation
- [ ] Stripe account setup
- [ ] Create products & prices
- [ ] Checkout session endpoint
- [ ] Customer portal integration
- [ ] Webhook handler
- [ ] Subscription status sync
- [ ] Upgrade/downgrade flow
- [ ] Cancel flow
- [ ] Invoice emails

### Ad Integration (Free Tier Only)

**Placement**:
- ✅ Landing page footer
- ✅ History page sidebar
- ❌ Upload page (no distraction)
- ❌ Results page (kills trust)
- ❌ Premium users (always ad-free)

**Provider Options**:
- Google AdSense
- Carbon Ads (tech-focused)
- PropellerAds

**Implementation**:
- [ ] Ad provider account
- [ ] Ad components
- [ ] Conditional rendering (tier check)
- [ ] Ad blocker detection (optional)

### GDPR Compliance

- [ ] Privacy policy page
- [ ] Terms of service page
- [ ] Cookie consent banner
- [ ] Data export endpoint
- [ ] Account deletion endpoint
- [ ] Data retention settings
- [ ] PII redaction
- [ ] Right to be forgotten

### Polish Tasks

- [ ] Loading states everywhere
- [ ] Error messages (user-friendly)
- [ ] Empty states (no contracts yet)
- [ ] Success animations
- [ ] Toast notifications
- [ ] Keyboard shortcuts
- [ ] Accessibility audit
- [ ] Mobile testing (iOS Safari, Android Chrome)
- [ ] Cross-browser testing
- [ ] Performance optimization
- [ ] Bundle size reduction
- [ ] Image optimization
- [ ] Lazy loading

---

## Phase 6: Testing & Launch (Weeks 7-8)

### Testing

#### Unit Tests
- [ ] Backend: parsers, analyzers, formatters
- [ ] Frontend: components, stores, utils

#### Integration Tests
- [ ] API endpoints
- [ ] Authentication flow
- [ ] Upload → analyze → results flow
- [ ] Payment flow

#### E2E Tests (Playwright)
- [ ] User registration
- [ ] Login
- [ ] Upload contract
- [ ] View results
- [ ] Upgrade to premium
- [ ] Multi-document upload
- [ ] Comparison
- [ ] Export

#### Manual Testing
- [ ] Test with real contracts (10+ per language)
- [ ] Test all edge cases
- [ ] Test error scenarios
- [ ] Mobile testing
- [ ] Accessibility testing

### Performance

- [ ] Lighthouse score >90 (mobile & desktop)
- [ ] First Contentful Paint <1.5s
- [ ] Time to Interactive <3s
- [ ] Bundle size <250KB gzipped
- [ ] API response time P95 <500ms

### Security

- [ ] OWASP Top 10 checklist
- [ ] SQL injection tests
- [ ] XSS tests
- [ ] CSRF protection
- [ ] Rate limiting
- [ ] File upload validation
- [ ] Password strength requirements
- [ ] JWT expiration
- [ ] Secrets management

### Deployment

#### Backend (Fly.io)
- [ ] Dockerfile
- [ ] fly.toml configuration
- [ ] PostgreSQL setup
- [ ] Redis setup
- [ ] Persistent volumes for files
- [ ] Environment variables
- [ ] Deploy to production
- [ ] Health checks
- [ ] Scaling configuration

#### Frontend (Vercel)
- [ ] Build configuration
- [ ] Environment variables
- [ ] Deploy to production
- [ ] Custom domain
- [ ] SSL certificate
- [ ] CDN configuration

#### Infrastructure
- [ ] Domain registration
- [ ] DNS configuration
- [ ] Email service (SendGrid)
- [ ] Monitoring (Sentry)
- [ ] Uptime monitoring (UptimeRobot)
- [ ] Database backups (daily)
- [ ] Backup restore test

### Launch

- [ ] Landing page with clear value prop
- [ ] Sample analyses (scrubbed contracts)
- [ ] SEO optimization
  - Meta tags
  - Open Graph images
  - Sitemap.xml
  - robots.txt
- [ ] Analytics (Plausible or GA4)
- [ ] Social media accounts
- [ ] Launch announcement
- [ ] Product Hunt launch (optional)
- [ ] Reddit/HN post (optional)

---

## Post-Launch Roadmap

### Phase 7: Growth & Iteration (Months 2-3)

#### Features
- [ ] OCR support (scanned contracts)
- [ ] Mobile app (React Native or Capacitor)
- [ ] Contract templates library
- [ ] Negotiation email generator
- [ ] Contract builder (reverse: create contracts)
- [ ] Team accounts (share analyses)
- [ ] Slack/Teams integration
- [ ] API for developers
- [ ] More languages (Spanish, German, Italian)
- [ ] More contract types (freelance, vendor, partnership)

#### Improvements
- [ ] Better risk detection (ML model training)
- [ ] Faster analysis (optimize prompts)
- [ ] Better translations (fine-tuned models)
- [ ] Personalized recommendations
- [ ] Learning from feedback

#### Marketing
- [ ] Content marketing (blog posts)
- [ ] SEO optimization
- [ ] Partnerships with law firms
- [ ] Affiliate program
- [ ] Referral program
- [ ] Case studies

---

## Cost Projections

### Prototype (Week 1)
- Hosting: $0 (HF Spaces)
- LLM: $0 (Groq free tier)
- **Total: $0/month**

### MVP (Months 1-2)
- Hosting: $5/month (Fly.io free tier + $5 backend)
- LLM: $0-10/month (Groq free tier, pay if exceed)
- Domain: $1/month ($12/year)
- Email: $0 (SendGrid free tier)
- Monitoring: $0 (Sentry free tier)
- **Total: $6-16/month** ✅

### Growth (100 users, 10 Premium)
- Hosting: $10/month
- LLM: $30/month
- Email: $0 (still free)
- **Total: $40/month**
- **Revenue: $99/month** (10 × $9.99)
- **Profit: $59/month**

### Scale (1000 users, 100 Premium)
- Hosting: $30/month
- LLM: $100/month
- Email: $15/month
- CDN: $10/month
- **Total: $155/month**
- **Revenue: $999/month** (100 × $9.99)
- **Profit: $844/month**

---

## Success Metrics

### MVP Launch (Month 1)
- [ ] 50 registered users
- [ ] 150 contracts analyzed
- [ ] 5 Premium subscribers
- [ ] <5% error rate
- [ ] >4/5 user satisfaction

### Month 3
- [ ] 500 users
- [ ] 1500 contracts analyzed
- [ ] 50 Premium subscribers ($500/month revenue)
- [ ] <2% error rate
- [ ] >4.5/5 user satisfaction

### Month 6
- [ ] 2000 users
- [ ] 6000 contracts analyzed
- [ ] 200 Premium subscribers ($2000/month revenue)
- [ ] Break-even or profitable
- [ ] Case studies from lawyers

---

## Risk Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| LLM accuracy too low | High | Medium | Prototype testing with lawyer first; iterate |
| LLM costs too high | High | Low | Free tier + cache aggressively; self-host if needed |
| Legal liability | Critical | Low | Strong disclaimers; "not legal advice"; ToS |
| Translation quality poor | Medium | Medium | Hybrid approach (original + English); show both |
| No product-market fit | High | Medium | Prototype validation; early user feedback |
| GDPR violations | Critical | Low | Built-in compliance; data export/delete |
| Stripe payment issues | Medium | Low | Test thoroughly; use Stripe test mode first |
| Slow adoption | Medium | Medium | Free tier; word-of-mouth; lawyer partnerships |

---

## Team & Resources

### Current Team
- 1 developer (you)
- 1 lawyer tester (for validation)

### Future Hires (if scaling)
- Product designer (Month 3)
- Marketing (Month 4)
- Legal counsel (Month 6)
- Customer support (Month 6)

### Tools & Services
- **Development**: VS Code, GitHub, Docker
- **Design**: Figma (optional), Tailwind UI
- **Project Management**: Linear or GitHub Projects
- **Communication**: Slack or Discord
- **Documentation**: Notion or GitBook
- **Analytics**: Plausible or PostHog
- **Error Tracking**: Sentry
- **Uptime**: UptimeRobot
- **Status Page**: Statuspage.io (optional)

---

**Last Updated**: 2025-11-06
