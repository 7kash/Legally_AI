# Legally AI - Branding Guidelines

## Brand Philosophy: "The Disneyland Layer"

**Core Principle**: Fun and easy on the surface, professional and accurate underneath.

Legal analysis is intimidating. Most people avoid reading contracts because they're dense, boring, and scary. We make it approachable without sacrificing professionalism.

**Inspiration**:
- **Disneyland**: Magical experience (surface) + engineering excellence (underneath)
- **Stripe**: Serious payments (underneath) + delightful DX (surface)
- **Notion**: Powerful database (underneath) + friendly UI (surface)
- **Linear**: Complex project management (underneath) + beautiful UX (surface)

---

## Brand Personality

### We Are
- 🎯 **Clear**: No legal jargon, plain language
- 🤝 **Helpful**: Like a knowledgeable friend, not a stuffy lawyer
- 🎨 **Delightful**: Smooth interactions, thoughtful micro-copy
- 🔒 **Trustworthy**: Accurate, honest, transparent about limitations
- 🌍 **Inclusive**: Works for everyone, any language, any device

### We Are NOT
- ❌ Overly formal or intimidating
- ❌ Condescending or patronizing
- ❌ Cutesy or unprofessional
- ❌ Overpromising or misleading
- ❌ Boring or bureaucratic

---

## Voice & Tone

### Voice (Consistent)
- **Conversational**: "Let's look at your contract" not "Contract analysis initiated"
- **Direct**: Short sentences, active voice
- **Friendly**: Warm but professional
- **Honest**: Transparent about what we can and can't do

### Tone (Context-Dependent)

**Uploading**:
- Encouraging: "Upload your contract and we'll help you understand it"
- Simple: "PDF or DOCX, any language"

**Analyzing** (Progress):
- Reassuring: "Analyzing your contract... this usually takes about 20 seconds"
- Transparent: "Reading document → Checking terms → Finding risks"

**Results** (Good news):
- Calm: "No major issues detected"
- Helpful: "Here's what you need to know"

**Results** (Concerns):
- Clear but not alarming: "We found a few things to check"
- Actionable: "Here's what you can do"

**Errors**:
- Apologetic: "Sorry, something went wrong"
- Helpful: "Try uploading again, or contact us if the problem continues"

---

## Writing Guidelines

### General Rules
1. **Short sentences**: Max 20 words per sentence
2. **Active voice**: "We found 3 risks" not "3 risks were found"
3. **Second person**: "You" not "the user"
4. **Present tense**: "Your contract says..." not "Your contract said..."
5. **No jargon**: "End date" not "Termination provision"
6. **One idea per sentence**: Don't combine multiple concepts

### Specific Cases

**Disclaimers** (Must be clear, not scary):
```
❌ "THIS IS NOT LEGAL ADVICE. WE MAKE NO WARRANTIES..."
✅ "This is an AI-powered review, not legal advice. For important
    contracts, consider speaking with a lawyer."
```

**Error Messages** (Helpful, not blaming):
```
❌ "Invalid file format"
✅ "We can only read PDF and DOCX files. Try converting your file first."
```

**Empty States** (Encouraging, not sad):
```
❌ "No contracts found"
✅ "Ready to analyze your first contract? Upload one to get started."
```

**Success Messages** (Celebratory but not over-the-top):
```
❌ "SUCCESS!!! 🎉🎉🎉"
✅ "Analysis complete. Let's review your contract."
```

---

## Visual Design

### Color Palette

**Primary Colors**:
- **Brand Blue**: `#2563EB` (Trust, stability)
- **Dark Blue**: `#1E40AF` (Professional, serious)
- **Light Blue**: `#DBEAFE` (Calm, approachable)

**Accent Colors**:
- **Success Green**: `#10B981` (Positive outcomes)
- **Warning Yellow**: `#F59E0B` (Caution, attention)
- **Danger Red**: `#EF4444` (Critical issues)
- **Info Purple**: `#8B5CF6` (Additional info, tips)

**Neutrals**:
- **Text**: `#111827` (Almost black)
- **Secondary Text**: `#6B7280` (Gray)
- **Border**: `#E5E7EB` (Light gray)
- **Background**: `#F9FAFB` (Off-white)
- **White**: `#FFFFFF`

**Dark Mode** (Optional):
- **Background**: `#111827`
- **Surface**: `#1F2937`
- **Text**: `#F9FAFB`
- **Border**: `#374151`

### Typography

**Font Family**:
- **Primary**: Inter (clean, modern, multilingual support)
- **Fallback**: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif
- **Monospace** (for quotes, code): "Fira Code", monospace

**Font Sizes** (Tailwind scale):
- **H1**: `text-4xl` (36px) — Page titles
- **H2**: `text-2xl` (24px) — Section headers
- **H3**: `text-xl` (20px) — Subsections
- **Body**: `text-base` (16px) — Main content
- **Small**: `text-sm` (14px) — Secondary info
- **Tiny**: `text-xs` (12px) — Labels, captions

