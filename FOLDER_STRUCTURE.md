# Folder Structure - Legally AI Project

This document explains the organization of the Legally AI project, including local paths, git setup, and file purposes.

---

## Local Directory Structure

```
/Users/ekaterinamatyushina/Legally_AI/          # Main project (GitHub)
│
├── .git/                                        # Git repository (GitHub)
│
├── docs/                                        # Project documentation
│   ├── architecture.md
│   ├── decisions.md
│   ├── mvp-features.md
│   └── ...
│
├── prototype/                                   # HF Spaces deployment (separate git repo)
│   ├── .git/                                    # Separate git repository (HF)
│   ├── venv/                                    # Virtual environment (NOT in git)
│   ├── app.py                                   # Main Gradio application
│   ├── requirements.txt                         # Python dependencies
│   ├── packages.txt                             # System dependencies (tesseract, poppler)
│   ├── README.md                                # HF Space description
│   ├── QUICKSTART.md                            # Deployment instructions
│   ├── .env.example                             # Example environment variables
│   └── src/                                     # Source code
│       ├── __init__.py
│       ├── constants.py                         # UI strings, screening results, config
│       ├── parsers.py                           # PDF/DOCX parsing + OCR
│       ├── language.py                          # Language detection
│       ├── quality.py                           # Quality & confidence scoring
│       ├── llm_router.py                        # Groq API integration
│       ├── step1_preparation.py                 # Step 1 analysis
│       ├── step2_analysis.py                    # Step 2 analysis
│       ├── formatter.py                         # Output formatting
│       ├── agreement_types_catalog.txt          # 48 agreement types reference
│       └── prompts/
│           ├── preparation_en.txt               # Step 1 prompt
│           └── analysis_en.txt                  # Step 2 prompt
│
├── backend/                                     # FastAPI production backend
│   ├── app/                                     # Application code
│   │   ├── api/                                 # API endpoints
│   │   │   ├── auth.py                          # Authentication endpoints
│   │   │   ├── contracts.py                     # Contract upload/management
│   │   │   └── analyses.py                      # Analysis endpoints + SSE
│   │   ├── core/                                # Core configuration
│   │   │   ├── config.py                        # Settings
│   │   │   ├── security.py                      # JWT, password hashing
│   │   │   └── database.py                      # DB connection
│   │   ├── models/                              # SQLAlchemy models
│   │   │   ├── user.py
│   │   │   ├── contract.py
│   │   │   └── analysis.py
│   │   ├── schemas/                             # Pydantic schemas
│   │   │   ├── user.py
│   │   │   ├── contract.py
│   │   │   └── analysis.py
│   │   ├── services/                            # Business logic
│   │   │   ├── auth_service.py
│   │   │   ├── contract_service.py
│   │   │   └── analysis_service.py
│   │   ├── tasks/                               # Celery tasks
│   │   │   └── analyze_contract.py
│   │   └── main.py                              # FastAPI app entry point
│   ├── alembic/                                 # Database migrations
│   │   └── versions/
│   ├── tests/                                   # Pytest tests
│   ├── requirements.txt                         # Python dependencies
│   ├── alembic.ini                              # Alembic config
│   ├── .env.example                             # Environment variables template
│   └── README.md                                # Backend documentation
│
├── frontend/                                    # Nuxt 3 production frontend
│   ├── .nuxt/                                   # Auto-generated (gitignored)
│   ├── node_modules/                            # Dependencies (gitignored)
│   ├── public/                                  # Static assets
│   │   └── manifest.json                        # PWA manifest
│   ├── assets/                                  # Compiled assets
│   │   └── styles/
│   │       ├── main.scss                        # Global styles
│   │       ├── variables.scss                   # CSS variables & design tokens
│   │       └── tailwind.css                     # Tailwind entry point
│   ├── components/                              # Vue components
│   │   ├── analysis/
│   │   │   ├── AnalysisSection.vue
│   │   │   └── FileUpload.vue
│   │   └── common/
│   │       ├── NotificationContainer.vue
│   │       ├── ThemeToggle.vue
│   │       ├── LanguageSwitcher.vue
│   │       └── SkeletonLoader.vue
│   ├── composables/                             # Composition functions
│   │   ├── useDarkMode.ts
│   │   └── useNotifications.ts
│   ├── layouts/                                 # Layout components
│   │   └── default.vue
│   ├── middleware/                              # Route middleware
│   │   ├── auth.ts                              # Protected routes
│   │   └── guest.ts                             # Public-only routes
│   ├── pages/                                   # File-based routing
│   │   ├── index.vue                            # Landing page
│   │   ├── login.vue                            # Login
│   │   ├── register.vue                         # Registration
│   │   ├── upload.vue                           # Upload contracts
│   │   ├── history.vue                          # Past analyses
│   │   ├── account.vue                          # User settings
│   │   ├── analysis/
│   │   │   └── [id].vue                         # Analysis results (SSE)
│   │   └── auth/
│   │       ├── forgot-password.vue
│   │       ├── reset-password.vue
│   │       └── verify-email.vue
│   ├── plugins/                                 # Nuxt plugins
│   │   ├── auth.client.ts                       # Auth initialization
│   │   └── analytics.client.ts                  # Analytics tracking
│   ├── stores/                                  # Pinia stores
│   │   ├── auth.ts                              # Authentication state
│   │   ├── contracts.ts                         # Contract uploads
│   │   └── analyses.ts                          # Analysis results & SSE
│   ├── utils/                                   # Utility functions
│   │   └── exportToPDF.ts                       # PDF export helper
│   ├── types/                                   # TypeScript types
│   │   └── index.ts
│   ├── nuxt.config.ts                           # Nuxt configuration
│   ├── tailwind.config.ts                       # Tailwind configuration
│   ├── i18n.config.ts                           # i18n configuration
│   ├── pwa.config.ts                            # PWA configuration
│   ├── tsconfig.json                            # TypeScript config
│   ├── vitest.config.ts                         # Vitest config
│   ├── playwright.config.ts                     # Playwright config
│   ├── package.json                             # Node dependencies
│   └── README.md                                # Frontend documentation
│
├── DEPLOYMENT_GUIDE.md                          # How to deploy (this is you!)
├── FOLDER_STRUCTURE.md                          # This file
├── Claude.md                                    # Session context
├── plan.md                                      # Development roadmap
├── progress.md                                  # Progress tracking
├── decisions.md                                 # Technical decisions
├── branding.md                                  # Branding guidelines
├── architecture.md                              # System architecture
└── README.md                                    # Main project README

```

