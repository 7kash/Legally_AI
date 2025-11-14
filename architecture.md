# Legally AI - Technical Architecture

## System Overview

Legally AI is a multilingual contract analysis platform built with a modern, cloud-native architecture optimized for cost-efficiency and scalability.

**Architecture Pattern**: Serverless + JAMstack hybrid
**Development Approach**: Prototype-first, then production-grade MVP

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         USERS                                │
│  Web Browser (Desktop/Mobile) · PWA · API Clients           │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                    VERCEL CDN                                │
│  • Nuxt 3 SSR/SSG Frontend                                   │
│  • Edge Functions                                            │
│  • Static Assets (images, JS, CSS)                           │
└────────────────┬────────────────────────────────────────────┘
                 │
                 │ HTTPS (API Requests)
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                    FLY.IO BACKEND                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  FastAPI Application (3 instances)                   │   │
│  │  • REST API                                           │   │
│  │  • SSE endpoints                                      │   │
│  │  • Authentication (JWT)                               │   │
│  │  • File uploads                                       │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Celery Workers (2 instances)                        │   │
│  │  • Async contract analysis                            │   │
│  │  • Document parsing                                   │   │
│  │  • LLM orchestration                                  │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Redis (1 instance)                                   │   │
│  │  • Celery queue                                       │   │
│  │  • Rate limiting                                      │   │
│  │  • Session cache                                      │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  PostgreSQL (1 instance)                              │   │
│  │  • User data                                          │   │
│  │  • Contracts & analyses                               │   │
│  │  • Subscriptions                                      │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Persistent Volumes                                   │   │
│  │  • Uploaded contract files                            │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                  EXTERNAL SERVICES                           │
│  • Groq API (LLM inference)                                  │
│  • Together.ai (fallback LLM)                                │
│  • Stripe (payments)                                         │
│  • SendGrid (emails)                                         │
│  • Sentry (error tracking)                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## Prototype Architecture (HF Spaces)

**Purpose**: Fast validation with lawyer feedback

```
┌────────────────────────────────────┐
│  Hugging Face Spaces (CPU)         │
│  ┌──────────────────────────────┐  │
│  │  Gradio UI                   │  │
│  │  • File upload               │  │
│  │  • Language selector         │  │
│  │  • Results display           │  │
│  └─────────┬────────────────────┘  │
│            │                        │
│  ┌─────────▼────────────────────┐  │
│  │  Python Backend              │  │
│  │  • parsers.py                │  │
│  │  • step1_preparation.py      │  │
│  │  • step2_analysis.py         │  │
│  │  • formatter.py              │  │
│  └─────────┬────────────────────┘  │
└────────────┼────────────────────────┘
             │
             ▼
     ┌───────────────┐
     │  Groq API     │
     │  (FREE tier)  │
     └───────────────┘
```

**Key Characteristics**:
- Stateless (no database)
- Single process (Gradio + backend)
- No authentication
- Results disappear after session
- Zero cost

---

## Component Details

### Frontend (Nuxt 3)

#### Technology
- **Framework**: Nuxt 3.8+
- **Language**: TypeScript
- **UI Framework**: Tailwind CSS + Headless UI
- **State Management**: Pinia
- **HTTP Client**: $fetch (Nuxt built-in)
- **Forms**: VeeValidate + Zod
- **PWA**: @vite-pwa/nuxt

#### Structure
```
frontend/
├── nuxt.config.ts          # Nuxt configuration
├── app.vue                 # Root component
├── pages/                  # File-based routing
├── components/             # Vue components
├── composables/            # Composition API functions
├── stores/                 # Pinia stores
├── middleware/             # Route middleware
├── plugins/                # Vue plugins
├── layouts/                # Layout components
├── public/                 # Static assets
├── assets/                 # Compiled assets (CSS, images)
└── server/                 # Nuxt server routes (optional)
```

