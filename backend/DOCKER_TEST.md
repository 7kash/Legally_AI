# Docker Compose Testing Guide

The easiest way to test the bug fix using only Docker Compose.

## Quick Test (One Command)

```bash
cd backend
./test-docker.sh
```

That's it! This will:
1. ✅ Start PostgreSQL, Redis, API, and Celery worker
2. ✅ Wait for all services to be ready
3. ✅ Run the automated bug fix test
4. ✅ Show you the results

## Expected Output

```
========================================
  Legally AI - Docker Compose Test
========================================

🐳 Starting Docker Compose services...

⏳ Waiting for services to be ready...

  Waiting for PostgreSQL... ✅
  Waiting for Redis... ✅
  Waiting for API... ✅
  Waiting for Celery worker... ✅

========================================
  🧪 Running Bug Fix Test
========================================

============================================================
  🧪 Docker Compose Bug Fix Test
============================================================

[Step 0] Waiting for API to be ready...
✅ API is ready

[Step 1] Creating test contract...
✅ Using contract ID: abc123-...

[Step 2] Creating analysis...
✅ Analysis created: def456-...
   Status: queued

[Step 3] Checking if Celery worker picked up the task...
✅ Celery worker started processing! Status: running

[Step 4] Streaming analysis events (SSE)...
📡 Event #1: status_change - Analysis started
📡 Event #2: progress - Starting document preparation
📡 Event #3: progress - Document preparation completed
📡 Event #4: progress - Starting contract analysis
📡 Event #5: progress - Contract analysis completed
📡 Event #6: status_change - Analysis completed successfully
✅ Analysis completed!

[Step 5] Verifying final status...

   Final status: completed
✅ Analysis completed successfully!
✅ Bug fix is working! ✅

============================================================
  📊 Test Results Summary
============================================================
✅ Analysis created: YES
✅ Celery processing: YES
✅ Events received: YES
✅ Analysis completed: YES

============================================================
  🎉 SUCCESS! Bug fix is working!
============================================================

========================================
  ✅ TEST PASSED
========================================

The duplicate analysis bug is FIXED! 🎉
```

## What the Test Verifies

The test confirms that the bug fix is working by checking:

1. ✅ **Analysis Creation**: API creates an analysis successfully
2. ✅ **Celery Processing**: Celery worker picks up and processes the task
3. ✅ **No Duplicates**: Only ONE analysis record exists (not two)
4. ✅ **SSE Events**: Events are received through the SSE stream
5. ✅ **Completion**: Analysis completes successfully (not stuck in "queued")

## If the Test Fails

If you see `❌ TEST FAILED`, the script will show troubleshooting steps:

### Check Celery Worker Logs

```bash
docker-compose logs celery
```

Look for:
- ✅ `Task analyze_contract[...] received`
- ✅ `Task analyze_contract[...] succeeded`
- ❌ Error messages or exceptions

### Check API Logs

```bash
docker-compose logs api
```

### Check Database State

```bash
docker-compose exec api python scripts/diagnose.py
```

This shows:
- What tables exist
- The status of the latest analysis
- How many events were created

### View All Logs

```bash
docker-compose logs
```

## Manual Testing

If you want to test manually:

### 1. Start Services

```bash
docker-compose up -d
```

### 2. Check Services Are Running

```bash
docker-compose ps
```

Should show all services as "Up":
- `legally-ai-db` (postgres)
- `legally-ai-redis` (redis)
- `legally-ai-api` (api)
- `legally-ai-celery` (celery)

### 3. Create an Analysis

```bash
# Create analysis
curl -X POST http://localhost:8000/api/v1/analyses \
  -H "Content-Type: application/json" \
  -d '{
    "contract_id": "00000000-0000-0000-0000-000000000001",
    "output_language": "english"
  }'

# Save the returned "id" as ANALYSIS_ID
```

### 4. Stream Events

```bash
# Replace ANALYSIS_ID with the ID from step 3
curl -N http://localhost:8000/api/v1/analyses/ANALYSIS_ID/stream
```

You should see events streaming:
```
data: {"type":"status_change","message":"Analysis started"...}
data: {"type":"progress","message":"Starting document preparation"...}
...
```

### 5. Check Final Status

```bash
curl http://localhost:8000/api/v1/analyses/ANALYSIS_ID
```

Should show:
```json
{
  "id": "ANALYSIS_ID",
  "status": "completed",
  ...
}
```

## Viewing Logs in Real-Time

```bash
# All services
docker-compose logs -f

# Just API
docker-compose logs -f api

# Just Celery
docker-compose logs -f celery

# Just Postgres
docker-compose logs -f postgres
```

## Stopping Services

```bash
# Stop services (keep data)
docker-compose down

# Stop services and delete data
docker-compose down -v
```

## Rebuilding After Code Changes

If you modify the code:

```bash
# Rebuild and restart
docker-compose up -d --build

# Run test again
./test-docker.sh
```

## Troubleshooting

### "Cannot connect to Docker daemon"

Make sure Docker is running:
```bash
docker ps
```

### "Port already in use"

Stop conflicting services:
```bash
# Check what's using port 8000
lsof -i :8000

# Stop existing containers
docker-compose down
```

### "Build failed"

Clean and rebuild:
```bash
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Services not starting

Check logs for errors:
```bash
docker-compose logs
```

## Understanding the Bug Fix

The test verifies this flow works correctly:

**Before Fix (Broken)**:
```
API creates Analysis A (ID: abc123)
  ↓ sends contract_id
Celery creates Analysis B (ID: def456) ❌ DUPLICATE!
  ↓ creates events for B
SSE polls for events from A
  ↓ never receives events
STUCK IN "QUEUED" FOREVER ❌
```

**After Fix (Working)**:
```
API creates Analysis A (ID: abc123)
  ↓ sends analysis_id (abc123)
Celery updates Analysis A ✅ NO DUPLICATE
  ↓ creates events for A
SSE polls for events from A
  ↓ receives events correctly
COMPLETES SUCCESSFULLY ✅
```

## Next Steps

After the test passes:

1. Review the code changes:
   - `backend/app/api/analyses.py` (line 83-86)
   - `backend/app/tasks/analyze_contract.py` (line 60-95)

2. Test with real contract files

3. Deploy to staging/production

---

**For detailed manual testing, see `TESTING.md`**
