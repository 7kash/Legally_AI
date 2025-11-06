# Legally AI - Decision Log

This document records all major decisions made during development, including alternatives considered and rationale for choices.

---

## Architecture Decisions

### AD-001: Prototype-First Approach on Hugging Face Spaces

**Date**: 2025-11-06
**Status**: ✅ Accepted
**Context**: Need to validate accuracy and usefulness before building full production system.

**Decision**: Build working prototype on HF Spaces first, get lawyer feedback, then build production MVP.

**Alternatives Considered**:
1. ❌ **Build full MVP first**: Too risky; might build wrong thing
2. ❌ **Skip prototype, use gold test set**: We don't have gold set; lawyer's real contracts more valuable

**Rationale**:
- Fast iteration on HF Spaces (deploy in minutes)
- Real lawyer feedback with actual contracts
- Validate LLM accuracy before committing to architecture
- Zero cost for testing phase
- Can pivot quickly if approach is wrong

**Consequences**:
- ✅ Lower risk
- ✅ Faster validation
- ⚠️ Need to rebuild for production (but prompts/logic reusable)

---

### AD-002: Groq API over Hugging Face Inference API

**Date**: 2025-11-06
**Status**: ✅ Accepted
**Context**: Need free or very low-cost LLM API for prototype and MVP.

**Decision**: Use Groq API with llama-3.3-70b-versatile as primary provider.

**Alternatives Considered**:
1. ❌ **Hugging Face Inference API**: Rate limits too strict on free tier; slow inference
2. ❌ **OpenAI API**: Not free; $0.15-0.60 per 1M tokens
3. ❌ **Self-hosted LLM**: Requires GPU; complex setup; higher cost
4. ❌ **DeepSeek via HF**: Initially proposed but Groq is faster and more generous

**Rationale**:
- Groq free tier: 14,400 requests/day, 30/min
- Extremely fast (800+ tokens/sec)
- Llama-3.3-70B has excellent multilingual support (Russian, Serbian, French)
- Strong reasoning capabilities for contract analysis
- Easy to switch providers later (using LLM router abstraction)

**Consequences**:
- ✅ $0 cost for prototype
- ✅ Very fast responses (<2s for most analyses)
- ✅ Generous free tier covers hundreds of analyses/month
- ⚠️ Need fallback if rate limited (add in production)

---

### AD-003: Nuxt 3 over Vue 3 Standalone

**Date**: 2025-11-06
**Status**: ✅ Accepted
**Context**: Need modern frontend framework for mobile-first PWA.

**Decision**: Use Nuxt 3 (Vue meta-framework) instead of standalone Vue 3.

**Alternatives Considered**:
1. ❌ **Vue 3 + Vite**: More manual setup; need to configure routing, SSR, i18n separately
2. ❌ **Next.js**: React-based; team prefers Vue; larger bundle size
3. ❌ **SvelteKit**: Less mature ecosystem; fewer components

**Rationale**:
- Nuxt 3 includes out-of-the-box:
  - File-based routing
  - SSR/SSG for SEO and performance
  - Auto-imports
  - Built-in i18n support
  - PWA plugin
  - State management (Pinia)
- Faster development (less boilerplate)
- Better SEO (server-side rendering)
- Excellent mobile performance
- Strong TypeScript support

**Consequences**:
- ✅ Faster development
- ✅ Better SEO
- ✅ Easier i18n (4 languages)
- ⚠️ Slightly more opinionated than Vue 3 alone

---

### AD-004: PostgreSQL from Day 1 (Not SQLite)

**Date**: 2025-11-06
**Status**: ✅ Accepted
**Context**: Need database for MVP user accounts and contract storage.

**Decision**: Use PostgreSQL from day 1, even in development.

**Alternatives Considered**:
1. ❌ **SQLite for dev, PostgreSQL for production**: Migration pain; subtle bugs
2. ❌ **MongoDB**: Overkill; relational data fits SQL better
3. ❌ **Supabase**: Extra abstraction layer; prefer direct PostgreSQL

**Rationale**:
- Avoid SQLite → PostgreSQL migration issues
- PostgreSQL features needed:
  - JSONB for analysis data
  - Full-text search for contracts
  - Better concurrent access
  - Row-level security
- Fly.io offers free PostgreSQL (1GB)
- Development parity with production

