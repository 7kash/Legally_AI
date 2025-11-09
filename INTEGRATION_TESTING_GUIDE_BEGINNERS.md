# Integration Testing Guide for Beginners

**Welcome!** This guide will walk you through integration testing step-by-step. No prior Docker experience needed!

---

## 📚 Table of Contents

1. [What is Integration Testing?](#what-is-integration-testing)
2. [What is Docker Compose?](#what-is-docker-compose)
3. [Installation](#installation)
4. [Quick Start (5 minutes)](#quick-start)
5. [Step-by-Step Testing](#step-by-step-testing)
6. [Troubleshooting](#troubleshooting)

---

## What is Integration Testing?

**Simple explanation**: Testing that all parts of your application work together correctly.

Think of it like testing a car:
- ✅ **Unit Testing**: Testing the engine alone
- ✅ **Integration Testing**: Testing the engine + wheels + steering together
- ✅ **E2E Testing**: Test driving the entire car

**For Legally AI**, we're testing:
- Backend API ↔ Database
- Backend API ↔ Redis
- Backend API ↔ Celery Worker
- Frontend ↔ Backend API
- All together!

---

## What is Docker Compose?

**Docker Compose** is a tool that lets you run multiple services (database, backend, etc.) together with one command.

**Without Docker Compose**:
```bash
# Start PostgreSQL manually
brew install postgresql
pg_ctl start

# Start Redis manually
brew install redis
redis-server

# Start backend manually
cd backend
python -m uvicorn app.main:app

# Start Celery manually
celery -A app.tasks.celery_app worker

# Start frontend manually
cd frontend
npm run dev
```

**With Docker Compose**:
```bash
docker-compose up  # Everything starts!
```

**Magic!** ✨

---

## Installation

### Step 1: Install Docker Desktop

#### macOS
1. Download: https://www.docker.com/products/docker-desktop/
2. Open the `.dmg` file
3. Drag Docker to Applications
4. Launch Docker Desktop
5. Wait for Docker to start (whale icon in menu bar)

#### Windows
1. Download: https://www.docker.com/products/docker-desktop/
2. Run the installer
3. Follow setup wizard
4. Restart if prompted
5. Launch Docker Desktop

#### Linux (Ubuntu/Debian)
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt-get install docker-compose-plugin

# Add your user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

### Step 2: Verify Installation

Open a terminal and run:

```bash
docker --version
# Should see: Docker version 24.x.x or higher

docker-compose --version
# Should see: Docker Compose version 2.x.x or higher
```

✅ **If you see version numbers, you're ready!**

---

## Quick Start (5 minutes)

This will get your entire stack running in ~5 minutes.

### 1. Navigate to Backend Directory

```bash
cd /path/to/Legally_AI/backend
```

### 2. Check Your .env File

Make sure you have a `.env` file with these variables:

```bash
# Required for basic testing
DATABASE_URL=postgresql://legally_ai:password@postgres:5432/legally_ai
REDIS_URL=redis://redis:6379/0
SECRET_KEY=your-secret-key-here
LLM_PROVIDER=groq
GROQ_API_KEY=your-groq-api-key

# Optional but recommended
SENDGRID_API_KEY=your-sendgrid-key
FROM_EMAIL=noreply@legally-ai.com
FRONTEND_URL=http://localhost:3000
```

**Don't have a .env file?** Copy from example:
```bash
cp .env.example .env
# Then edit .env with your values
```

### 3. Start Everything!

```bash
docker-compose up
```

**What you'll see**:
```
Creating network "backend_default" with the default driver
Creating legally_ai_db ... done
Creating legally_ai_redis ... done
Creating legally_ai_backend ... done
Creating legally_ai_worker ... done
```

**Then logs will stream**:
- Green text = PostgreSQL logs
- Blue text = Redis logs
- Yellow text = Backend API logs
- Purple text = Celery worker logs

### 4. Wait for "Application startup complete"

Look for this message:
```
legally_ai_backend | INFO:     Application startup complete.
legally_ai_backend | INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ **When you see this, your backend is ready!**

### 5. Test It's Working

Open a **new terminal** (keep docker-compose running) and run:

```bash
curl http://localhost:8000/health
```

**Expected response**:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "app": "Legally AI"
}
```

✅ **If you see this, everything is working!**

---

## Step-by-Step Testing

Now let's test all the features systematically.

### Test 1: Check API Documentation

Open your browser and visit:
```
http://localhost:8000/docs
```

You should see **FastAPI's interactive API documentation** (Swagger UI).

This shows all 21 API endpoints you can test!

✅ **Try clicking on an endpoint and testing it directly in the browser.**

---

### Test 2: Register a New User

#### Option A: Using curl

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123!"
  }'
```

**Expected Response**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": "uuid-here",
    "email": "test@example.com",
    "tier": "free",
    "contracts_analyzed": 0,
    "analyses_remaining": 3,
    "is_active": true,
    "is_verified": false,
    "created_at": "2025-11-09T..."
  }
}
```

**✅ Copy the `access_token` - you'll need it for next tests!**

#### Option B: Using the API Docs

1. Go to http://localhost:8000/docs
2. Find `POST /api/auth/register`
3. Click "Try it out"
4. Fill in the request body:
   ```json
   {
     "email": "test@example.com",
     "password": "TestPassword123!"
   }
   ```
5. Click "Execute"
6. Copy the `access_token` from the response

---

### Test 3: Login

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123!"
  }'
```

**Expected**: Same response as registration with a new token.

---

### Test 4: Get User Profile

**Replace `YOUR_TOKEN` with your actual token from Test 2:**

```bash
curl http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Expected Response**:
```json
{
  "id": "uuid",
  "email": "test@example.com",
  "tier": "free",
  "contracts_analyzed": 0,
  "analyses_remaining": 3,
  "is_active": true,
  "is_verified": false,
  "created_at": "2025-11-09T..."
}
```

✅ **If you see your user details, authentication is working!**

---

### Test 5: Upload a Contract

First, create a test PDF file:

```bash
echo "This is a test contract" > test-contract.txt
```

Then upload it:

```bash
curl -X POST http://localhost:8000/api/contracts/upload \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@test-contract.txt"
```

**Expected Response**:
```json
{
  "contract_id": "uuid",
  "filename": "test-contract.txt",
  "status": "uploaded"
}
```

✅ **Copy the `contract_id` for the next test!**

---

### Test 6: Start Analysis

**Replace `CONTRACT_ID` and `YOUR_TOKEN`:**

```bash
curl -X POST http://localhost:8000/api/analyses \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "contract_id": "CONTRACT_ID",
    "output_language": "english"
  }'
```

**Expected Response**:
```json
{
  "id": "analysis-uuid",
  "contract_id": "contract-uuid",
  "status": "queued",
  ...
}
```

✅ **Copy the `analysis id` for the next test!**

---

### Test 7: Watch Analysis Progress (Real-Time!)

**Replace `ANALYSIS_ID` and `YOUR_TOKEN`:**

```bash
curl -N http://localhost:8000/api/analyses/ANALYSIS_ID/stream?token=YOUR_TOKEN
```

**What you'll see** (Server-Sent Events):
```
data: {"status": "queued", "progress": 0, "message": "Analysis queued"}

data: {"status": "parsing", "progress": 20, "message": "Parsing contract..."}

data: {"status": "analyzing", "progress": 60, "message": "Analyzing contract..."}

data: {"status": "done", "progress": 100, "message": "Analysis complete"}
```

**This is real-time streaming!** You'll see progress updates as they happen.

**To stop watching**: Press `Ctrl+C`

---

### Test 8: Get Analysis Results

**After analysis completes** (wait for "done" status):

```bash
curl http://localhost:8000/api/analyses/ANALYSIS_ID \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Expected**: Complete analysis results with all sections.

---

### Test 9: Export as PDF

```bash
curl http://localhost:8000/api/analyses/ANALYSIS_ID/export/pdf \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -o analysis.pdf
```

**Expected**: Downloads `analysis.pdf` file

**View it**:
```bash
open analysis.pdf  # macOS
xdg-open analysis.pdf  # Linux
start analysis.pdf  # Windows
```

---

### Test 10: Test Free Tier Limit

Try creating 4 analyses (free tier limit is 3):

```bash
# 1st analysis (should work)
curl -X POST http://localhost:8000/api/analyses \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"contract_id": "CONTRACT_ID", "output_language": "english"}'

# 2nd analysis (should work)
# Upload new contract first, then analyze

# 3rd analysis (should work)
# Upload new contract first, then analyze

# 4th analysis (should FAIL with 402 error)
```

**Expected for 4th attempt**:
```json
{
  "detail": "Free tier limit reached (3/3 analyses used). Upgrade to Premium for unlimited analyses."
}
```

✅ **If you get this error, free tier enforcement is working!**

---

### Test 11: Account Management

Get account details:

```bash
curl http://localhost:8000/api/account \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Expected Response**:
```json
{
  "id": "uuid",
  "email": "test@example.com",
  "tier": "free",
  "contracts_analyzed": 3,
  "analyses_remaining": 0,
  "total_contracts": 3,
  "total_analyses": 3,
  "tier_limit": 3,
  ...
}
```

---

### Test 12: GDPR Data Export

Export all your data:

```bash
curl http://localhost:8000/api/account/export \
  -H "Authorization: Bearer YOUR_TOKEN" \
  > my-data.json
```

**View it**:
```bash
cat my-data.json | python -m json.tool  # Pretty print
```

**Expected**: JSON with all your user data, contracts, analyses, and feedback.

---

## Monitoring & Debugging

### View Logs

**All services**:
```bash
docker-compose logs -f
```

**Just backend**:
```bash
docker-compose logs -f backend
```

**Just database**:
```bash
docker-compose logs -f postgres
```

**Just Celery worker**:
```bash
docker-compose logs -f celery_worker
```

### Check Database

Connect to PostgreSQL:

```bash
docker-compose exec postgres psql -U legally_ai -d legally_ai
```

**Useful queries**:
```sql
-- List all users
SELECT id, email, tier, contracts_analyzed FROM users;

-- List all contracts
SELECT id, filename, status, created_at FROM contracts;

-- List all analyses
SELECT id, status, created_at FROM analyses;

-- Exit
\q
```

### Check Redis

Connect to Redis:

```bash
docker-compose exec redis redis-cli
```

**Useful commands**:
```bash
# List all keys
KEYS *

# Check Celery tasks
LLEN celery

# Exit
exit
```

---

## Stopping & Cleaning Up

### Stop Services (Keep Data)

```bash
docker-compose down
```

This stops all services but **keeps your data** (database, uploaded files).

### Stop Services (Delete Everything)

```bash
docker-compose down -v
```

This stops services and **deletes all data** (fresh start next time).

### Restart Services

```bash
docker-compose restart
```

### Rebuild After Code Changes

```bash
docker-compose up --build
```

---

## Troubleshooting

### Problem: Port Already in Use

**Error**:
```
Error: Bind for 0.0.0.0:5432 failed: port is already allocated
```

**Solution**: Another PostgreSQL is running. Stop it:

```bash
# macOS
brew services stop postgresql

# Linux
sudo systemctl stop postgresql

# Or change the port in docker-compose.yml
ports:
  - "5433:5432"  # Use 5433 instead
```

### Problem: Database Connection Failed

**Error**: `could not connect to server: Connection refused`

**Solution**: Wait for health check to complete:

```bash
docker-compose ps
# Wait until postgres shows "(healthy)"
```

### Problem: Celery Worker Not Processing Tasks

**Check logs**:
```bash
docker-compose logs celery_worker
```

**Common issues**:
1. Redis not connected - Check Redis is running
2. Task not registered - Restart worker: `docker-compose restart celery_worker`

### Problem: Out of Disk Space

**Check disk usage**:
```bash
docker system df
```

**Clean up**:
```bash
# Remove old images and containers
docker system prune

# Remove everything (careful!)
docker system prune -a --volumes
```

### Problem: Can't Access API

**Check if backend is running**:
```bash
docker-compose ps
```

**Check logs**:
```bash
docker-compose logs backend
```

**Try accessing directly**:
```bash
curl http://localhost:8000/health
```

---

## Next Steps

After completing these tests:

1. ✅ **Test Frontend Integration**
   - Start frontend: `cd frontend && npm run dev`
   - Open http://localhost:3000
   - Test the full user interface

2. ✅ **Run Automated Tests**
   - Backend: `cd backend && pytest`
   - Frontend: `cd frontend && npm run test`

3. ✅ **Performance Testing**
   - Run Lighthouse audit
   - Test API response times
   - Check database query performance

4. ✅ **Deploy to Staging**
   - Follow `TESTING_DEPLOYMENT_GUIDE.md`
   - Deploy backend to Railway/Fly.io
   - Deploy frontend to Vercel

---

## Quick Reference

### Essential Commands

```bash
# Start everything
docker-compose up

# Start in background
docker-compose up -d

# Stop everything
docker-compose down

# View logs
docker-compose logs -f

# Restart a service
docker-compose restart backend

# Rebuild and start
docker-compose up --build

# Check status
docker-compose ps

# Clean up
docker-compose down -v
```

### Test Endpoints

```bash
# Health check
curl http://localhost:8000/health

# API docs
open http://localhost:8000/docs

# Register
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!"}'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!"}'

# Get profile
curl http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Need Help?

- 📖 **Docker Docs**: https://docs.docker.com/
- 📖 **Docker Compose Docs**: https://docs.docker.com/compose/
- 📖 **FastAPI Docs**: https://fastapi.tiangolo.com/
- 📖 **PostgreSQL Docs**: https://www.postgresql.org/docs/

---

**Last Updated**: 2025-11-09
**Status**: Ready for Integration Testing
**Difficulty**: Beginner-Friendly 🟢

**Happy Testing!** 🚀