#### Key Features
- **SSR (Server-Side Rendering)**: Fast initial load, SEO-friendly
- **SSG (Static Site Generation)**: Landing page, pricing page
- **PWA**: Install to home screen, offline shell
- **i18n**: 4 languages (Russian, Serbian, French, English)
- **Responsive**: 320px (mobile) to 2560px (desktop)
- **Dark Mode**: System preference detection (optional)

#### Performance Targets
- First Contentful Paint: <1.5s
- Time to Interactive: <3s
- Lighthouse Score: >90
- Bundle Size: <250KB gzipped

---

### Backend (FastAPI)

#### Technology
- **Framework**: FastAPI 0.110+
- **Language**: Python 3.11+
- **ASGI Server**: Uvicorn
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic
- **Validation**: Pydantic v2
- **Auth**: FastAPI-Users + JWT
- **Tasks**: Celery 5.x
- **Queue**: Redis 7.x

#### Structure
```
backend/
├── app/
│   ├── main.py                 # FastAPI app entry
│   ├── config.py               # Settings (from env)
│   ├── api/
│   │   ├── auth.py             # Authentication endpoints
│   │   ├── contracts.py        # Contract endpoints
│   │   ├── analyses.py         # Analysis endpoints
│   │   ├── deadlines.py        # Deadline Radar
│   │   ├── document_sets.py    # Cross-doc consistency
│   │   ├── billing.py          # Stripe integration
│   │   └── account.py          # User account
│   ├── models/
│   │   ├── user.py
│   │   ├── contract.py
│   │   ├── analysis.py
│   │   └── ...
│   ├── schemas/
│   │   ├── contract.py         # Pydantic schemas
│   │   ├── analysis.py
│   │   └── ...
│   ├── services/
│   │   ├── document_parser.py  # PDF/DOCX text extraction
│   │   ├── llm_analysis/       # ✅ LLM analysis modules (INTEGRATED)
│   │   │   ├── llm_router.py       # GROQ API client
│   │   │   ├── step1_preparation.py # Document preparation
│   │   │   ├── step2_analysis.py   # Contract analysis
│   │   │   ├── language.py         # Language detection
│   │   │   ├── parsers.py          # Document structure
│   │   │   ├── quality.py          # Confidence scoring
│   │   │   ├── constants.py        # Model settings, UI strings
│   │   │   ├── formatter.py        # Output formatting
│   │   │   └── prompts/            # LLM prompt templates
│   │   ├── deadline_extractor.py
│   │   ├── conflict_detector.py
│   │   └── ...
│   ├── tasks/
│   │   └── analyze_contract.py # ✅ Celery tasks with LLM integration
│   ├── db/
│   │   ├── base.py
│   │   └── session.py
│   ├── core/
│   │   ├── security.py         # JWT, password hashing
│   │   ├── deps.py             # Dependencies
│   │   └── exceptions.py
│   └── utils/
├── tests/
├── alembic/                    # Database migrations
├── prompts/                    # LLM prompts
├── Dockerfile
├── requirements.txt
└── celery_worker.py
```

#### Key Endpoints

**Authentication**
```
POST   /api/auth/register
POST   /api/auth/login
POST   /api/auth/logout
GET    /api/auth/me
```

**Contracts**
```
POST   /api/contracts/upload
GET    /api/contracts
GET    /api/contracts/{id}
DELETE /api/contracts/{id}
```

**Analysis**
```
POST   /api/contracts/{id}/analyze
GET    /api/analyses/{id}
GET    /api/analyses/{id}/stream      # SSE
POST   /api/analyses/{id}/feedback
GET    /api/analyses/{id}/export/{format}
```

**Advanced Features**
```
POST   /api/document-sets
GET    /api/document-sets/{id}/conflicts
POST   /api/compare
GET    /api/deadlines/upcoming
```

---

### Database (PostgreSQL)

#### Schema Overview

**Core Tables**:
- `users`: User accounts
- `contracts`: Uploaded contracts
- `analyses`: Analysis results
- `events`: Audit log

