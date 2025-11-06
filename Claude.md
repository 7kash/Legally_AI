# Claude Context - Legally AI Project

## Project Overview
Legally AI is a multilingual contract analysis web application that helps users understand legal agreements in Russian, Serbian, French, and English. The app provides AI-powered analysis of contracts, extracting key terms, obligations, rights, and risks.

## Current Session Summary (2025-11-06)

### User Profile
- **GitHub**: 7kash
- **Hugging Face**: 7Kash-FluffyHedgehog
- **Has**: Groq API account (free tier)
- **Target User**: Lawyer who works with Russian/Serbian/French contracts

### Key Decisions Made Today

1. **Development Approach**: Prototype-first on HF Spaces, then full MVP
2. **LLM Strategy**: Groq API (free tier) with llama-3.3-70b-versatile
3. **Languages**: Russian, Serbian, French, English (MVP)
4. **Cost Target**: Prototype $0/month, MVP <$50/month (achieved $6-16/month)
5. **Branding**: "Disneyland layer" - fun and easy, but professional

### Core Use Cases

1. **Primary**: User uploads contract → gets comprehensive analysis
2. **Secondary**: Foreign language contracts → translation + analysis + jurisdiction context
3. **Trial**: 3 free analyses, then $9.99/month Premium

### Tech Stack

#### Prototype (HF Spaces)
- **Frontend**: Gradio
- **Backend**: Python 3.11 (in same app)
- **LLM**: Groq API (llama-3.3-70b-versatile)
- **Parsers**: pdfplumber, python-docx, langdetect
- **Hosting**: Hugging Face Spaces (free CPU tier)
- **Storage**: None (stateless)

#### MVP (Production)
- **Frontend**: Nuxt 3 + Tailwind + PWA
- **Backend**: FastAPI + Celery + Redis
- **Database**: PostgreSQL
- **LLM**: Groq API with fallback providers
- **Hosting**: Fly.io ($5/month) + Vercel (free)
- **Auth**: JWT with FastAPI-Users
- **Payments**: Stripe
- **Monitoring**: Sentry (free tier)

### Analysis Specification

The app follows a detailed two-step analysis process:

#### Step 1: Preparation
- File inventory and classification
- Primary agreement selection
- Text normalization and OCR detection
- Governing language check
- Coverage discovery (missing annexes)
- Quality & completeness scoring
- Version & status detection
- Agreement type classification
- User role identification
- Negotiability assessment
- Analysis mode selection

#### Step 2: Text Analysis
- Structure mapping
- Core field extraction (parties, amounts, dates, etc.)
- User obligations extraction (with short quotes)
- User rights extraction (with short quotes)
- Expectations check vs typical agreements
- Risk detection and scoring
- Calendar building (deadlines, renewal dates)
- Screening result determination

### Output Format (Exact Spec)

The UI must display these sections in this exact format:

1. **Summary** (always visible)
   - Screening result (4 fixed variants)
   - Important limits disclaimer (exact text)
   - Confidence level with coverage line

2. **About the contract**
   - What this agreement is about (2-3 sentences, ≤300 chars)
   - What you pay and when (up to 5 bullets, ≤120 chars each)
   - What you agree to do (up to 5 bullets, ≤120 chars each)

3. **Suggestions**
   - Check these terms (3-5 items, ≤150 chars)
   - Also think about (3-5 items, ≤150 chars)
   - Ask for these changes (if negotiability ≠ low)
   - If you decide to sign "As Is" (3-5 mitigations)
   - Each section has "Helpful, what else?" button (loads next 5)

4. **Act now**
   - Action buttons (calendar, checklists, email drafts)

5. **All key terms** (collapsed by default)
   - 8+ subsections with plain text explanations

### MVP Feature Set (Enhanced)

#### Core Features
- ✅ User accounts (email/password)
- ✅ 3 free analyses trial
- ✅ Premium subscription ($9.99/month)
- ✅ Contract history with re-view
- ✅ Download as PDF
- ✅ Multilingual (4 languages)
- ✅ Mobile-responsive PWA
- ✅ GDPR (export/delete data)
- ✅ Async analysis with SSE progress
- ✅ Ads on landing/history only (not results)

#### Advanced Features (Added Today)
- ✅ **Renewal & Deadline Radar**: Auto-detect renewal windows, notice periods, escalations
- ✅ **Cross-Document Consistency Check**: Upload MSA + SOWs + NDA; flag conflicts
- ✅ **Lawyer Handoff Pack**: One-click export (summary, redlines, questions, table)
- ✅ **Privacy "Do-Not-Store" Mode**: Local processing, scrub after analysis, redact PII
- ✅ **Multilingual Mirror View**: Side-by-side translation with alignment
- ✅ **Contract Type Detection Training**: Type-specific prompts per language
- ✅ **"Explain Like I'm 5" Mode**: Simplify legal jargon
- ✅ **Comparison Feature**: Compare 2 contracts, highlight differences
- ✅ **Red Flag Alerts**: Prominent warnings for critical issues
- ✅ **Multiple Export Options**: PDF, DOCX, email to lawyer, Google Docs
- ✅ **Confidence Calibration**: Feedback loop from lawyer corrections

### Rejected Ideas (and Why)

