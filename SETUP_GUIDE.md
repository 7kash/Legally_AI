# Legally AI - Development Setup Guide

Complete guide for setting up the development environment and integrating frontend with backend.

---

## Prerequisites

### Required Software

- **Node.js** 18+ and npm/yarn/pnpm
- **Python** 3.11+
- **Docker** and Docker Compose
- **Git**

### Recommended Tools

- **VS Code** with extensions:
  - Vue Language Features (Volar)
  - Python
  - ESLint
  - Prettier
  - Tailwind CSS IntelliSense

---

## Quick Start (Development)

### 1. Clone Repository

```bash
git clone https://github.com/7kash/Legally_AI.git
cd Legally_AI
```

### 2. Backend Setup

```bash
cd backend

# Create .env file (already created in this session)
# The .env file is already in backend/.env with development settings

# Start services with Docker Compose
docker-compose up -d

# Wait for services to be healthy (check with)
docker-compose ps

# Install Python dependencies (if running without Docker)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Verify backend is running
curl http://localhost:8000/api/health
# Expected: {"status": "healthy"}
```

### 3. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Create .env.development file
cat > .env.development << EOF
NUXT_PUBLIC_API_BASE=http://localhost:8000/api
NUXT_PUBLIC_ENABLE_ANALYTICS=false
EOF

# Generate PWA icons (requires ImageMagick or online tool)
cd public/icons
# Follow instructions in README.md to generate PNG icons

# Start development server
cd ../..
npm run dev

# Frontend should be running at http://localhost:3000
```

---

## Backend Setup (Detailed)

### Option 1: Docker Compose (Recommended)

**Advantages**:
- All services configured automatically
- Consistent environment
- Easy to start/stop

**Steps**:

```bash
cd backend

# Start all services (PostgreSQL, Redis, Backend API, Celery Worker)
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down

# Stop and remove volumes (clean slate)
docker-compose down -v
```

**Service URLs**:
- Backend API: http://localhost:8000
- PostgreSQL: localhost:5432
- Redis: localhost:6379

### Option 2: Local Installation

**Advantages**:
- Faster iteration
- Direct debugging
- No Docker required

**Steps**:

#### 2.1. Install PostgreSQL

**macOS**:
```bash
brew install postgresql@16
brew services start postgresql@16
createdb legally_ai
```

**Ubuntu/Debian**:
```bash
sudo apt-get install postgresql-16
sudo systemctl start postgresql
sudo -u postgres createdb legally_ai
sudo -u postgres psql
# In psql:
CREATE USER legally_ai WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE legally_ai TO legally_ai;
\q
```

**Windows**:
- Download from https://www.postgresql.org/download/windows/
- Install and create database `legally_ai`

#### 2.2. Install Redis

**macOS**:
```bash
brew install redis
brew services start redis
```

**Ubuntu/Debian**:
```bash
sudo apt-get install redis-server
sudo systemctl start redis
```

**Windows**:
- Use WSL2 or Redis for Windows port

#### 2.3. Run Backend

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# In a separate terminal, start Celery worker
cd backend
source venv/bin/activate
celery -A app.tasks.celery_app worker --loglevel=info
```

---

## Frontend Setup (Detailed)

### Install Dependencies

```bash
cd frontend
npm install
```

**Common Issues**:

- **Vitest version conflict**: Already fixed in package.json (v3.2.0)
- **ESLint plugin**: Using `eslint-plugin-vuejs-accessibility` instead of `vue-a11y`
- **Husky errors**: prepare script removed from package.json

### Environment Variables

Create `.env.development`:

```bash
# API Configuration
NUXT_PUBLIC_API_BASE=http://localhost:8000/api

# Features
NUXT_PUBLIC_ENABLE_ANALYTICS=false
```

For production, create `.env.production`:

```bash
NUXT_PUBLIC_API_BASE=https://api.legally-ai.com/api
NUXT_PUBLIC_ENABLE_ANALYTICS=true
```

### Generate PWA Icons

The frontend requires PNG icons for the PWA. Follow these steps:

#### Option 1: Using ImageMagick (Command Line)

```bash
cd frontend/public/icons

# Install ImageMagick if needed
# macOS: brew install imagemagick
# Ubuntu: sudo apt-get install imagemagick

# Generate icons
convert icon.svg -resize 192x192 icon-192x192.png
convert icon.svg -resize 512x512 icon-512x512.png
```

#### Option 2: Using Sharp (Node.js)

```bash
cd frontend

# Install sharp-cli
npm install --save-dev sharp-cli

# Generate icons
npx sharp -i public/icons/icon.svg -o public/icons/icon-192x192.png resize 192 192
npx sharp -i public/icons/icon.svg -o public/icons/icon-512x512.png resize 512 512
```

#### Option 3: Online Tool

