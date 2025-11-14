# Testing the Bug Fix - Step by Step Guide

This guide will walk you through testing the critical bug fix for duplicate analysis records.

## Prerequisites

You'll need:
- Python 3.9+
- PostgreSQL
- Redis
- Terminal access

## Quick Start (Recommended)

### Option 1: Using Docker Compose (Easiest)

```bash
# 1. Start all services
cd backend
docker-compose up -d

# 2. Run the test script
python tests/test_bug_fix.py

# 3. View logs
docker-compose logs -f api
docker-compose logs -f celery
```

### Option 2: Manual Setup

Follow the detailed steps below.

---

## Step 1: Install Dependencies

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## Step 2: Set Up PostgreSQL Database

### Option A: Using Docker (Recommended)

```bash
# Start PostgreSQL in Docker
docker run --name legally-ai-db \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=legally_ai \
  -p 5432:5432 \
  -d postgres:15

# Verify it's running
docker ps | grep legally-ai-db
```

### Option B: Using Local PostgreSQL

```bash
# Create database
createdb legally_ai

# Or using psql
psql -U postgres -c "CREATE DATABASE legally_ai;"
```

---

## Step 3: Set Up Redis

### Option A: Using Docker (Recommended)

```bash
# Start Redis in Docker
docker run --name legally-ai-redis \
  -p 6379:6379 \
  -d redis:7

# Verify it's running
docker ps | grep legally-ai-redis
```

### Option B: Using Local Redis

```bash
# Start Redis server
redis-server

# Or as a service
sudo systemctl start redis
```

---

## Step 4: Configure Environment

```bash
cd backend

# Copy example environment file
cp .env.example .env

# Edit .env with your settings (default values should work for local testing)
nano .env  # or your preferred editor
```

Verify these settings in `.env`:
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/legally_ai
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
GROQ_API_KEY=your_api_key_here  # Optional for basic testing
```

---

## Step 5: Initialize Database

```bash
# Run the database setup script
python scripts/init_db.py

# You should see:
# ✅ Database initialized successfully
# ✅ Tables created: contracts, analyses, analysis_events
```

---

## Step 6: Start the Services

You'll need **3 terminal windows**.

### Terminal 1: FastAPI Server

```bash
cd backend
source venv/bin/activate

# Start API server
python -m app.main

# Or with auto-reload
uvicorn app.main:app --reload --port 8000

# You should see:
# INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Terminal 2: Celery Worker

```bash
cd backend
source venv/bin/activate

# Start Celery worker
celery -A app.celery_app worker --loglevel=info

# You should see:
# [tasks]
#   . analyze_contract
#   . cleanup_old_analyses
# celery@hostname ready.
```

### Terminal 3: Testing Commands

Keep this terminal open for running test commands.

---

## Step 7: Verify Services Are Running

In Terminal 3:

```bash
# Test API is running
curl http://localhost:8000/health
# Expected: {"status":"healthy"}

# Test Redis is running
redis-cli ping
# Expected: PONG

# Test PostgreSQL is running
psql -U postgres -d legally_ai -c "SELECT 1;"
# Expected: Shows a table with value 1
```

---

## Step 8: Run the Bug Fix Test

### Automated Test (Recommended)

```bash
cd backend
source venv/bin/activate

# Run the comprehensive test script
python tests/test_bug_fix.py

# This will:
# 1. Create a test contract
# 2. Create an analysis
# 3. Verify only ONE analysis record exists
# 4. Monitor SSE stream for events
# 5. Verify analysis completes successfully
```

Expected output:
```
🧪 Testing Bug Fix: Duplicate Analysis Records
================================================

Step 1: Creating test contract...
✅ Contract created: 123e4567-e89b-12d3-a456-426614174000

Step 2: Creating analysis...
✅ Analysis created: 987fcdeb-51a2-43b1-9876-543210fedcba
   Status: queued

Step 3: Checking for duplicate records...
✅ PASS: Only 1 analysis record exists (no duplicates!)

Step 4: Streaming analysis events...
📡 Event: status_change - Analysis started
📡 Event: progress - Starting document preparation
📡 Event: progress - Document preparation completed
📡 Event: progress - Starting contract analysis
📡 Event: progress - Contract analysis completed
📡 Event: status_change - Analysis completed successfully

Step 5: Verifying final status...
✅ PASS: Analysis completed successfully
✅ PASS: SSE stream received events correctly

================================================
🎉 All tests passed! Bug fix verified.
================================================
```

### Manual Testing

#### Test 1: Create a Contract

```bash
curl -X POST http://localhost:8000/api/v1/contracts \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "00000000-0000-0000-0000-000000000001",
    "filename": "test-contract.pdf",
    "file_path": "/tmp/test.pdf",
    "file_size": 1024,
    "mime_type": "application/pdf",
    "extracted_text": "This is a test contract..."
  }'

# Save the returned "id" for next steps
```

#### Test 2: Create an Analysis

```bash
# Replace <contract_id> with the ID from Test 1
curl -X POST http://localhost:8000/api/v1/analyses \
  -H "Content-Type: application/json" \
  -d '{
    "contract_id": "<contract_id>",
    "output_language": "english"
  }'

# Save the returned "id" as <analysis_id>
```