**Consequences**:
- ✅ No migration pain
- ✅ Production-ready from start
- ✅ Better features (JSONB, full-text search)
- ⚠️ Slightly more setup than SQLite

---

### AD-005: LLM Router (Provider-Agnostic)

**Date**: 2025-11-06
**Status**: ✅ Accepted
**Context**: Initial plan hard-wired DeepSeek-R1; feedback suggested abstraction.

**Decision**: Build LLM router abstraction layer supporting multiple providers.

**Alternatives Considered**:
1. ❌ **Hard-wire single provider**: Brittle; expensive if that provider has issues
2. ❌ **Use LangChain for everything**: Overkill; adds complexity

**Rationale**:
- Can switch providers without code changes
- Can route based on:
  - Task complexity (preparation vs analysis)
  - Budget (cheap vs quality models)
  - Availability (fallback if primary down)
- Can A/B test different models
- Future-proof (new models emerge constantly)

**Providers in Router**:
1. Groq (llama-3.3-70b) - Primary
2. Together.ai (mixtral, qwen) - Fallback
3. OpenAI (gpt-4o-mini) - Quality fallback
4. Anthropic (claude-3-haiku) - Future option

**Consequences**:
- ✅ Flexibility
- ✅ Cost optimization
- ✅ Resilience
- ⚠️ More code to maintain

---

## Feature Decisions

### FD-001: Multilingual Support from Day 1

**Date**: 2025-11-06
**Status**: ✅ Accepted
**Context**: Core use case is foreign-language contracts (Russian, Serbian, French).

**Decision**: Support 4 languages in MVP: Russian, Serbian, French, English.

**Alternatives Considered**:
1. ❌ **English only, add languages later**: Core use case requires multilingual
2. ❌ **All languages from start**: Too complex; start with 4
3. ❌ **Auto-translate everything to English first**: Loses legal nuance

**Rationale**:
- Target user (lawyer) needs Russian/Serbian/French
- Llama-3.3-70B handles all 4 languages well
- Structuring for i18n from start easier than retrofitting
- Competitive advantage (most tools are English-only)

**Approach**:
- Hybrid: Analyze in original language, optionally translate output
- Show key quotes in both original + translation
- Jurisdiction-specific risk context
- Legal term glossary

**Consequences**:
- ✅ Addresses core use case
- ✅ Competitive advantage
- ⚠️ More complex prompts
- ⚠️ Translation quality risk (mitigated by showing both)

---

### FD-002: No Ads on Results Pages

**Date**: 2025-11-06
**Status**: ✅ Accepted
**Context**: Initial plan had ads during analysis; feedback said this kills trust.

**Decision**: Ads only on landing and history pages, NEVER on results pages.

**Alternatives Considered**:
1. ❌ **Ads everywhere (more revenue)**: Kills trust for legal product
2. ❌ **No ads at all**: Need monetization for free tier
3. ❌ **Animated ad during analysis**: Distracting, untrustworthy

**Rationale**:
- Legal advice is trust-critical
- Users making important decisions
- Ads on results imply "not serious"
- Better to lose ad revenue than user trust
- Premium tier has no ads (incentive to upgrade)

**Ad Placement**:
- ✅ Landing page footer
- ✅ History page sidebar
- ❌ Upload page
- ❌ Analysis results page
- ❌ Any page during decision-making

**Consequences**:
- ✅ Maintains trust
- ✅ Professional image
- ⚠️ Lower ad revenue (acceptable trade-off)

---

### FD-003: Trial System (3 Free Analyses)

**Date**: 2025-11-06
**Status**: ✅ Accepted
**Context**: Need balance between free usage and conversion to paid.

**Decision**: 3 free contract analyses, then $9.99/month for unlimited.

**Alternatives Considered**:
1. ❌ **Fully free (ads only)**: Hard to sustain; LLM costs scale
2. ❌ **1 free analysis**: Too stingy; users can't evaluate quality
3. ❌ **Unlimited free with limits**: Complex to explain
4. ❌ **Freemium with crippled features**: Poor UX

**Rationale**:
- 3 analyses enough to evaluate usefulness
- Most users won't need more (one-time use)
- Power users (lawyers, businesses) will pay
- Simple to explain
- Industry standard (similar to Grammarly, Loom, etc.)