**Feature Tables**:
- `subscriptions`: Stripe subscriptions
- `feedback`: Confidence calibration
- `deadlines`: Deadline Radar
- `document_sets`: Multi-doc sets
- `document_set_members`: Set membership
- `conflicts`: Cross-doc conflicts

#### Key Indexes
```sql
-- Performance indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_contracts_user_created ON contracts(user_id, created_at DESC);
CREATE INDEX idx_analyses_contract ON analyses(contract_id);
CREATE INDEX idx_events_analysis_created ON events(analysis_id, created_at);
CREATE INDEX idx_deadlines_user_date ON deadlines(user_id, deadline_date);

-- Full-text search (future)
CREATE INDEX idx_contracts_text_search ON contracts USING gin(to_tsvector('english', text));
```

#### Backup Strategy
- **Frequency**: Daily automated backups
- **Retention**: 30 days
- **Location**: Fly.io managed backups
- **Testing**: Monthly restore drill

---

### LLM Router

**Purpose**: Provider-agnostic abstraction for LLM calls

#### Architecture
```python
class LLMRouter:
    providers = [
        GroqProvider("llama-3.3-70b"),      # Primary: fast, free
        TogetherProvider("mixtral-8x7b"),   # Fallback: cheap
        OpenAIProvider("gpt-4o-mini"),      # Quality fallback
    ]

    def route(task: str, budget: int, quality: float):
        # Choose provider based on task, budget, quality needs

    def call_with_retry(prompt, schema, max_retries=3):
        # Exponential backoff, fallback providers
```

#### Routing Logic

| Task | Model | Rationale |
|------|-------|-----------|
| Preparation | Llama-3.3-70B | Fast, cheap, accurate for extraction |
| Risk Analysis | Llama-3.3-70B or GPT-4o-mini | Complex reasoning |
| Translation | Llama-3.3-70B | Good multilingual support |
| ELI5 Simplification | Llama-3.3-70B | Simple generation task |

#### Cost Tracking
Every LLM call logs:
- Tokens used (prompt + completion)
- Cost in cents
- Latency
- Provider
- Model
- Success/failure

Stored in `analyses` table for analytics.

---

### Task Queue (Celery + Redis)

#### Why Async?
- Contract analysis takes 10-30 seconds
- HTTP request timeouts at 30s
- Better UX with progress updates

#### Architecture
```
[FastAPI] → [Redis Queue] → [Celery Worker] → [LLM] → [PostgreSQL]
                ↓
          [SSE Stream] ← [Frontend]
```

#### Task Flow
1. User uploads contract
2. FastAPI creates analysis record (status=QUEUED)
3. FastAPI dispatches Celery task
4. Returns task_id to frontend
5. Frontend opens SSE connection
6. Celery worker:
   - Parse document (emit: parsing, 10%)
   - Run Step 1 (emit: preparation, 40%)
   - Run Step 2 (emit: analysis, 80%)
   - Format output (emit: formatting, 95%)
   - Save to DB (emit: done, 100%)
7. SSE pushes updates to frontend in real-time
8. Frontend redirects to results page

#### Retry Logic
- Automatic retry on transient failures (3 attempts)
- Exponential backoff: 2s, 4s, 8s
- Mark as FAILED after 3 attempts
- Log error details for debugging

---

### File Storage

#### Development
- **Local filesystem**: `uploads/` directory
- **Cleanup**: Manual (dev only)

#### Production (Fly.io)
- **Persistent volumes**: SSD-backed, replicated
- **Path**: `/data/contracts/{user_id}/{contract_id}/`
- **Cleanup**: Soft delete (mark as deleted, purge after 30 days)

#### Future (Scale)
- **S3-compatible**: Cloudflare R2 or Backblaze B2
- **CDN**: CloudFront or Cloudflare
- **Cost**: ~$0.005/GB/month

#### Security
- **Encryption at rest**: Fly.io volumes encrypted
- **Access control**: Pre-signed URLs (if using S3)
- **Virus scanning**: ClamAV (optional, adds cost)

---

## Security Architecture

### Authentication Flow