**Font Weights**:
- **Regular**: 400 — Body text
- **Medium**: 500 — Emphasis
- **Semibold**: 600 — Headings
- **Bold**: 700 — Alerts, CTAs

### Spacing

**Consistent Scale** (Tailwind):
- `space-2` (8px) — Tight elements
- `space-4` (16px) — Standard gap
- `space-6` (24px) — Section spacing
- `space-8` (32px) — Large gaps
- `space-12` (48px) — Page sections

### Icons

**Style**: Outline (Heroicons or Lucide)
**Size**: 20px (default), 24px (headers), 16px (inline)
**Usage**:
- ✅ Use for common actions (upload, download, delete)
- ✅ Use for status (success, warning, error)
- ❌ Don't overuse (text often clearer)
- ❌ Don't use for decoration

### Buttons

**Primary** (Main actions):
- Background: Brand Blue
- Text: White
- Hover: Dark Blue
- Example: "Analyze Contract"

**Secondary** (Alternative actions):
- Background: Light Blue
- Text: Brand Blue
- Hover: Darker border
- Example: "View Sample"

**Danger** (Destructive):
- Background: Danger Red
- Text: White
- Hover: Darker red
- Example: "Delete Account"

**Ghost** (Tertiary):
- Background: Transparent
- Text: Brand Blue
- Hover: Light Blue background
- Example: "Cancel"

### Cards

```
┌────────────────────────────────┐
│ Title (semibold, text-lg)      │
│                                 │
│ Content (regular, text-base)   │
│ • Bullet points                 │
│ • Clear hierarchy               │
│                                 │
│ [Action Button]                 │
└────────────────────────────────┘

- Border: 1px solid #E5E7EB
- Border Radius: 8px
- Padding: 24px
- Shadow: Subtle (0 1px 3px rgba(0,0,0,0.1))
- Hover: Lift slightly (shadow increase)
```

---

## UI Patterns

### Confidence Badges

```
High Confidence       [Green badge]  • Complete document
                                     • Clear terms

Medium Confidence     [Yellow badge] • Some missing info
                                     • Minor concerns

Low Confidence        [Red badge]    • Poor quality scan
                                     • Missing documents
```

### Risk Alerts

**Critical**:
```
┌─────────────────────────────────────────┐
│ ⛔ CRITICAL ISSUE                        │
│                                          │
│ You have unlimited liability for damages│
│                                          │
│ → Add a liability cap clause            │
└─────────────────────────────────────────┘
Red background, white text, urgent
```

**High**:
```
┌─────────────────────────────────────────┐
│ ⚠️ Check This                           │
│                                          │
│ Provider can change terms anytime       │
│                                          │
│ → Request 30-day notice requirement     │
└─────────────────────────────────────────┘
Yellow background, dark text, important
```

**Medium/Low**:
```
• Normal bullet points
• Info icon available for details
```

### Progress Indicators

**Analyzing**:
```
[████████░░░░] 60%

Reading document... ✓
Analyzing terms... (current)
Checking for risks...
```

- Show current step
- Show progress bar
- Estimated time remaining (optional)

### Empty States

```
┌─────────────────────────────────────────┐
│            [Icon: Document]              │
│                                          │
│   Ready to analyze your first contract? │
│                                          │
│         [Upload Contract] button         │
│                                          │
│   Supports PDF and DOCX in any language │
└─────────────────────────────────────────┘

Centered, friendly, actionable
```

---

## Mobile-Specific Guidelines

### Touch Targets
- **Minimum size**: 48×48px (WCAG 2.1 AAA)
- **Spacing**: 8px between interactive elements
- **Tappable area**: Padding around text/icons

### Navigation
- **Bottom nav on mobile**: 5 items max
  - 📄 Contracts
  - ⏰ Deadlines
  - 👤 Account
- **Sidebar on desktop**: More options available

### Typography
- **Minimum font size**: 16px (prevents zoom on iOS)
- **Line height**: 1.5 (readability)
- **Contrast**: WCAG AA minimum (4.5:1)

### Forms
- **Input type**: Proper keyboard (email, tel, number)
- **Labels**: Above fields, not placeholders
- **Errors**: Inline, below field, clear message

---

## Accessibility

### WCAG 2.1 AA Compliance

**Color Contrast**:
- Text: ≥4.5:1 against background
- Large text (18pt+): ≥3:1
- Interactive elements: ≥3:1

**Keyboard Navigation**:
- All interactive elements focusable
- Visible focus indicator
- Logical tab order

**Screen Readers**:
- Semantic HTML (h1, h2, nav, main, etc.)
- ARIA labels where needed
- Alt text for images
- Form labels associated with inputs

**Motion**:
- Respect `prefers-reduced-motion`
- No auto-playing animations
- Pause/stop controls for movement