**Premium Features**:
- Unlimited analyses
- Multi-document consistency check
- Deadline reminders
- Priority support
- No ads
- Export options

**Consequences**:
- ✅ Clear value proposition
- ✅ Simple pricing
- ⚠️ May lose some users after 3 (acceptable)

---

### FD-004: Async Analysis with SSE Progress

**Date**: 2025-11-06
**Status**: ✅ Accepted
**Context**: Contract analysis takes 10-30 seconds; synchronous HTTP times out.

**Decision**: Use Celery for async jobs, SSE for real-time progress updates.

**Alternatives Considered**:
1. ❌ **Synchronous API calls**: Times out; poor UX
2. ❌ **Polling every 2s**: Inefficient; delays
3. ❌ **WebSockets**: Overkill; more complex
4. ❌ **Background job without progress**: User doesn't know what's happening

**Rationale**:
- Celery is mature, reliable
- SSE simpler than WebSockets (one-way)
- Real-time progress improves perceived performance
- Can show: "Parsing document → Analyzing structure → Detecting risks"
- Better UX than spinner

**Implementation**:
- FastAPI endpoint creates Celery task
- Returns task ID
- Frontend opens SSE connection
- Backend emits events: parsing (10%), preparation (40%), analysis (80%), done (100%)

**Consequences**:
- ✅ Better UX
- ✅ Handles long-running tasks
- ✅ No timeouts
- ⚠️ More infrastructure (Redis + Celery)

---

### FD-005: Confidence Scoring with Auto-Downgrade

**Date**: 2025-11-06
**Status**: ✅ Accepted
**Context**: Some contracts are too poor quality for reliable analysis.

**Decision**: Automatic confidence scoring with hard gates; downgrade to "Preliminary review" if too low.

**Alternatives Considered**:
1. ❌ **Always return full analysis**: Risky; might be wrong
2. ❌ **Manual review flag**: Can't scale
3. ❌ **Reject poor quality**: User has no output; poor UX

**Rationale**:
- Better to say "low confidence" than give wrong answer
- Users can still get some value (basic info)
- Protects against liability
- Builds trust (honest about limitations)

**Factors**:
- Scan quality (0-1)
- Coverage (0-1, % of referenced documents present)
- Translation (without original)
- OCR quality

**Thresholds**:
- High confidence: ≥0.8
- Medium confidence: 0.5-0.79
- Low confidence: <0.5 → Auto-downgrade to "Preliminary review"

**Hard Gates** (stop full analysis):
- Scan legibility <0.4
- Coverage <0.5
- Translation without original + governing law unclear

**Consequences**:
- ✅ Protects users from bad analysis
- ✅ Builds trust
- ✅ Reduces liability
- ⚠️ Some contracts can't be fully analyzed (acceptable)

---

## Technology Decisions

### TD-001: FastAPI over Flask/Django

**Date**: 2025-11-06
**Status**: ✅ Accepted
**Context**: Need Python backend framework.

**Decision**: Use FastAPI.

**Alternatives Considered**:
1. ❌ **Flask**: Less modern; no automatic docs; slower
2. ❌ **Django**: Too heavy; includes ORM, admin, etc. we don't need
3. ❌ **Starlette**: Too low-level; FastAPI built on it anyway

**Rationale**:
- Modern (async/await)
- Fast (comparable to Node.js)
- Automatic OpenAPI docs
- Type hints (Python 3.11+)
- Great developer experience
- Active community

**Consequences**:
- ✅ Fast development
- ✅ Automatic API docs
- ✅ Type safety
- ⚠️ Newer than Django (less mature)

---

### TD-002: Fly.io + Vercel over Railway/Heroku

**Date**: 2025-11-06
**Status**: ✅ Accepted
**Context**: Need hosting for production MVP with <$50/month budget.

**Decision**: Backend on Fly.io, frontend on Vercel.

**Alternatives Considered**:
1. ✅ **Railway (all-in-one)**: Simpler but slightly more expensive ($5 minimum); good alternative
2. ❌ **Heroku**: No free tier anymore; expensive
3. ❌ **AWS/GCP**: Overkill; complex; billing surprises
4. ❌ **DigitalOcean**: Good but more manual setup

**Rationale**:

**Fly.io**:
- Free tier: 3 VMs, 1GB PostgreSQL, 256MB Redis
- Easy scaling
- Global edge network
- Docker-based (portable)

**Vercel**:
- Perfect for Nuxt 3 (SSR out-of-the-box)
- Free tier generous (hobby projects)
- Fast CDN
- Zero config deployment

**Combined Cost**:
- Fly.io: $0-5/month (free tier + $5 if needed)
- Vercel: $0 (free tier)
- **Total: $0-5/month** ✅

**Railway as Alternative**:
- Single platform (simpler)
- $5/month minimum
- Great DX
- If Fly.io too complex, switch to Railway

**Consequences**:
- ✅ Well under budget
- ✅ Great performance
- ✅ Easy deployment
- ⚠️ Two platforms (could use Railway instead)

---

### TD-003: Gradio for Prototype UI

**Date**: 2025-11-06
**Status**: ✅ Accepted
**Context**: Need to build prototype UI quickly for HF Spaces.

**Decision**: Use Gradio for prototype.

**Alternatives Considered**:
1. ❌ **Streamlit**: Less interactive; harder to customize
2. ❌ **Plain HTML/JS**: Too much work for prototype
3. ❌ **Build Nuxt UI immediately**: Overkill for testing

**Rationale**:
- Gradio designed for HF Spaces
- 10-20 lines of code for full UI
- Built-in file upload, markdown rendering
- Easy to iterate
- Not for production (will rebuild with Nuxt)

**Consequences**:
- ✅ Extremely fast prototype
- ✅ Native HF Spaces support
- ⚠️ Limited customization (acceptable for prototype)
- ⚠️ Will rebuild for MVP (but prompts/logic reusable)

---

## Rejected Ideas

### Rejected: Gold Test Set Creation Before Prototype

**Date**: 2025-11-06
**Status**: ❌ Rejected

**Idea**: Create 20-40 annotated test contracts before building prototype.

**Why Rejected**:
- Don't have existing contracts to annotate
- Lawyer has real contracts to test with
- Real feedback more valuable than synthetic test set
- Test set creation is time-consuming
- Can create test set later based on lawyer feedback

**Better Approach**: Build prototype, get lawyer to test with real contracts, then create test set from those.

---

### Rejected: Embedded Gradio in Production Vue/Nuxt

**Date**: 2025-11-06
**Status**: ❌ Rejected

**Idea**: Embed Gradio components in Nuxt production app.

