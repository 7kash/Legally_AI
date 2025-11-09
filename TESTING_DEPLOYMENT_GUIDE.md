# Testing & Deployment Guide

**Phase 4 Complete** ✅ | **Ready for Integration Testing**

This guide provides step-by-step instructions for testing and deploying Legally AI to production.

---

## Table of Contents

1. [Quick Start (Local Development)](#quick-start-local-development)
2. [Integration Testing](#integration-testing)
3. [Performance Testing](#performance-testing)
4. [Deployment](#deployment)
5. [Post-Deployment Verification](#post-deployment-verification)

---

## Quick Start (Local Development)

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (recommended)

### Option 1: Docker Compose (Recommended)

The fastest way to get the full stack running locally:

```bash
# Start all services (PostgreSQL, Redis, Backend, Frontend)
docker-compose up

# Backend will be available at: http://localhost:8000
# Frontend will be available at: http://localhost:3000
# API docs at: http://localhost:8000/docs
```

### Option 2: Manual Setup

#### Step 1: Start PostgreSQL and Redis

```bash
# Using Docker
docker run -d --name legally-postgres \
  -e POSTGRES_USER=legally_ai \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=legally_ai \
  -p 5432:5432 \
  postgres:15

docker run -d --name legally-redis \
  -p 6379:6379 \
  redis:7-alpine
```

#### Step 2: Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your configuration

# Run database migrations
alembic upgrade head

# Start Celery worker (in separate terminal)
celery -A app.tasks.celery_app worker --loglevel=info

# Start backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend now running at: http://localhost:8000

API documentation: http://localhost:8000/docs

#### Step 3: Setup Frontend

```bash
cd frontend

# Install dependencies
npm install

# Create .env.development file
echo "NUXT_PUBLIC_API_BASE=http://localhost:8000/api" > .env.development
echo "NUXT_PUBLIC_ENABLE_ANALYTICS=false" >> .env.development

# Generate PWA icons (if needed)
npm run icons

# Start development server
npm run dev
```

Frontend now running at: http://localhost:3000

---

## Integration Testing

### Test Plan Overview

All user flows should be tested end-to-end with real API integration:

1. ✅ Authentication flows
2. ✅ Contract upload and analysis
3. ✅ Real-time SSE updates
4. ✅ Export functionality
5. ✅ Account management
6. ✅ Password reset
7. ✅ Email verification

### Manual Testing Checklist

#### 1. User Registration & Authentication

```bash
# Test Endpoint: POST /api/auth/register
```

- [ ] Register new user with valid email/password
- [ ] Verify email validation (invalid format rejected)
- [ ] Verify password validation (min length, complexity)
- [ ] Check duplicate email rejection
- [ ] Verify JWT token returned
- [ ] Verify user record created in database

#### 2. User Login

```bash
# Test Endpoint: POST /api/auth/login
```

- [ ] Login with valid credentials
- [ ] Login with invalid email (404 error)
- [ ] Login with wrong password (401 error)
- [ ] Verify JWT token returned
- [ ] Verify user data in response

#### 3. Password Reset Flow

```bash
# Test Endpoints:
# POST /api/auth/forgot-password
# POST /api/auth/reset-password
```

- [ ] Request password reset for valid email
- [ ] Request password reset for non-existent email (still returns success)
- [ ] Check SendGrid email sent (or logged in dev mode)
- [ ] Click reset link in email
- [ ] Reset password with valid token
- [ ] Try to reset with expired token (should fail)
- [ ] Login with new password

#### 4. Email Verification Flow

```bash
# Test Endpoints:
# POST /api/auth/verify-email
# POST /api/auth/resend-verification
```

- [ ] New user starts unverified (is_verified = false)
- [ ] Verification email sent on registration
- [ ] Click verification link
- [ ] User now verified (is_verified = true)
- [ ] Resend verification email
- [ ] Try to verify with invalid token (should fail)

#### 5. Contract Upload

```bash
# Test Endpoint: POST /api/contracts/upload
```

- [ ] Upload PDF file (<10MB)
- [ ] Upload DOCX file (<10MB)
- [ ] Upload progress tracking works
- [ ] Reject file >10MB (400 error)
- [ ] Reject invalid file type (400 error)
- [ ] Free user: Can upload 3 contracts
- [ ] Free user: 4th upload rejected (limit exceeded)
- [ ] Verify file saved to disk
- [ ] Verify contract record in database

#### 6. Analysis Creation & Real-Time Updates

```bash
# Test Endpoints:
# POST /api/analyses
# GET /api/analyses/{id}/stream (SSE)
# GET /api/analyses/{id}
```

- [ ] Create analysis for uploaded contract
- [ ] Celery task dispatched
- [ ] SSE connection established
- [ ] Receive progress events:
  - [ ] started
  - [ ] parsing
  - [ ] analyzing
  - [ ] completed
- [ ] Analysis results displayed
- [ ] Results stored in database
- [ ] SSE connection closes on completion

#### 7. Export Functionality

```bash
# Test Endpoints:
# GET /api/analyses/{id}/export/pdf
# GET /api/analyses/{id}/export/docx
```

- [ ] Export completed analysis as PDF
- [ ] PDF downloads correctly
- [ ] PDF contains contract metadata
- [ ] PDF contains analysis results
- [ ] PDF has professional formatting
- [ ] Export as DOCX
- [ ] DOCX downloads correctly
- [ ] DOCX has proper structure and styling
- [ ] Cannot export incomplete analysis (400 error)

#### 8. Analysis Feedback

```bash
# Test Endpoint: POST /api/analyses/{id}/feedback
```

- [ ] Submit positive feedback (is_correct = true)
- [ ] Submit negative feedback with comment
- [ ] Feedback saved to database
- [ ] Feedback linked to correct analysis

#### 9. Account Management

```bash
# Test Endpoints:
# GET /api/account
# PATCH /api/account
# GET /api/account/export
# DELETE /api/account
```

**Account Details:**
- [ ] GET /account returns user info
- [ ] Returns total contracts count
- [ ] Returns total analyses count
- [ ] Returns tier limit

**Profile Update:**
- [ ] Update email (with verification reset)
- [ ] Update email to existing email (400 error)
- [ ] Change password with current password
- [ ] Change password without current password (400 error)
- [ ] Change password with wrong current password (400 error)

**GDPR Data Export:**
- [ ] GET /account/export returns JSON
- [ ] JSON contains user data
- [ ] JSON contains all contracts
- [ ] JSON contains all analyses
- [ ] JSON contains all feedback
- [ ] JSON has export timestamp

**Account Deletion:**
- [ ] DELETE /account with confirmation
- [ ] All user data deleted (cascade)
- [ ] User cannot login after deletion
- [ ] Deleted user's contracts removed
- [ ] Deleted user's analyses removed

#### 10. History & Contract Management

```bash
# Test Endpoints:
# GET /api/contracts
# GET /api/contracts/{id}
# DELETE /api/contracts/{id}
```

- [ ] List all user contracts
- [ ] Pagination works (if >10 results)
- [ ] Get single contract details
- [ ] Delete contract
- [ ] Associated analyses also deleted (cascade)

### Automated Testing

#### Backend Unit Tests

```bash
cd backend
pytest tests/ -v --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py -v

# Run with coverage report
pytest --cov=app --cov-report=term-missing
```

**Expected Coverage**: >80%

#### Frontend Unit Tests

```bash
cd frontend
npm run test

# Run with coverage
npm run test:coverage

# Watch mode for development
npm run test:watch
```

**Test suites:**
- [ ] Store tests (auth, contracts, analyses)
- [ ] Composable tests (useDarkMode, useNotifications)
- [ ] Component tests (notification, header, footer)

#### E2E Tests (Playwright)

```bash
cd frontend

# Install Playwright browsers (first time only)
npx playwright install

# Run E2E tests
npm run test:e2e

# Run in headed mode (see browser)
npm run test:e2e -- --headed

# Run specific test file
npm run test:e2e tests/e2e/auth.spec.ts
```

**Test scenarios:**
- [ ] Complete registration flow
- [ ] Complete login flow
- [ ] Complete upload and analysis flow
- [ ] Password reset flow
- [ ] Mobile responsive tests

---

## Performance Testing

### 1. Bundle Size Analysis

```bash
cd frontend

# Build for production
npm run build

# Analyze bundle
npm run analyze

# Check output
ls -lh .output/public/_nuxt/
```

**Targets:**
- Total bundle size: <500KB gzipped
- Main chunk: <250KB gzipped
- Route chunks: <100KB each

### 2. Lighthouse Audit

```bash
# Build and preview
npm run build
npm run preview

# Then run Lighthouse in Chrome DevTools
# Or use CLI:
npx lighthouse http://localhost:3000 --view
```

**Targets:**
- Performance: >90
- Accessibility: >90
- Best Practices: >90
- SEO: >90

### 3. API Performance

```bash
# Install apache bench
sudo apt-get install apache2-utils  # Linux
brew install httpie  # macOS

# Test endpoint performance
ab -n 1000 -c 10 http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Targets:**
- Auth endpoints: <100ms
- Contract list: <200ms
- Analysis get: <150ms

### 4. Database Performance

```sql
-- Check query performance
EXPLAIN ANALYZE SELECT * FROM contracts WHERE user_id = 'user-uuid';

-- Check indexes
SELECT * FROM pg_indexes WHERE tablename IN ('users', 'contracts', 'analyses');

-- Check slow queries (if pg_stat_statements enabled)
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;
```

---

## Deployment

### Backend Deployment (Railway / Fly.io)

#### Option 1: Railway

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize project
cd backend
railway init

# Add environment variables
railway variables set DATABASE_URL=postgresql://...
railway variables set REDIS_URL=redis://...
railway variables set SECRET_KEY=your-secret-key
railway variables set GROQ_API_KEY=your-groq-key
railway variables set SENDGRID_API_KEY=your-sendgrid-key
railway variables set FROM_EMAIL=noreply@legally-ai.com
railway variables set FRONTEND_URL=https://legally-ai.vercel.app

# Deploy
railway up
```

#### Option 2: Fly.io

```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Launch app
cd backend
fly launch

# Set environment variables
fly secrets set DATABASE_URL=postgresql://...
fly secrets set REDIS_URL=redis://...
fly secrets set SECRET_KEY=your-secret-key
fly secrets set GROQ_API_KEY=your-groq-key
fly secrets set SENDGRID_API_KEY=your-sendgrid-key

# Deploy
fly deploy
```

### Frontend Deployment (Vercel)

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy to preview
cd frontend
vercel

# Deploy to production
vercel --prod
```

**Vercel Environment Variables:**

Set these in Vercel dashboard (Settings > Environment Variables):

```bash
NUXT_PUBLIC_API_BASE=https://api.legally-ai.com/api
NUXT_PUBLIC_ENABLE_ANALYTICS=true
```

### Database Migration

```bash
# On production, run migrations
cd backend
alembic upgrade head

# Verify
alembic current
```

### Celery Worker Deployment

#### Railway:
```bash
# Create worker service
railway init

# Set start command in railway.json:
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "celery -A app.tasks.celery_app worker --loglevel=info"
  }
}
```

#### Fly.io:
```bash
# Create worker instance
fly scale count worker=1

# In fly.toml, add processes:
[processes]
web = "uvicorn app.main:app --host 0.0.0.0 --port 8080"
worker = "celery -A app.tasks.celery_app worker --loglevel=info"
```

---

## Post-Deployment Verification

### Health Checks

```bash
# Backend health
curl https://api.legally-ai.com/health

# Expected:
{
  "status": "healthy",
  "version": "1.0.0",
  "app": "Legally AI"
}

# Frontend
curl https://legally-ai.vercel.app

# API docs (if DEBUG=true)
curl https://api.legally-ai.com/docs
```

### Smoke Tests

Run these tests immediately after deployment:

```bash
# 1. Register new user
curl -X POST https://api.legally-ai.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"TestPass123!"}'

# 2. Login
curl -X POST https://api.legally-ai.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"TestPass123!"}'

# 3. Get user profile
curl https://api.legally-ai.com/api/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Monitor Logs

```bash
# Railway
railway logs

# Fly.io
fly logs

# Vercel
vercel logs
```

### Setup Monitoring

#### Sentry (Error Tracking)

Backend is already configured for Sentry. Just set the environment variable:

```bash
railway variables set SENTRY_DSN=https://your-sentry-dsn@sentry.io/project
```

Frontend setup:
```bash
cd frontend
npm install --save @sentry/nuxt

# Add to nuxt.config.ts
export default defineNuxtConfig({
  modules: ['@sentry/nuxt/module'],
  sentry: {
    dsn: 'https://your-sentry-dsn@sentry.io/project'
  }
})
```

---

## Troubleshooting

### Common Issues

#### Backend won't start

```bash
# Check database connection
psql postgresql://legally_ai:password@localhost:5432/legally_ai

# Check Redis connection
redis-cli ping

# Check environment variables
env | grep -E "(DATABASE_URL|REDIS_URL|SECRET_KEY)"

# Check logs
tail -f backend/logs/app.log
```

#### Frontend API calls failing

```bash
# Check CORS configuration in backend
# backend/app/config.py should have:
CORS_ORIGINS = ["http://localhost:3000", "https://legally-ai.vercel.app"]

# Check API base URL
echo $NUXT_PUBLIC_API_BASE

# Check network tab in browser DevTools
```

#### Celery worker not processing tasks

```bash
# Check if worker is running
ps aux | grep celery

# Check Redis connection
redis-cli
> KEYS celery*

# Check task queue
celery -A app.tasks.celery_app inspect active

# Restart worker
pkill -9 celery
celery -A app.tasks.celery_app worker --loglevel=info
```

#### Database migrations failing

```bash
# Check current version
alembic current

# Check pending migrations
alembic heads

# Rollback one version
alembic downgrade -1

# Re-apply
alembic upgrade head
```

---

## Security Checklist

Before deploying to production:

- [ ] Change default SECRET_KEY to cryptographically secure random value
- [ ] Use strong database password
- [ ] Enable SSL/TLS for all connections
- [ ] Set `DEBUG=false` in production
- [ ] Configure proper CORS_ORIGINS (no wildcards)
- [ ] Enable rate limiting on API endpoints
- [ ] Set up firewall rules (only allow necessary ports)
- [ ] Regular security updates for dependencies
- [ ] Enable database backups
- [ ] Set up log monitoring and alerts
- [ ] Configure CSP headers
- [ ] Enable HTTPS only (no HTTP)

---

## Next Steps

### Immediate (Before Launch)

1. **Complete integration testing** - Test all user flows end-to-end
2. **Performance optimization** - Achieve Lighthouse >90 scores
3. **Security audit** - Review all endpoints and data flows
4. **Deploy to staging** - Test in production-like environment
5. **Load testing** - Ensure system handles expected traffic

### Phase 5: Payments & Polish (2 weeks)

1. **Stripe Integration**
   - Payment endpoint
   - Subscription management
   - Webhook handling

2. **Advanced Features**
   - Deadline Radar
   - Cross-Document Check
   - Batch analysis

3. **Polish**
   - Error messages refinement
   - Loading states
   - Empty states
   - Onboarding flow

### Phase 6: Launch (1 week)

1. **Final QA** - Complete testing checklist
2. **Production deployment** - Deploy to production
3. **Monitoring setup** - Sentry, analytics, uptime
4. **Marketing** - Landing page, docs, announcement
5. **Launch!** 🚀

---

**Last Updated**: 2025-11-09
**Status**: Phase 4 Complete - Ready for Integration Testing
**Next**: Start local testing with Docker Compose