```
[User] → [Login Form] → [FastAPI /auth/login]
                              ↓
                        Verify password
                              ↓
                        Generate JWT token
                              ↓
                        [Return token to client]
                              ↓
[Store in cookie]    [Include in Authorization header]
      ↓                       ↓
  httpOnly=true          Bearer {token}
  secure=true                ↓
  sameSite=strict      [FastAPI middleware]
                              ↓
                        Verify JWT signature
                              ↓
                        Check expiration
                              ↓
                        Inject user into request
```

### JWT Token
- **Algorithm**: HS256 (HMAC with SHA-256)
- **Expiration**: 7 days
- **Refresh**: 30 days (refresh token)
- **Payload**: `{user_id, email, tier, exp, iat}`

### Password Security
- **Hashing**: bcrypt (cost factor: 12)
- **Requirements**: ≥8 chars, 1 uppercase, 1 number
- **Reset**: Time-limited token (1 hour)

### API Security
- **Rate Limiting**: 100 requests/minute per IP
- **CORS**: Whitelist frontend domain only
- **CSRF**: SameSite cookies + token validation
- **Input Validation**: Pydantic schemas, SQL injection prevention
- **File Upload**:
  - Max size: 10MB
  - Allowed types: PDF, DOCX
  - Virus scan (optional)

---

## Observability

### Error Tracking (Sentry)
- All uncaught exceptions
- Custom error events
- User feedback
- Performance metrics (transaction traces)

### Logging
- **Format**: JSON structured logs
- **Levels**: DEBUG (dev), INFO (prod), ERROR, CRITICAL
- **Storage**: Fly.io logs (7 days retention)
- **Aggregation**: Sentry or Logtail (optional)

### Metrics (Future)
- OpenTelemetry → Prometheus → Grafana
- Key metrics:
  - Request rate (req/s)
  - Error rate (%)
  - Latency (P50, P95, P99)
  - LLM cost per analysis
  - Token usage
  - Analysis success rate

### Uptime Monitoring
- **Service**: UptimeRobot (free)
- **Checks**: Every 5 minutes
- **Alerts**: Email + Slack
- **Status Page**: Optional (Statuspage.io)

---

## Deployment Architecture

### CI/CD Pipeline

```
[GitHub Push] → [GitHub Actions]
                      ↓
                  Run Tests
                      ↓
                  Build Docker Image
                      ↓
               ┌──────┴──────┐
               ↓             ↓
         [Deploy Frontend] [Deploy Backend]
         to Vercel         to Fly.io
               ↓             ↓
         [Smoke Tests]   [Health Check]
               ↓             ↓
            [Success]     [Success]
```

### Environments

**Development** (Local)
- Docker Compose
- PostgreSQL, Redis, FastAPI, Nuxt (all local)
- Hot reload
- Mock Stripe

**Staging** (Optional)
- Same as production but separate database
- Test Stripe mode
- For final testing before production deploy

**Production**
- Fly.io: Backend + DB + Redis
- Vercel: Frontend
- Real Stripe
- Monitoring enabled

---

## Scaling Strategy

### Phase 1: MVP (0-100 users)
- 1 FastAPI instance (Fly.io free tier)
- 1 Celery worker
- 1 PostgreSQL (1GB)
- 1 Redis (256MB)
- **Cost**: $0-5/month

### Phase 2: Growth (100-1000 users)
- 2 FastAPI instances
- 2 Celery workers
- PostgreSQL (10GB)
- Redis (1GB)
- **Cost**: $30-50/month

### Phase 3: Scale (1000-10000 users)
- 5+ FastAPI instances (auto-scale)
- 5+ Celery workers (auto-scale)
- PostgreSQL (50GB, read replicas)
- Redis (5GB, cluster)
- CDN for static assets
- S3 for file storage
- **Cost**: $200-500/month

### Bottlenecks & Solutions