1. Open https://squoosh.app/
2. Upload `frontend/public/icons/icon.svg`
3. Resize to 192x192, download as `icon-192x192.png`
4. Resize to 512x512, download as `icon-512x512.png`
5. Place both in `frontend/public/icons/`

### Run Development Server

```bash
cd frontend
npm run dev

# Server running at http://localhost:3000
```

---

## Testing the Integration

### 1. Backend Health Check

```bash
# Check API is running
curl http://localhost:8000/api/health

# Check API documentation
open http://localhost:8000/docs
```

### 2. Test Authentication

```bash
# Register a user
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123"
  }'

# Expected: {"access_token": "...", "token_type": "bearer", "user": {...}}
```

### 3. Frontend Integration Test

```bash
# Open browser
open http://localhost:3000

# Test flow:
# 1. Click "Register" → Create account
# 2. Login with credentials
# 3. Upload a PDF contract
# 4. Watch real-time analysis progress
# 5. View analysis results
```

---

## Database Migrations

### Create a Migration

```bash
cd backend
source venv/bin/activate

# Auto-generate migration from model changes
alembic revision --autogenerate -m "Description of changes"

# Review the generated migration in alembic/versions/

# Apply migration
alembic upgrade head
```

### Common Migration Commands

```bash
# View current version
alembic current

# View migration history
alembic history

# Upgrade to specific version
alembic upgrade <revision>

# Downgrade one version
alembic downgrade -1

# Reset database (DANGER: deletes all data)
alembic downgrade base
alembic upgrade head
```

---

## API Keys Setup

### Required for Full Functionality

#### 1. Groq API (LLM Provider)

```bash
# Get free API key from https://console.groq.com/
# Add to backend/.env:
GROQ_API_KEY=gsk_your_actual_key_here
```

#### 2. Optional Services

**DeepSeek** (Fallback LLM):
```bash
# Get key from https://platform.deepseek.com/
DEEPSEEK_API_KEY=sk_your_key_here
```

**Stripe** (Payments - Phase 5):
```bash
# Get keys from https://dashboard.stripe.com/test/apikeys
STRIPE_API_KEY=sk_test_your_key
STRIPE_WEBHOOK_SECRET=whsec_your_secret
```

**SendGrid** (Email - Phase 5):
```bash
# Get key from https://app.sendgrid.com/settings/api_keys
SENDGRID_API_KEY=SG.your_key
FROM_EMAIL=noreply@your-domain.com
```

---

## Troubleshooting

### Backend Issues

#### Port 8000 Already in Use

```bash
# Find process using port 8000
lsof -ti:8000

# Kill process
kill -9 $(lsof -ti:8000)

# Or use different port
uvicorn app.main:app --port 8001
```

#### Database Connection Error

```bash
# Check PostgreSQL is running
pg_isready -h localhost -p 5432

# Check credentials in .env match database
# DATABASE_URL=postgresql://legally_ai:password@localhost:5432/legally_ai

# Test connection
psql postgresql://legally_ai:password@localhost:5432/legally_ai
```

#### Redis Connection Error

```bash
# Check Redis is running
redis-cli ping
# Expected: PONG

# Start Redis if not running
# macOS: brew services start redis
# Linux: sudo systemctl start redis
```

#### Celery Worker Not Starting

```bash
# Check Redis connection
redis-cli ping

# Check Celery broker URL in .env
CELERY_BROKER_URL=redis://localhost:6379/0

# Start with verbose logging
celery -A app.tasks.celery_app worker --loglevel=debug
```

### Frontend Issues

#### Module Not Found Errors

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

#### Nuxt Build Errors

```bash
# Clear Nuxt cache
rm -rf .nuxt .output
npm run dev
```

#### API Connection Refused

```bash
# Check backend is running
curl http://localhost:8000/api/health

# Check CORS settings in backend/.env
CORS_ORIGINS=["http://localhost:3000"]

# Check frontend .env
NUXT_PUBLIC_API_BASE=http://localhost:8000/api
```

#### PWA Not Working

```bash
# Ensure icons are generated
ls -la frontend/public/icons/
# Should see: icon-192x192.png, icon-512x512.png

# Build and preview
npm run build
npm run preview

# Test PWA in Chrome DevTools > Application > Manifest
```

---

## Development Workflow

### Daily Development

```bash
# Terminal 1: Backend
cd backend
docker-compose up

# Terminal 2: Frontend
cd frontend
npm run dev

# Terminal 3: Git operations, testing, etc.
```

### Making Changes

#### Backend Changes

```bash
# 1. Edit code in backend/app/
# 2. Backend auto-reloads with --reload flag
# 3. Test with curl or frontend
# 4. Commit changes

# If database models changed:
alembic revision --autogenerate -m "Your change"
alembic upgrade head
```

#### Frontend Changes