---

## Git Repository Setup

### Repository 1: Main Project (GitHub)

```
Location:    /Users/ekaterinamatyushina/Legally_AI
Remote:      origin → https://github.com/7kash/Legally_AI
Purpose:     Full project including docs, planning, and prototype code
```

**What's tracked:**
- All documentation files (`.md` files)
- Prototype source code
- Planning documents
- Architecture decisions

**NOT tracked:**
- Virtual environments (`venv/`)
- Environment files (`.env`)
- Python cache (`__pycache__/`)
- Mac system files (`.DS_Store`)

### Repository 2: Prototype (Hugging Face Spaces)

```
Location:    /Users/ekaterinamatyushina/Legally_AI/prototype
Remote:      hf → https://huggingface.co/spaces/7Kash-FluffyHedgehog/Legally_AI
Purpose:     Live deployment of the contract analysis app
```

**What's tracked:**
- `app.py` - Main application
- `requirements.txt` - Python dependencies
- `packages.txt` - System dependencies
- `src/` - All source code
- `README.md` - Space description
- `QUICKSTART.md` - Setup guide
- `.env.example` - Example env vars

**NOT tracked:**
- `venv/` - Virtual environment
- `.env` - Actual secrets/API keys
- `__pycache__/` - Python cache

---

## File Purposes

### Root Level Documentation