**Why Rejected**:
- Known integration issues (Gradio doesn't work well in Next.js/Nuxt)
- Only option is iframe (poor UX)
- Can't customize styling
- Can't integrate with Vue state management
- Two separate apps harder to maintain

**Better Approach**: Build native Nuxt UI, call backend API directly.

---

### Rejected: OCR in MVP

**Date**: 2025-11-06
**Status**: ❌ Deferred to Phase 2

**Idea**: Support scanned contracts (OCR) in MVP.

**Why Rejected**:
- Adds complexity
- OCR quality often poor (leads to bad analysis)
- Most target users have digital contracts
- Can add later if demand exists
- Tesseract/Google Vision API adds cost

**Better Approach**: MVP handles digital PDFs/DOCX only; add OCR in Phase 2 if users request it.

---

### Rejected: Contract Templates Library

**Date**: 2025-11-06
**Status**: ❌ Deferred to Post-Launch

**Idea**: Include library of contract templates users can customize.

**Why Rejected**:
- Scope creep for MVP
- Not core use case (analysis, not creation)
- Legal liability (providing templates)
- Can add later if users want it

**Better Approach**: Focus on analysis; add templates later if there's demand.

---

### Rejected: Team Accounts in MVP

**Date**: 2025-11-06
**Status**: ❌ Deferred to Post-Launch

**Idea**: Multiple users can share analyses, collaborate.

**Why Rejected**:
- Adds significant complexity (permissions, sharing, collaboration)
- MVP targets individuals, not teams
- Can validate single-user first
- If successful, add team features later

**Better Approach**: Single-user MVP; add teams in Phase 7 if there's B2B demand.

---

### Rejected: Mobile Native App (iOS/Android)

**Date**: 2025-11-06
**Status**: ❌ Deferred to Post-Launch

**Idea**: Build native mobile apps in addition to web.

**Why Rejected**:
- PWA (Progressive Web App) provides 90% of native app benefits
- Native apps mean:
  - 3x codebases (web, iOS, Android)
  - App Store review process
  - More maintenance
- Can install PWA to home screen
- Web app works on all devices

**Better Approach**: Build excellent PWA; only go native if users strongly request it.

---

## Strategy Decisions

### SD-001: "Disneyland Layer" Branding

**Date**: 2025-11-06
**Status**: ✅ Accepted
**Context**: Legal products often feel intimidating, formal, stuffy.

**Decision**: Brand as "fun and easy, but professional" — like Disneyland (delightful surface, professional underneath).

**Rationale**:
- Legal analysis intimidates most people
- Friendly ≠ unprofessional
- Examples: Stripe, Notion, Linear (serious products, friendly UX)
- Trust comes from accuracy, not stuffiness

**Implementation**:
- Conversational copy ("Let's look at your contract" not "Contract analysis initiated")
- Clear explanations, no jargon
- Helpful micro-copy
- Smooth animations, delightful interactions
- Warm color palette (not all blue/gray)
- Encouraging tone ("You've got this")
- Still show disclaimers, accuracy, professionalism

**Consequences**:
- ✅ More approachable
- ✅ Better user experience
- ✅ Word-of-mouth ("this tool is actually nice to use")
- ⚠️ Risk of seeming too casual (mitigated by accurate analysis)

---

### SD-002: Lawyer Partnership for Validation

**Date**: 2025-11-06
**Status**: ✅ Accepted
**Context**: Can't launch legal product without expert validation.

**Decision**: Partner with lawyer (who works with Russian/Serbian/French contracts) for prototype testing.

**Rationale**:
- Need domain expertise
- Real contracts better than synthetic tests
- Feedback on accuracy critical
- Lawyer testimonial valuable for marketing
- May lead to referrals

**Approach**:
1. Build prototype
2. Share with lawyer
3. Lawyer tests with real contracts (anonymized)
4. Collect detailed feedback
5. Iterate until lawyer satisfied
6. Get testimonial/case study

**Consequences**:
- ✅ Validates accuracy
- ✅ Identifies blind spots
- ✅ Marketing asset (testimonial)
- ⚠️ Dependent on lawyer's availability

---

### SD-003: Freemium with Premium Upsell

**Date**: 2025-11-06
**Status**: ✅ Accepted
**Context**: Need monetization strategy.

**Decision**: Freemium model — 3 free analyses, then $9.99/month Premium.

**Alternatives Considered**:
1. ❌ **Fully paid (no free tier)**: Limits growth
2. ❌ **Pay-per-analysis**: Complex pricing; friction
3. ❌ **Ads-only (no paid tier)**: Hard to sustain; user experience suffers
4. ❌ **Enterprise-only**: Limits market

**Rationale**:
- Free tier drives adoption
- Most users one-time (won't pay)
- Power users (lawyers, HR, small businesses) will pay
- $9.99/month affordable
- Unlimited analyses (no pay-per-use friction)
- Clear upgrade path

**Revenue Projections**:
- 10% conversion is realistic
- 1000 users → 100 Premium → $999/month
- Break-even at ~50-100 users

**Consequences**:
- ✅ Growth via free tier
- ✅ Sustainable via paid tier
- ✅ Simple pricing
- ⚠️ Need to balance free/paid value

---

## Open Questions

Questions to answer as we progress:

### OQ-001: Should we add more languages?
**Status**: Open
**Context**: MVP has 4 languages (Russian, Serbian, French, English). Users may want more.
**Options**:
- Add Spanish (large market)
- Add German (business market)
- Add Chinese (huge market)
**Decision**: Wait for user feedback after MVP launch.

---

### OQ-002: Should we support video contracts?
**Status**: Open
**Context**: Some contracts might be in video format (signed via Zoom, etc.)
**Options**:
- Add speech-to-text
- Extract contract from meeting recording
**Decision**: Not MVP; evaluate if users request.

---

### OQ-003: Should we build API for developers?
**Status**: Open
**Context**: Developers might want to integrate contract analysis into their apps.
**Options**:
- Public API with API keys
- Rate limits, tiered pricing
**Decision**: Post-launch; validate B2B demand first.

---

**Last Updated**: 2025-11-06