```bash
# 1. Edit code in frontend/
# 2. Frontend auto-reloads (Hot Module Replacement)
# 3. Test in browser
# 4. Run tests:
npm run lint
npm run test
# 5. Commit changes
```

### Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm run test              # Unit tests
npm run test:e2e          # E2E tests
npm run test:a11y         # Accessibility
npm run lint              # Linting
```

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes, commit often
git add .
git commit -m "feat: your feature description"

# Push to remote
git push -u origin feature/your-feature-name

# Create pull request on GitHub
```

---

## Deployment

### Frontend (Vercel)

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

**Environment Variables** (Set in Vercel dashboard):
- `NUXT_PUBLIC_API_BASE` = Production API URL
- `NUXT_PUBLIC_ENABLE_ANALYTICS` = `true`

### Backend (Fly.io)

```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Initialize app
cd backend
fly launch

# Set secrets
fly secrets set SECRET_KEY=your-secret-key
fly secrets set GROQ_API_KEY=your-groq-key
fly secrets set DATABASE_URL=your-postgres-url

# Deploy
fly deploy
```

---

## Useful Commands Reference

### Backend

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Run migrations
alembic upgrade head

# Create admin user (if needed)
python scripts/create_admin.py

# Run tests
pytest

# Check API docs
open http://localhost:8000/docs
```

### Frontend

```bash
# Development
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run tests
npm run test
npm run test:e2e
npm run test:a11y

# Linting
npm run lint
npm run format

# Type checking
npm run typecheck
```

### Database

```bash
# Connect to PostgreSQL
psql postgresql://legally_ai:password@localhost:5432/legally_ai

# Backup database
pg_dump -U legally_ai legally_ai > backup.sql

# Restore database
psql -U legally_ai legally_ai < backup.sql

# View tables
psql postgresql://legally_ai:password@localhost:5432/legally_ai
\dt

# Reset database
alembic downgrade base && alembic upgrade head
```

---

## Common Integration Scenarios

### Scenario 1: Testing File Upload

```bash
# 1. Start backend and frontend
# 2. Login to frontend (http://localhost:3000/login)
# 3. Navigate to upload page
# 4. Drop a PDF file
# 5. Watch backend logs:
docker-compose logs -f backend celery_worker

# You should see:
# - File upload received
# - Celery task dispatched
# - Analysis started
# - SSE events sent
# - Analysis completed
```

### Scenario 2: Debugging SSE Connection

```bash
# Terminal 1: Start backend with debug logging
cd backend
uvicorn app.main:app --reload --log-level=debug

# Terminal 2: Test SSE endpoint
curl -N http://localhost:8000/api/analyses/123/stream?token=your-jwt-token

# Terminal 3: Frontend dev server
cd frontend
npm run dev

# Check browser console for SSE connection logs
```

### Scenario 3: Testing Authentication Flow

```bash
# 1. Register new user via frontend
# 2. Check backend logs for registration
# 3. Login via frontend
# 4. Verify JWT token stored in browser (DevTools > Application > Storage)
# 5. Make authenticated request
# 6. Check token validation in backend logs
```

---

## Performance Optimization

### Backend

```bash
# Profile slow endpoints
python -m cProfile -o profile.stats app/main.py

# Analyze profile
python -c "import pstats; p = pstats.Stats('profile.stats'); p.sort_stats('cumulative'); p.print_stats(20)"

# Monitor database queries
# Add to backend/.env:
DEBUG=True
DATABASE_ECHO=True
```

### Frontend

```bash
# Analyze bundle size
npm run build
npx nuxt analyze

# Check Lighthouse score
npm run build
npm run preview
# Open Chrome DevTools > Lighthouse > Run audit

# Measure build time
time npm run build
```

---

## Security Checklist

Before deploying to production:

- [ ] Change `SECRET_KEY` in backend/.env to production value
- [ ] Set `DEBUG=False` in backend/.env
- [ ] Use real API keys (Groq, Stripe, SendGrid)
- [ ] Enable HTTPS only (no HTTP)
- [ ] Set secure CORS origins (no `*`)
- [ ] Enable rate limiting
- [ ] Set up monitoring (Sentry)
- [ ] Configure database backups
- [ ] Use environment variables for all secrets (never commit .env)
- [ ] Review and test authentication flow
- [ ] Test file upload size limits
- [ ] Review error messages (don't leak sensitive info)

---

## Additional Resources

- **Backend API Docs**: http://localhost:8000/docs (when running)
- **Frontend README**: `frontend/README.md`
- **Integration Checklist**: `INTEGRATION_CHECKLIST.md`
- **Architecture**: `architecture.md`
- **Project Progress**: `progress.md`

---

**Last Updated**: 2025-11-09
**Version**: 1.0.0 (Phase 4 - Integration Ready)