**Language**:
- Proper `lang` attribute per section
- Clear, simple language (no idioms)

---

## Content Principles

### Disclaimers

**Always Include**:
```
Important limits: This is an AI-powered informational screening
— not legal advice, not a law-firm review, and it does not create
an attorney–client relationship. We looked only at the text you
provided and did not verify facts, identities, authority to sign,
ownership, required formalities, or compliance with local law.
Attachments, the governing-language version, or later edits can
change the result. Laws differ by country and state, so
enforceability may vary. Don't rely on this summary alone; for
meaningful stakes, read everything and consider speaking with
a qualified lawyer.
```

**Placement**:
- On every results page
- Before user makes decisions
- In exports (PDF, DOCX)

### Risk Language

**Avoid**:
- ❌ "This is illegal"
- ❌ "You must do X"
- ❌ "This will fail in court"
- ❌ "Safe to sign"

**Use**:
- ✅ "May be unenforceable"
- ✅ "Consider asking for..."
- ✅ "High-risk indicators detected"
- ✅ "Appears to conflict with..."

### Confidence Language

**High Confidence**:
- "Based on the complete document..."
- "We found..."
- "The agreement states..."

**Medium Confidence**:
- "Based on what we reviewed..."
- "It appears..."
- "Some details are unclear..."

**Low Confidence**:
- "We can't reliably assess..."
- "The document quality is too poor..."
- "Please provide a clearer copy..."

---

## Multilingual Considerations

### Translation Quality
- Professional tone maintained across languages
- Legal terminology researched (not literal translation)
- Cultural context preserved
- Examples relevant to jurisdiction

### Language Selector
```
🌐 English  ▼

Dropdown shows:
• English
• Русский (Russian)
• Српски (Serbian)
• Français (French)
```

### RTL Support (Future)
- If adding Arabic, Hebrew, Urdu
- Mirror layout (nav on right, etc.)
- Proper text alignment
- Test thoroughly

---

## Marketing Voice

### Landing Page
**Headline**: Clear value proposition
```
❌ "AI-Powered Legal Document Analysis Platform"
✅ "Understand any contract in minutes"
```

**Subheadline**: Who it's for
```
"Get AI-powered analysis of contracts in Russian, Serbian,
French, or English — no law degree required."
```

**CTA**:
```
Primary: "Analyze Your First Contract" (bold, clear)
Secondary: "See a Sample Analysis" (less prominent)
```

### Social Media
- **Tone**: Helpful, educational, not salesy
- **Content**: Tips, examples, success stories
- **Hashtags**: #LegalTech #ContractReview #SmallBusiness

---

## Examples

### Good vs Bad Copy

**Upload Page**:
```
❌ "Please upload a valid contract file in PDF or DOCX format
    for analysis processing."

✅ "Upload your contract (PDF or DOCX) and we'll help you
    understand it."
```

**Error**:
```
❌ "Error 500: Internal server error"

✅ "Sorry, something went wrong on our end. Please try again,
    or contact us if the issue persists."
```

**Results**:
```
❌ "Analysis complete. Results displayed below."

✅ "Here's what we found in your contract:"
```

**Empty Deadlines**:
```
❌ "No deadlines."

✅ "No upcoming deadlines. We'll notify you when dates approach."
```

---

## Logo & Wordmark

### Logo Concept Ideas
1. **Contract + Magnifying Glass**: Classic, but clear
2. **Document + Checkmark**: Reviewed and approved
3. **Scales + Globe**: Justice + international
4. **Shield + Document**: Protection through knowledge

**Requirements**:
- Works in monochrome
- Readable at 16×16px (favicon)
- Distinctive silhouette
- Appropriate for legal context

### Wordmark
- **Font**: Inter Bold or custom
- **Style**: Clean, modern, professional
- **Treatment**: All caps or sentence case?
  - "LEGALLY AI" (stronger, but formal)
  - "Legally AI" (friendlier, approachable) ✅

---

## Launch Materials

### Social Media Announcement
```
🎉 Introducing Legally AI

Upload your contract in Russian, Serbian, French, or English
and get an instant AI-powered analysis.

✅ Understand your obligations
✅ Identify potential risks
✅ Get actionable recommendations

Try 3 analyses free: [link]
```

### Product Hunt Launch
```
Title: Legally AI – Understand any contract in minutes

Tagline: AI-powered contract analysis in 4 languages

Description:
Most people don't read contracts because they're confusing and
intimidating. Legally AI uses AI to break down agreements into
simple terms.

Upload a contract (PDF/DOCX) in Russian, Serbian, French, or
English and get:
• Clear summary of what you're agreeing to
• List of your obligations and rights
• Risk flags and what to negotiate
• Deadline reminders

Perfect for freelancers, small businesses, and anyone dealing
with foreign-language contracts.

First 3 analyses free, then $9.99/month for unlimited.
```

---

**Last Updated**: 2025-11-06
