# Legally AI - MVP Feature Specifications

This document details all features to be implemented in the MVP, with acceptance criteria and priorities.

---

## Core Features (P0 - Must Have)

### CF-001: User Authentication

**User Story**: As a user, I want to create an account so I can save my contract analyses.

**Requirements**:
- [ ] Registration with email + password
- [ ] Email validation (format check)
- [ ] Password requirements: ≥8 chars, 1 uppercase, 1 number
- [ ] Password hashing (bcrypt, cost factor 12)
- [ ] Login with email + password
- [ ] JWT token generation (7 day expiration)
- [ ] Logout (client-side token deletion)
- [ ] "Remember me" option (30 day refresh token)

**UI Components**:
- Registration page
- Login page
- Password strength indicator
- Error messages (email taken, wrong password, etc.)

**Acceptance Criteria**:
- User can register with valid credentials
- User cannot register with duplicate email
- User can log in with correct credentials
- User cannot log in with wrong credentials
- Token expires after 7 days
- User redirected to login if token invalid

---

### CF-002: Contract Upload

**User Story**: As a user, I want to upload contracts in multiple formats and languages.

**Requirements**:
- [ ] Support PDF files (up to 10MB)
- [ ] Support DOCX files (up to 10MB)
- [ ] Drag & drop upload
- [ ] File picker upload
- [ ] File type validation (reject other formats)
- [ ] File size validation (reject >10MB)
- [ ] Upload progress indicator
- [ ] Auto-detect language (Russian, Serbian, French, English)
- [ ] User can override detected language
- [ ] Store file securely (filesystem or S3)

**UI Components**:
- Upload dropzone
- File picker button
- Upload progress bar
- File preview/thumbnail
- Error messages (wrong format, too large, etc.)

**Acceptance Criteria**:
- User can upload PDF ≤10MB
- User can upload DOCX ≤10MB
- User cannot upload JPG, PNG, TXT, etc.
- User cannot upload files >10MB
- Language auto-detected correctly >90% of time
- User can override language if wrong
- Upload completes in <10 seconds (P95)

---

### CF-003: Contract Analysis (Step 1: Preparation)

**User Story**: As a user, I want the system to analyze my contract's structure and quality.

**Requirements** (from specification):
- [ ] Count files; classify as agreement/context/unsupported
- [ ] If no agreement → stop, request one
- [ ] If >1 agreement → choose primary, mark others as context
- [ ] Normalize text (fix order/encoding, detect language)
- [ ] Governing language check (original vs translation)
- [ ] Timezone/jurisdiction hints detection
- [ ] Coverage discovery (referenced annexes/policies/schedules)
- [ ] Mark which annexes are present vs missing
- [ ] Quality & completeness score (0-1)
- [ ] Rate scan legibility, coverage, reasons (scan, OCR, partial, translation)
- [ ] Version & status (draft vs signed, effective date, version stamp)
- [ ] Deduplicate near-duplicates, keep latest
- [ ] Agreement type classification (lease, ToS, NDA, employment, etc.)
- [ ] User role identification (tenant/customer/buyer, with confidence)
- [ ] Negotiability assessment (high/medium/low with rationale)
- [ ] Select analysis mode (Full review / Check-only / Preliminary)

**Output Fields**:
```json
{
  "files_uploaded": 1,
  "agreement_present": true,
  "primary_agreement": "Lease_Agreement.pdf",
  "agreement_type": "Residential lease",
  "agreement_subtype": "long-term",
  "user_role": "Tenant",
  "user_role_confidence": 0.82,
  "negotiability": "Medium",
  "negotiability_reason": "Private-party deal; edits likely",
  "governing_language": "English",
  "jurisdiction_hints": "Serbia / Europe/Belgrade",
  "version_status": "Draft (no signatures)",
  "effective_date": null,
  "coverage": {
    "present": ["Handover report", "Utilities list"],
    "missing": ["Inventory photos", "Serbian original"]
  },
  "quality_score": 0.74,
  "quality_reason": "Good scan; missing annexes",
  "warnings": ["Translation not confirmed", "No annexes"]
}
```