| Bottleneck | Solution |
|------------|----------|
| Database connections | Connection pooling (pgbouncer) |
| Slow queries | Indexes, query optimization |
| LLM rate limits | Queue, retry, multiple providers |
| File storage | Move to S3, add CDN |
| Memory (Celery) | More workers, smaller task batches |

---

## Data Flow

### Contract Analysis Flow

```
1. [User] → Upload PDF
2. [Frontend] → POST /api/contracts/upload
3. [FastAPI] → Save file to disk
4. [FastAPI] → Create contract record (DB)
5. [FastAPI] → Dispatch Celery task
6. [FastAPI] → Return {contract_id, task_id}
7. [Frontend] → Open SSE /api/analyses/{id}/stream

8. [Celery Worker] → Parse PDF (pdfplumber)
9. [Celery Worker] → Detect language (langdetect)
10. [Celery Worker] → Emit event: "parsing" (10%)

11. [Celery Worker] → Call LLM (Step 1: Preparation)
12. [LLM Router] → Route to Groq (llama-3.3-70b)
13. [Groq API] → Return preparation JSON
14. [Celery Worker] → Store step1_data (DB)
15. [Celery Worker] → Emit event: "preparation" (40%)

16. [Celery Worker] → Check confidence score
17. [Celery Worker] → If low, downgrade to "Preliminary"
18. [Celery Worker] → Call LLM (Step 2: Analysis)
19. [LLM Router] → Route based on quality needed
20. [LLM] → Return analysis JSON
21. [Celery Worker] → Store step2_data (DB)
22. [Celery Worker] → Emit event: "analysis" (80%)

23. [Celery Worker] → Format output (UI schema)
24. [Celery Worker] → Extract deadlines → Save to deadlines table
25. [Celery Worker] → Store formatted_output (DB)
26. [Celery Worker] → Mark analysis SUCCEEDED
27. [Celery Worker] → Emit event: "done" (100%)

28. [SSE] → Push events to frontend
29. [Frontend] → Redirect to /analysis/{id}
30. [Frontend] → Fetch analysis data
31. [Frontend] → Render all sections
```

### Multi-Document Analysis Flow

```
1. [User] → Upload 3 PDFs (1 primary, 2 context)
2. [Frontend] → POST /api/document-sets
3. [FastAPI] → Create document_set record
4. [FastAPI] → Upload all files
5. [FastAPI] → Create contract records for each
6. [FastAPI] → Dispatch 3 Celery tasks (parallel)

7. [Celery Workers] → Analyze all 3 contracts
8. [Celery Workers] → Store analyses

9. [Conflict Detector] → Compare all contracts
10. [Conflict Detector] → Find:
    - Term conflicts (e.g., different termination notice periods)
    - Missing exhibits (referenced but not uploaded)
    - Overrides (SOW overrides MSA)
11. [Conflict Detector] → Store conflicts table
12. [Conflict Detector] → Determine "source of truth" per term

13. [Frontend] → Display:
    - All 3 analyses
    - Conflicts list (sorted by severity)
    - "Source of truth" badges
```

---

## Technology Choices: Rationale

### Why FastAPI?
- Modern, async Python framework
- Fast (comparable to Node.js)
- Automatic OpenAPI docs
- Type hints + Pydantic validation
- Large ecosystem

### Why Nuxt 3?
- Best-in-class Vue meta-framework
- SSR/SSG out of the box
- File-based routing
- Auto-imports
- Great DX

### Why PostgreSQL?
- JSONB for flexible analysis storage
- Full-text search
- Mature, reliable
- Free tier available (Fly.io)

### Why Groq?
- Extremely fast (800+ tokens/sec)
- Free tier is generous
- Llama-3.3-70B is excellent for multilingual
- Low cost if paid ($0.59/1M tokens)

### Why Fly.io?
- Free tier (3 VMs, 1GB PG, 256MB Redis)
- Global edge network
- Docker-based (portable)
- Easy scaling

### Why Vercel?
- Perfect for Nuxt 3 SSR
- Free tier generous
- Fast CDN
- Zero config

---

**Last Updated**: 2025-11-14
