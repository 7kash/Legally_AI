# Quick Start Guide - Testing the Bug Fix

This is a condensed guide to quickly test the duplicate analysis bug fix.

## Prerequisites

- Python 3.9+
- Docker & Docker Compose (recommended)
- OR PostgreSQL & Redis installed locally

## Option 1: Docker Compose (Easiest - 2 minutes)

```bash
cd backend

# Start all services
docker-compose up

# In another terminal, run the test
docker exec -it legally-ai-api python tests/test_bug_fix.py
```

That's it! The test will verify the bug fix is working.

## Option 2: Manual Setup (5 minutes)

### Step 1: Start Database & Redis

```bash
cd backend

# Start PostgreSQL
docker run --name legally-ai-db \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=legally_ai \
  -p 5432:5432 -d postgres:15

# Start Redis
docker run --name legally-ai-redis \
  -p 6379:6379 -d redis:7
```

### Step 2: Setup Python Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python scripts/init_db.py
```

### Step 3: Start Services (3 terminals)

**Terminal 1 - API Server:**
```bash
cd backend
source venv/bin/activate
python -m app.main
```

**Terminal 2 - Celery Worker:**
```bash
cd backend
source venv/bin/activate
celery -A app.celery_app worker --loglevel=info
```

**Terminal 3 - Run Test:**
```bash
cd backend
source venv/bin/activate
python tests/test_bug_fix.py
```

## Expected Result

```
🧪 Testing Bug Fix: Duplicate Analysis Records
================================================

Step 1: Creating test contract...
✅ Contract created: abc123...

Step 2: Creating analysis...
✅ Analysis created: def456...
   Status: queued

Step 3: Checking for duplicate records...
✅ PASS: Only 1 analysis record exists (no duplicates!)

Step 4: Streaming analysis events...
📡 Event: status_change - Analysis started
📡 Event: progress - Starting document preparation
📡 Event: progress - Document preparation completed
📡 Event: status_change - Analysis completed successfully

Step 5: Verifying final status...
✅ PASS: Analysis completed successfully
✅ PASS: SSE stream received events correctly

================================================
🎉 All tests passed! Bug fix verified.
================================================
```

## What the Test Verifies

1. ✅ Only ONE Analysis record is created (no duplicates)
2. ✅ Celery task receives the correct `analysis_id`
3. ✅ Celery task updates the existing record (doesn't create new one)
4. ✅ SSE stream receives events with the correct `analysis_id`
5. ✅ Analysis completes successfully (not stuck in "queued")

## The Bug Fix

**Before (Broken):**
- API creates Analysis A → Sends `contract_id` to Celery
- Celery creates Analysis B → Creates events for B
- SSE polls Analysis A → Never receives events → STUCK!

**After (Fixed):**
- API creates Analysis A → Sends `analysis_id` to Celery
- Celery updates Analysis A → Creates events for A
- SSE polls Analysis A → Receives events → SUCCESS!

## Troubleshooting

**Cannot connect to API:**
```bash
# Check API is running
curl http://localhost:8000/health
```

**Database connection failed:**
```bash
# Check PostgreSQL is running
docker ps | grep postgres
```

**Celery not processing tasks:**
```bash
# Check Redis is running
redis-cli ping

# Check Celery logs
# Look at Terminal 2 for errors
```

## Next Steps

After the test passes:

1. Review the implementation:
   - `backend/app/api/analyses.py` (line 83-86)
   - `backend/app/tasks/analyze_contract.py` (line 60-95)

2. Read the full testing guide: `TESTING.md`

3. Test with real contract files

4. Deploy to staging/production

## Cleanup

```bash
# Stop services
docker-compose down

# Remove volumes (if needed)
docker-compose down -v
```

---

**For detailed testing instructions, see `TESTING.md`**