#### Test 3: Check for Duplicates (The Bug Test!)

```bash
# Connect to database and count analysis records
psql -U postgres -d legally_ai -c "SELECT COUNT(*) FROM analyses;"

# Expected: 1 (only one record)
# Before bug fix: 2 (duplicate records!)
```

#### Test 4: Stream Events (SSE)

```bash
# Replace <analysis_id> with the ID from Test 2
curl -N http://localhost:8000/api/v1/analyses/<analysis_id>/stream

# You should see events streaming in real-time:
# data: {"type":"status_change","message":"Analysis started"...}
# data: {"type":"progress","message":"Starting document preparation"...}
# ...

# Before bug fix: This would hang forever (no events received)
```

#### Test 5: Get Final Analysis Result

```bash
# Replace <analysis_id> with the ID from Test 2
curl http://localhost:8000/api/v1/analyses/<analysis_id>

# Expected: status should be "completed" (not stuck in "queued")
```

---

## Step 9: Verify Bug Fix in Logs

### Check Celery Worker Logs (Terminal 2)

Look for these lines:
```
[INFO/MainProcess] Task analyze_contract[<task_id>] received
[INFO/MainProcess] Fetching existing Analysis record: <analysis_id>
[INFO/MainProcess] Analysis status updated: running
[INFO/MainProcess] Analysis completed successfully
[INFO/MainProcess] Task analyze_contract[<task_id>] succeeded
```

**Key Indicators the Bug is Fixed:**
- ✅ Only ONE analysis_id mentioned throughout the logs
- ✅ "Fetching existing Analysis record" (not "Creating new Analysis")
- ✅ Task completes successfully

**Before Bug Fix (What You'd See):**
- ❌ TWO different analysis_ids in logs
- ❌ "Creating new Analysis record"
- ❌ SSE stream never receives events

### Check Database Records

```bash
# View all analyses
psql -U postgres -d legally_ai -c "SELECT id, status, created_at FROM analyses;"

# View analysis events
psql -U postgres -d legally_ai -c "SELECT analysis_id, event_type, message FROM analysis_events ORDER BY created_at;"

# Expected: All events have the SAME analysis_id
```

---

## Step 10: Performance Test (Optional)

Test multiple concurrent analyses:

```bash
cd backend
python tests/load_test.py

# This will create 10 concurrent analyses and verify:
# - No duplicate records
# - All analyses complete successfully
# - SSE streams work correctly
```

---

## Troubleshooting

### Issue: "Database connection failed"

```bash
# Check PostgreSQL is running
docker ps | grep postgres

# Check connection
psql -U postgres -d legally_ai -c "SELECT 1;"

# Verify DATABASE_URL in .env
cat .env | grep DATABASE_URL
```

### Issue: "Celery worker not picking up tasks"

```bash
# Check Redis is running
redis-cli ping

# Check Celery logs for errors
# In Terminal 2, look for any ERROR messages

# Restart Celery worker
# Ctrl+C in Terminal 2, then restart:
celery -A app.celery_app worker --loglevel=info
```

### Issue: "ImportError" or "ModuleNotFoundError"

```bash
# Make sure you're in the virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Verify Python path
echo $PYTHONPATH
```

### Issue: "SSE stream times out"

```bash
# Check Celery worker is running and processing tasks
# Look in Terminal 2 for task execution logs

# Check Redis connection
redis-cli ping

# Verify analysis was created
curl http://localhost:8000/api/v1/analyses/<analysis_id>
```

---

## Cleanup

### Stop Services

```bash
# Terminal 1 (API): Ctrl+C
# Terminal 2 (Celery): Ctrl+C

# Stop Docker containers (if used)
docker stop legally-ai-db legally-ai-redis

# Remove containers (optional)
docker rm legally-ai-db legally-ai-redis
```

### Clean Database

```bash
# Drop and recreate database
dropdb legally_ai
createdb legally_ai

# Or truncate tables
psql -U postgres -d legally_ai -c "TRUNCATE analyses, contracts, analysis_events CASCADE;"
```

---

## Summary

The bug fix ensures:

1. ✅ **API endpoint** creates ONE Analysis record with a unique ID
2. ✅ **API endpoint** passes this `analysis_id` to the Celery task
3. ✅ **Celery task** receives `analysis_id` and fetches the existing record
4. ✅ **Celery task** updates the same record (doesn't create a duplicate)
5. ✅ **SSE stream** polls for events with the correct `analysis_id`
6. ✅ **Events are received** and analysis completes successfully

**Before the fix:**
- API created Analysis A
- Celery created Analysis B (duplicate!)
- SSE polled for events from A, but events were created for B
- Result: Stuck in "queued" forever

**After the fix:**
- API creates Analysis A
- Celery updates Analysis A (no duplicate)
- SSE polls for events from A, receives events for A
- Result: Analysis completes successfully ✅

---

## Next Steps

After verifying the bug fix works:

1. Run the full test suite: `pytest tests/`
2. Review the implementation in `backend/app/api/analyses.py` and `backend/app/tasks/analyze_contract.py`
3. Deploy to staging environment
4. Test with real contract files

For production deployment, see `../DEPLOYMENT_GUIDE.md`.