| File | Purpose | Audience |
|------|---------|----------|
| `Claude.md` | Session context for Claude | AI Assistant |
| `plan.md` | Development roadmap & timeline | Team |
| `progress.md` | Progress tracking & metrics | Team |
| `decisions.md` | Technical decisions & rationale | Developers |
| `architecture.md` | System architecture | Developers |
| `branding.md` | Branding & UX guidelines | Designers |
| `mvp-features.md` | Feature specifications | Product |
| `DEPLOYMENT_GUIDE.md` | GitHub → HF deployment | You (Ekaterina) |
| `FOLDER_STRUCTURE.md` | This file | You (Ekaterina) |

### Prototype Application Files

| File | Purpose | When to Edit |
|------|---------|--------------|
| `app.py` | Main Gradio UI & workflow | Changing UI or flow |
| `requirements.txt` | Python dependencies | Adding/updating libraries |
| `packages.txt` | System packages | Need system tools (OCR, etc.) |
| `README.md` | HF Space description | Update space info |
| `QUICKSTART.md` | Setup instructions | Deployment steps change |
| `.env.example` | Example secrets | New env vars needed |

### Source Code (`src/`)

| File | Purpose | Contains |
|------|---------|----------|
| `constants.py` | Configuration & strings | UI text (4 languages), screening results, thresholds, 48 agreement types |
| `parsers.py` | Document extraction | PDF text extraction, DOCX table extraction, OCR for scanned PDFs |
| `language.py` | Language detection | Detect Russian/Serbian/French/English, jurisdiction detection |
| `quality.py` | Quality scoring | Quality score calculation, confidence levels, hard gates |
| `llm_router.py` | LLM API client | Groq API integration, JSON parsing, error handling |
| `step1_preparation.py` | Preparation analysis | Extract metadata, detect type, assess negotiability |
| `step2_analysis.py` | Text analysis | Extract obligations, rights, risks, payment terms |
| `formatter.py` | Output formatting | Format markdown output for Gradio, multilingual support |
| `agreement_types_catalog.txt` | Agreement types | 48 types with negotiability defaults & key fields |

### Prompts (`src/prompts/`)

| File | Purpose | Contains |
|------|---------|----------|
| `preparation_en.txt` | Step 1 LLM prompt | 10-step preparation checklist, agreement types catalog, negotiability guidance |
| `analysis_en.txt` | Step 2 LLM prompt | Obligations, rights, risks extraction, payment terms, screening result criteria |

---

## Virtual Environment

### Location
```
/Users/ekaterinamatyushina/Legally_AI/prototype/venv/
```

### Purpose
- Isolated Python environment for development
- NOT tracked in git
- Recreate with: `python3 -m venv venv`

### Activation
```bash
cd /Users/ekaterinamatyushina/Legally_AI/prototype
source venv/bin/activate
```

### Dependencies Install
```bash
pip install -r requirements.txt
```

---

## Environment Variables

### Local Development (`.env`)

```
Location: /Users/ekaterinamatyushina/Legally_AI/prototype/.env
Status: NOT in git (secret)
```

**Contents:**
```bash
GROQ_API_KEY=gsk_your_api_key_here
DEFAULT_MODEL=llama-3.3-70b-versatile
SUPPORTED_LANGUAGES=russian,serbian,french,english
```

### HF Spaces (Secrets)

Set in HF Space settings:
- **Name**: `GROQ_API_KEY`
- **Value**: Your Groq API key
- **Access**: Injected as environment variable at runtime

---

## Key Paths Reference

### Commands You'll Use

```bash
# Navigate to main project
cd /Users/ekaterinamatyushina/Legally_AI

# Navigate to prototype
cd /Users/ekaterinamatyushina/Legally_AI/prototype

# Activate virtual environment
cd /Users/ekaterinamatyushina/Legally_AI/prototype
source venv/bin/activate

# Edit source code (example)
code /Users/ekaterinamatyushina/Legally_AI/prototype/src/parsers.py

# View logs (local run)
cd /Users/ekaterinamatyushina/Legally_AI/prototype
python app.py
# Then open http://localhost:7860
```

---

## File Size & Performance Notes

### Large Files (be cautious)
- `src/parsers.py` - Can be slow with large PDFs
- `src/prompts/*.txt` - Prompts sent to LLM (stay concise)
- Contract uploads - Limited to reasonable size by Gradio