1. **SQLite for production** → Rejected: PostgreSQL from day 1 to avoid migration pain
2. **Vue 3 standalone** → Rejected: Nuxt 3 gives SSR, routing, i18n out of the box
3. **Hard-wire DeepSeek-R1** → Rejected: Built provider-agnostic LLM router instead
4. **Ads on results pages** → Rejected: Kills trust; ads only on landing/history
5. **Gradio embedded in Next.js/Vue** → Rejected: Integration issues; build native frontend
6. **OCR in MVP** → Deferred: Start with digital PDFs, add OCR in Phase 2
7. **Gold set creation first** → Rejected: Prototype first, get lawyer to test with real docs

### Confidence Scoring & Auto-Downgrade

The app automatically downgrades to "Preliminary review (low confidence)" when:
- Scan legibility < 0.4
- Coverage < 0.5 (more than half documents missing)
- Translation without original
- OCR quality too poor

Confidence factors:
- Scan quality (×0.5 if poor)
- Missing annexes (×0.8)
- Translation without original (×0.7)
- OCR used (×0.8)

Final levels: High (≥0.8), Medium (≥0.5), Low (<0.5)

### Multilingual Strategy

**Analysis Approach**: Hybrid
1. Step 1 (Preparation) in original language (preserves legal terms)
2. Step 2 (Analysis) can be in English for better reasoning
3. Output formatted in user's preferred language
4. Key quotes always shown in both original + translation

**Translation Principles**:
- Preserve legal terms in [brackets] if no good translation
- Keep amounts, dates, names untranslated
- Add brief notes for culture-specific terms
- Always show original quote alongside translation

**Jurisdiction-Aware Risk Assessment**:
- Russian: Employer-favored termination, weak deposit protection, electronic signature issues
- Serbian: Original Serbian required for validity, notarization needs, consumer protection
- French: Strong employee protection, cooling-off periods, tenant protections

### Cost Optimization Achieved

**Prototype**: $0/month (HF Spaces + Groq free)
**MVP**: $6-16/month (Fly.io $5 + domain $1 + Groq free tier)
**Scale (1000 users)**: $85-135/month
**Revenue potential**: 100 Premium users = $999/month

### Branding Guidelines

**Theme**: "Disneyland layer" - fun and easy, but professional

**Characteristics**:
- Friendly, approachable, not intimidating
- Clear, simple language (no legalese in UI)
- Delightful interactions (smooth animations, helpful feedback)
- Professional underneath (accurate, reliable, trustworthy)
- Color palette: TBD (likely blues/greens for trust + warm accent)
- Tone: Conversational but respectful, "helpful friend" not "stuffy lawyer"

**UI Principles**:
- Mobile-first (320px and up)
- Touch targets ≥48×48px
- No emoji in content (accessibility)
- Sentence case for headings
- Short bullets (≤200 chars)
- Progress indicators for all async operations
- Skeleton loaders, not spinners

### Development Timeline

**Week 1**: HF Prototype
- Days 1-2: Setup, Groq integration, file structure
- Days 3-4: Core logic (Step 1 + 2)
- Days 5-6: Multilingual support
- Day 7: Gradio UI, deploy to HF

**Week 2**: Lawyer Feedback & Iteration
- Share with lawyer, collect feedback
- Iterate on prompts and accuracy
- Refine risk detection

**Weeks 3-6**: MVP Development
- Week 3: Backend (FastAPI, auth, Celery)
- Week 4: Frontend (Nuxt 3, responsive UI)
- Week 5: Integration (connect FE/BE, SSE, trial system)
- Week 6: Polish (Stripe, GDPR, deploy)

### Important Constraints

1. **Character Limits** (from spec):
   - "About" section: ≤300 chars total
   - Payment bullets: ≤120 chars each
   - Obligation bullets: ≤120 chars each
   - Risk items: ≤150 chars each
   - Short quotes: ≤12 words

2. **Output Rules**:
   - No legal symbols (§) in user-facing text
   - No Latin terms unless in spec
   - No exclamation marks
   - No color/emoji-only cues
   - Screen-reader friendly

3. **Disclaimers** (exact text required):
   - Important limits on every result page
   - "Not legal advice" clearly stated
   - "No attorney-client relationship"
   - "Read full document, consider lawyer"

### Git Workflow

- **Development branch**: `claude/push-to-github-011CUqJ2MKGK82nb2cerQD3k`
- **Commit strategy**: Clear, descriptive messages
- **Push**: Always use `git push -u origin <branch-name>`
- **Branch naming**: Must start with `claude/` and end with session ID

### Next Steps

1. Create all documentation files (this session)
2. Initialize HF Space repository
3. Set up project structure
4. Implement document parser
5. Build Step 1 + 2 analysis logic
6. Create Gradio UI
7. Deploy and share with lawyer

### Files to Reference

- `plan.md`: Comprehensive development plan
- `progress.md`: Track completed tasks
- `decisions.md`: Record of all decisions and rationale
- `architecture.md`: Technical architecture details
- `mvp-features.md`: Feature specifications
- `branding.md`: Brand guidelines and UI principles
- `prompts/`: Directory with all LLM prompts per language

### Useful Commands

```bash
# Start local development
cd legally-ai-prototype
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py

# Deploy to HF
git push hf main

# Run MVP locally
docker-compose up

# Deploy MVP to Fly.io
fly deploy
```

### Contact & Resources

- **Repository**: https://github.com/7kash/Legally_AI
- **HF Space**: https://huggingface.co/spaces/7Kash-FluffyHedgehog/legally-ai (to be created)
- **Groq API**: https://console.groq.com
- **Docs**: All markdown files in root directory

---

**Last Updated**: 2025-11-06
**Session ID**: 011CUqJ2MKGK82nb2cerQD3k