**Acceptance Criteria**:
- Agreement type identified correctly ≥80% of time
- User role identified correctly ≥75% of time
- Quality score correlates with actual quality
- Missing annexes detected ≥90% of time
- Analysis mode selected appropriately

---

### CF-004: Contract Analysis (Step 2: Text Analysis)

**User Story**: As a user, I want detailed analysis of terms, obligations, rights, and risks.

**Requirements** (from specification):
- [ ] Map structure (headings/themes: term, payments, exit, duties, rights, law)
- [ ] Extract core fields:
  - Parties (names, roles)
  - What you get/provide
  - Amounts (money, quantities)
  - Dates (start, end, deadlines)
  - Notices (how to communicate)
  - Change rights (who can modify)
  - Entry (access rights)
  - Repairs (who's responsible)
  - Law/forum (governing law, jurisdiction)
- [ ] Normalize values (format dates, money; deadline formulas)
- [ ] User obligations list:
  - Action required
  - Trigger condition
  - Time window/formula
  - Consequence of non-compliance
  - Short quote (≤12 words)
- [ ] User rights list:
  - Right description
  - How to exercise
  - Any window/condition
  - Short quote (≤12 words)
- [ ] Expectations check (compare to typical for this type)
- [ ] Mark gaps and anomalies
- [ ] Risk detection (high/medium/low signals):
  - Unilateral change clauses
  - Short notice periods
  - Data privacy risks
  - Liability issues
  - Unusual terms
- [ ] Risk scoring (priority = severity × likelihood × duration)
- [ ] Note hidden/forgettable risks
- [ ] Calendar build (derive dates or formulas):
  - Renewal/notice windows
  - Payment schedules
  - Activation windows
- [ ] Screening result (one of 4 variants):
  - "No major issues detected"
  - "Recommended to address flagged items"
  - "High risk as drafted — do not proceed without legal review"
  - "Preliminary review (low confidence)"
- [ ] Confidence update (keep Medium/Low with reason if applicable)

**Output Fields**:
```json
{
  "extracted_fields": {
    "parties": "Lessor: Danijela Božić; Lessee: Maria Matyushina",
    "premises": "Apt 22, Kraljice Marije 12, Belgrade",
    "term_start": "2025-03-20",
    "term_end": "2026-03-19",
    "rent": "€700 cash, pay 20-23 monthly",
    "deposit": "€600",
    "utilities": "Tenant pays (electricity, internet, building)",
    "entry": "48h notice, tenant presence required",
    "price_change": "60-day notice; tenant may exit early (10-day notice)",
    "termination": "Either side 30-day written notice",
    "law_forum": "Serbia; court in Belgrade"
  },
  "obligations": [
    {
      "action": "Pay €700 each month 20–23",
      "trigger": "Monthly rent due",
      "time_window": "20th-23rd of month",
      "consequence": "Breach; termination possible",
      "quote": "[pay … from 20th until 23rd]"
    }
  ],
  "rights": [
    {
      "right": "Terminate with 30-day notice",
      "how_to_exercise": "Written notice",
      "window": "Anytime",
      "quote": "[terminate … with 30 days]"
    }
  ],
  "gaps_anomalies": [
    "Deposit return has no fixed deadline (gap)",
    "Auto-renewal not stated (gap)",
    "Payments only in cash (risk)"
  ],
  "risks": [
    {
      "level": "medium",
      "category": "payment",
      "description": "Unilateral rent change (60-day notice)",
      "recommendation": "Request written notice + right to exit with no penalties"
    },
    {
      "level": "medium",
      "category": "evidence",
      "description": "Cash-only rent",
      "recommendation": "Request bank transfer or signed receipts"
    }
  ],
  "calendar": [
    {"date": "2025-03-05", "event": "Initial rent paid"},
    {"date": "monthly:20-23", "event": "Pay rent (€700)"},
    {"date": "2026-02-17", "event": "Send 30-day notice if ending at term"}
  ],
  "screening_result": "recommended_to_address",
  "confidence": {
    "level": "Medium",
    "coverage": "Reviewed 1 agreement; missing 2 annexes",
    "reason": "Annexes missing (handover inventory, Serbian original); cash payments reduce verifiability"
  }
}
```

**Acceptance Criteria**:
- Core fields extracted correctly ≥90% accuracy
- Obligations listed comprehensively (≥80% recall)
- Rights listed comprehensively (≥80% recall)
- Risks prioritized correctly (high-risk items ranked top)
- Calendar dates formatted consistently
- Screening result matches document quality

---

### CF-005: Analysis Results Display

**User Story**: As a user, I want to see analysis results in a clear, scannable format.

**Requirements** (from specification):
All sections must match the exact specification. See `Claude.md` for full details.

**UI Sections**:
1. **Summary** (always visible):
   - [ ] Screening result badge (4 variants with exact text)
   - [ ] Important limits disclaimer (exact text from spec)
   - [ ] Confidence level with coverage line

2. **About the contract**:
   - [ ] "What this agreement is about" (2-3 sentences, ≤300 chars)
   - [ ] "What you pay and when" (up to 5 bullets, ≤120 chars each)
   - [ ] "What you agree to do" (up to 5 bullets, ≤120 chars each)

3. **Suggestions**:
   - [ ] "Check these terms" (3-5 items, ≤150 chars, "More" button)
   - [ ] "Also think about" (3-5 items, ≤150 chars, "More" button)
   - [ ] "Ask for these changes" (if negotiable; "More" button)
   - [ ] "If you decide to sign 'As Is'" (3-5 mitigations, "More" button)

4. **Act now**:
   - [ ] Action buttons (Add to calendar, checklists, email drafts)

5. **All key terms** (collapsed by default):
   - [ ] Expandable accordion with subsections

**Acceptance Criteria**:
- All text follows character limits
- All sections present as specified
- Mobile-responsive (readable on 320px screens)
- "More" buttons load next 5 items
- Collapsible sections work correctly

---

### CF-006: Trial System (3 Free Analyses)

**User Story**: As a free user, I want to try the service with 3 free analyses before subscribing.

**Requirements**:
- [ ] Track `contracts_analyzed` per user
- [ ] Allow 3 analyses for free tier
- [ ] After 3rd analysis, show upgrade modal
- [ ] Block upload if limit reached (HTTP 402)
- [ ] Show usage stats: "X of 3 free analyses used"
- [ ] Premium users: unlimited analyses

**UI Components**:
- Usage stats badge in header
- Upgrade modal (after 3rd analysis)
- Paywall on upload page (if limit reached)

**Acceptance Criteria**:
- Free user can analyze 3 contracts
- Free user cannot analyze 4th without upgrading
- Premium user has no limit
- Usage stats update in real-time

---

### CF-007: Contract History

**User Story**: As a user, I want to see all my past contract analyses.

**Requirements**:
- [ ] List all contracts for current user
- [ ] Show: filename, upload date, status, agreement type
- [ ] Sort by: most recent first
- [ ] Filter by: agreement type, date range
- [ ] Search by: filename
- [ ] Click to view analysis
- [ ] Delete contract (soft delete)
- [ ] Pagination (20 per page)

**UI Components**:
- History page with list
- Search bar
- Filter dropdowns
- Contract card (thumbnail, filename, date, type)
- Delete button (with confirmation)

**Acceptance Criteria**:
- User sees all their contracts
- User can search by filename
- User can filter by type
- User can delete contract
- Pagination works (no crashes with 100+ contracts)

---

## Advanced Features (P1 - Should Have)

### AF-001: Renewal & Deadline Radar

**User Story**: As a user, I want automated reminders for contract deadlines.

**Requirements**:
- [ ] Extract all deadlines from contract:
  - Renewal windows
  - Notice periods
  - Payment due dates
  - Termination deadlines
  - Option exercise windows
- [ ] Store deadlines in `deadlines` table
- [ ] Display on Deadlines page:
  - Timeline view
  - List view (upcoming first)
  - Filter by type
- [ ] Show upcoming deadlines (next 30 days) on dashboard
- [ ] Export to calendar (.ics file)
- [ ] Email reminders (optional, Premium feature)
- [ ] Mark deadlines as "completed"

**UI Components**:
- Deadlines page
- Timeline component (visual calendar)
- Deadline cards
- "Add to calendar" button
- Reminder settings (Premium)

**Acceptance Criteria**:
- Deadlines extracted correctly ≥85% accuracy
- Calendar export works (Google, Apple, Outlook)
- Upcoming deadlines visible on dashboard
- User can mark deadlines complete

---

### AF-002: Cross-Document Consistency Check

**User Story**: As a user, I want to upload multiple related contracts and detect conflicts.

**Requirements**:
- [ ] Upload multiple files (1 primary + N context)
- [ ] Create `document_set`
- [ ] Analyze all documents
- [ ] Detect conflicts:
  - **Term conflicts**: Different values for same term (e.g., different notice periods)
  - **Missing exhibits**: Referenced but not uploaded
  - **Overrides**: SOW overrides MSA
  - **Inconsistencies**: Contradictory clauses
- [ ] Categorize severity: Critical / High / Medium / Low
- [ ] Show "source of truth" for each term
- [ ] Display conflicts list (sorted by severity)

**Output**:
```json
{
  "conflicts": [
    {
      "severity": "critical",
      "category": "term_conflict",
      "description": "MSA says 30-day notice; SOW says 14-day notice",
      "source_of_truth": "SOW (overrides MSA per Section 12)",
      "contracts": ["MSA.pdf", "SOW_2024.pdf"]
    },
    {
      "severity": "high",
      "category": "missing_exhibit",
      "description": "Exhibit A (Data Processing Agreement) referenced but not uploaded",
      "recommendation": "Upload Exhibit A for complete review"
    }
  ]
}
```

**UI Components**:
- Multi-file upload (drag multiple files)
- Document set page
- Conflict cards (severity badges)
- "Source of truth" indicators
- Side-by-side comparison

**Acceptance Criteria**:
- User can upload up to 5 related documents
- Conflicts detected ≥75% accuracy
- Source of truth identified correctly
- Conflicts sorted by severity

---

### AF-003: Lawyer Handoff Pack

**User Story**: As a user, I want to export a comprehensive package to share with my lawyer.

**Requirements**:
- [ ] One-click "Create Lawyer Pack" button
- [ ] Generate PDF/DOCX with:
  - Executive summary (1 page)
  - Extracted fields table
  - Full analysis (all sections)
  - Highlighted concerns
  - List of open questions
  - Redline suggestions (if applicable)
- [ ] Professional formatting
- [ ] Include original contract (as appendix)
- [ ] Option to email directly to lawyer

**Output Sections**:
1. **Cover Page**:
   - Contract name
   - Analysis date
   - Prepared for: [user's name]
2. **Executive Summary** (1 page):
   - Screening result
   - Top 3 concerns
   - Top 3 recommendations
3. **Key Terms Table**:
   - Parties, dates, amounts, notices
4. **Detailed Analysis**:
   - All sections from results page
5. **Questions for Counsel**:
   - Auto-generated based on risks
6. **Appendix**:
   - Original contract PDF

**UI Components**:
- "Export Lawyer Pack" button on results page
- Format selector (PDF or DOCX)
- Email form (optional)
- Preview before export

**Acceptance Criteria**:
- Lawyer pack generates in <10 seconds
- All sections included
- Professional formatting
- Readable by non-technical lawyers
- Email delivery works

---

### AF-004: Privacy "Do-Not-Store" Mode

**User Story**: As a privacy-conscious user, I want to analyze contracts without storing them.

**Requirements**:
- [ ] Toggle on upload page: "Don't store this analysis"
- [ ] If enabled:
  - Skip database storage (except minimal audit log)
  - Process in-memory only
  - Scrub text after analysis complete
  - Redact PII in exports
  - Auto-delete after 24 hours
- [ ] Show privacy badge: "This analysis will not be saved"
- [ ] User can still download results
- [ ] Cannot view later (no history entry)

**UI Components**:
- Privacy toggle on upload
- Badge showing privacy mode active
- Warning: "Analysis will not be saved"
- Download results button (expires after session)

**Acceptance Criteria**:
- Toggle activates do-not-store mode
- No data saved to database (except audit)
- Text scrubbed after analysis
- User cannot retrieve later
- Download works during session

---

### AF-005: Multilingual Mirror View

**User Story**: As a user with a foreign-language contract, I want to see original and translation side-by-side.

**Requirements**:
- [ ] Side-by-side layout (original | translation)
- [ ] Sentence alignment (paragraph-level)
- [ ] Highlight differences from source
- [ ] Sync scrolling (scroll one side, other follows)
- [ ] Toggle between languages
- [ ] Show legal terms in both languages
- [ ] Translation quality indicator

**UI Components**:
- Split-pane view
- Language toggle (top)
- Sync scroll
- Highlight differences
- Glossary popover (hover on legal term)

**Acceptance Criteria**:
- Side-by-side layout works on tablet+
- Scrolling synced correctly
- Sentences aligned (visual inspection)
- User can toggle between views

---

## Enhanced Features (P2 - Nice to Have)

### EF-001: Contract Type Detection Training

**User Story**: As the system, I want to improve classification accuracy over time.

**Requirements**:
- [ ] Type-specific prompts per language
- [ ] Load appropriate prompt based on detected type
- [ ] Store classification confidence
- [ ] User can correct if wrong
- [ ] Feedback loop: use corrections to improve

**Prompts**:
- `prompts/lease_en.txt`, `prompts/lease_ru.txt`, etc.
- `prompts/nda_en.txt`, `prompts/nda_ru.txt`, etc.
- `prompts/employment_en.txt`, etc.

**Acceptance Criteria**:
- Type-specific prompts improve accuracy by ≥10%
- User can correct classification
- Corrections stored for training

---

### EF-002: "Explain Like I'm 5" Mode

**User Story**: As a non-lawyer, I want complex legal terms explained in simple language.

**Requirements**:
- [ ] Toggle on results page: "Simplify language"
- [ ] If enabled:
  - Rewrite obligations in simple terms
  - Replace legal jargon with everyday words
  - Add examples
  - Use short sentences
- [ ] Show both versions (original + simplified)
- [ ] Tooltips on legal terms

**Example**:
```
Original: "Lessee shall indemnify and hold harmless Lessor from
any claims arising from Lessee's use of the premises."

Simplified: "If someone sues the landlord because of something
you did, you have to pay for the landlord's legal costs."
```

**Acceptance Criteria**:
- Toggle activates ELI5 mode
- Legal terms replaced with simple words
- Examples provided where helpful
- Sentence length ≤15 words

---

### EF-003: Comparison Feature

**User Story**: As a user, I want to compare two contracts to see which is better.

**Requirements**:
- [ ] Select 2 contracts from history
- [ ] Side-by-side comparison
- [ ] Highlight differences:
  - Terms that changed
  - Better/worse for user
  - New clauses
  - Removed clauses
- [ ] Summary: "Contract B is more favorable because..."
- [ ] Negotiation points: "Ask to change X to match Contract A"

**UI Components**:
- "Compare" button on history page
- Contract selector (2 checkboxes)
- Comparison view (split pane)
- Diff highlights (green = better, red = worse, yellow = changed)
- Recommendation card

**Acceptance Criteria**:
- User can select 2 contracts
- Differences highlighted correctly
- Summary explains which is better
- Negotiation points actionable

---

### EF-004: Red Flag Alerts

**User Story**: As a user, I want critical issues prominently displayed.

**Requirements**:
- [ ] Detect critical issues:
  - Unlimited liability
  - Unilateral changes without notice
  - Auto-renewal without opt-out
  - Unreasonable penalties
  - Data rights violations
- [ ] Show red flag alert at top of results (before other content)
- [ ] Icon + severity + description + action
- [ ] Link to relevant section

**UI**:
```
┌─────────────────────────────────────────┐
│ ⛔ CRITICAL ISSUE DETECTED               │
│                                          │
│ Unlimited Liability                      │
│ You're responsible for all damages with  │
│ no cap, even if not your fault.          │
│                                          │
│ → Recommended action:                    │
│ Add a liability cap (e.g., 2× annual fee)│
│                                          │
│ [View Details] [Get Help]                │
└─────────────────────────────────────────┘
```

**Acceptance Criteria**:
- Critical issues detected ≥90% of time
- Alert shown prominently
- Action recommended
- No false positives (avoid alarm fatigue)

---

### EF-005: Multiple Export Options

**User Story**: As a user, I want to export results in multiple formats.

**Requirements**:
- [ ] **PDF**: Styled, professional, printable
- [ ] **DOCX**: Editable (for adding notes)
- [ ] **Email**: Send to lawyer or self
- [ ] **Google Docs**: One-click save to Drive (OAuth)
- [ ] **Markdown**: For developers
- [ ] **JSON**: For programmatic access

**UI Components**:
- Export dropdown on results page
- Format selector
- Email form (if email selected)
- Google auth (if Google Docs selected)

**Acceptance Criteria**:
- All formats generate correctly
- PDF is print-friendly
- DOCX is editable
- Email delivers within 1 minute
- Google Docs integration works

---

### EF-006: Confidence Calibration

**User Story**: As the system, I want to learn from user feedback to improve accuracy.

**Requirements**:
- [ ] Feedback form on each section:
  - "Was this accurate?" (Yes / Partly / No)
  - "What was wrong?" (free text)
- [ ] Store feedback in `feedback` table
- [ ] Analyze patterns:
  - Which sections are often marked "No"?
  - Which contract types have low accuracy?
  - Which languages need improvement?
- [ ] Use feedback to:
  - Adjust confidence scores
  - Improve prompts
  - Identify training needs
- [ ] Dashboard (admin only): feedback stats

**UI Components**:
- Feedback buttons at bottom of each section
- Feedback form (appears on click)
- Thank you message after submission

**Acceptance Criteria**:
- User can submit feedback on any section
- Feedback stored in database
- Patterns identified (manual analysis for MVP)
- Confidence scores adjusted based on feedback

---

## Monetization Features (P0)

### MF-001: Stripe Subscription

**User Story**: As a Premium user, I want to subscribe for unlimited analyses.

**Requirements**:
- [ ] Stripe account setup
- [ ] Products created:
  - Premium Monthly ($9.99/month)
  - Premium Annual ($99/year)
- [ ] Checkout session endpoint
- [ ] Redirect to Stripe Checkout
- [ ] Webhook handler (payment events)
- [ ] Update user tier on success
- [ ] Customer portal (manage subscription)
- [ ] Cancel subscription
- [ ] Invoice emails

**Flow**:
1. User clicks "Upgrade to Premium"
2. Backend creates Checkout session
3. User redirected to Stripe
4. User enters payment info
5. Stripe processes payment
6. Webhook received
7. User tier updated to "premium"
8. User redirected back with success message

**Acceptance Criteria**:
- User can subscribe successfully
- User tier updated immediately
- User can manage subscription (cancel, update card)
- Invoices sent via email
- Webhooks handled correctly (no missed events)

---

### MF-002: Advertisement Integration

**User Story**: As a free user, I see ads on some pages but not on results pages.

**Requirements**:
- [ ] Google AdSense account setup
- [ ] Ad units created:
  - Banner ad (landing page footer)
  - Sidebar ad (history page)
- [ ] Conditional rendering: free users only
- [ ] Premium users: no ads ever
- [ ] Ad blocker detection (optional)

**Placement**:
- ✅ Landing page footer
- ✅ History page sidebar
- ❌ Upload page
- ❌ Results page
- ❌ Any decision-making page

**Acceptance Criteria**:
- Ads show for free users
- Ads hidden for Premium users
- Ads never appear on results pages
- Revenue tracked (AdSense dashboard)

---

## GDPR Compliance Features (P0)

### GF-001: Data Export

**User Story**: As a user, I want to export all my data.

**Requirements**:
- [ ] Endpoint: GET /api/account/export
- [ ] Generate JSON with:
  - User profile
  - All contracts
  - All analyses
  - All feedback
  - Subscription info
- [ ] Download as .json file
- [ ] Complete within 10 seconds

**Acceptance Criteria**:
- User can download all data
- JSON is well-formatted
- All data included
- Download completes quickly

---

### GF-002: Account Deletion

**User Story**: As a user, I want to permanently delete my account.

**Requirements**:
- [ ] Endpoint: DELETE /api/account
- [ ] Confirmation required (type "DELETE" to confirm)
- [ ] Delete all user data:
  - User record
  - Contracts (cascade)
  - Analyses (cascade)
  - Deadlines (cascade)
  - Document sets (cascade)
  - Feedback (cascade)
- [ ] Delete files from storage
- [ ] Cancel Stripe subscription (if active)
- [ ] Redirect to goodbye page

**Acceptance Criteria**:
- User must confirm before deletion
- All data deleted permanently
- Files deleted from storage
- Subscription canceled
- User cannot log in after deletion

---

## Technical Quality Requirements (All Features)

### Performance
- [ ] P95 latency <500ms (API endpoints)
- [ ] P95 analysis time <30s (full analysis)
- [ ] Bundle size <250KB (gzipped)
- [ ] Lighthouse score >90 (mobile)

### Security
- [ ] All passwords hashed (bcrypt)
- [ ] JWT tokens expire (7 days)
- [ ] Rate limiting (100 req/min)
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (sanitized inputs)
- [ ] CSRF protection (SameSite cookies)
- [ ] File upload validation (type + size)

### Accessibility
- [ ] WCAG 2.1 AA compliant
- [ ] Keyboard navigation works
- [ ] Screen reader friendly
- [ ] Color contrast ≥4.5:1
- [ ] Touch targets ≥48×48px

### Reliability
- [ ] Error rate <1%
- [ ] Uptime ≥99% (SLA)
- [ ] All errors logged (Sentry)
- [ ] Automated backups (daily)
- [ ] Restore tested (monthly)

---

## Feature Priority Summary

**P0 (Must Have for MVP)**:
- Authentication
- Contract upload
- Analysis (Step 1 + 2)
- Results display
- Trial system (3 free)
- Contract history
- Stripe subscriptions
- GDPR (export, delete)

**P1 (Should Have, Add Week 5-6)**:
- Deadline Radar
- Cross-Document Check
- Lawyer Handoff Pack
- Privacy Mode
- Multilingual Mirror View

**P2 (Nice to Have, Post-Launch)**:
- Contract Type Training
- ELI5 Mode
- Comparison Feature
- Red Flag Alerts
- Multiple Export Options
- Confidence Calibration

---

**Last Updated**: 2025-11-06