### Small Files (quick changes)
- `constants.py` - Just configuration
- `formatter.py` - Just formatting logic
- `requirements.txt` - Just dependency list

---

## Backup Strategy

### What to Backup

1. **Source Code**: Backed up to GitHub automatically
2. **Documentation**: Backed up to GitHub automatically
3. **Environment Variables**: Keep `.env` copy somewhere safe (NOT in git)
4. **API Keys**: Store securely (password manager)

### What NOT to Backup

- `venv/` - Can be recreated
- `__pycache__/` - Generated automatically
- Uploaded test contracts - Can be deleted

---

## Development Workflow

### Typical Edit Flow

```bash
# 1. Navigate to prototype
cd /Users/ekaterinamatyushina/Legally_AI/prototype

# 2. Activate environment
source venv/bin/activate

# 3. Edit file
code src/parsers.py  # or your editor of choice

# 4. Test locally
python app.py
# Test at http://localhost:7860

# 5. Commit changes (prototype repo)
git add src/parsers.py
git commit -m "Fix table extraction"

# 6. Push to HF
git push hf main

# 7. Also commit to GitHub (main repo)
cd ..  # Back to main project
git add prototype/src/parsers.py
git commit -m "Fix table extraction in prototype"
git push origin main
```

### Why Two Git Repos?

1. **Main GitHub Repo**: Full project with docs, planning, multiple components
2. **Prototype HF Repo**: Only deployment-ready app files

This keeps the HF deployment clean and fast (no unnecessary docs/planning files).

---

## Common File Operations

### Edit a Source File
```bash
cd /Users/ekaterinamatyushina/Legally_AI/prototype
code src/step2_analysis.py
# Make changes
git add src/step2_analysis.py
git commit -m "Update analysis logic"
git push hf main
```

### Update Dependencies
```bash
cd /Users/ekaterinamatyushina/Legally_AI/prototype
# Edit requirements.txt
code requirements.txt
# Add new library, e.g.: pandas==2.0.0
git add requirements.txt
git commit -m "Add pandas dependency"
git push hf main
# HF will automatically install new dependency
```

### Update UI Text
```bash
cd /Users/ekaterinamatyushina/Legally_AI/prototype
code src/constants.py
# Edit UI_STRINGS section
git add src/constants.py
git commit -m "Update UI strings"
git push hf main
```

### Update Prompts
```bash
cd /Users/ekaterinamatyushina/Legally_AI/prototype
code src/prompts/analysis_en.txt
# Edit prompt instructions
git add src/prompts/analysis_en.txt
git commit -m "Improve analysis prompt"
git push hf main
```

---

## Troubleshooting Paths

### "File not found" Error

Check you're in the right directory:
```bash
pwd
# Should show: /Users/ekaterinamatyushina/Legally_AI/prototype
```

### "Command not found" Error

Activate virtual environment:
```bash
source /Users/ekaterinamatyushina/Legally_AI/prototype/venv/bin/activate
```

### "Module not found" Error

Install dependencies:
```bash
cd /Users/ekaterinamatyushina/Legally_AI/prototype
pip install -r requirements.txt
```

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────────┐
│                  LEGALLY AI - QUICK PATHS                   │
├─────────────────────────────────────────────────────────────┤
│ Main Project:     /Users/ekaterinamatyushina/Legally_AI    │
│ Prototype:        .../Legally_AI/prototype                 │
│ Source Code:      .../prototype/src/                       │
│ Virtual Env:      .../prototype/venv/                      │
│ Activate:         source venv/bin/activate                 │
│                                                             │
│ GitHub:   https://github.com/7kash/Legally_AI              │
│ HF Space: https://huggingface.co/spaces/7Kash-...          │
│                                                             │
│ Deploy: cd prototype → git add . → commit → push hf main   │
└─────────────────────────────────────────────────────────────┘
```

---

**Last Updated**: 2025-11-09
**Maintained By**: Ekaterina Matyushina
**Session**: 011CUtiiNvgPVR7ram5DwPLU
**Status**: Phase 3 Frontend Complete
