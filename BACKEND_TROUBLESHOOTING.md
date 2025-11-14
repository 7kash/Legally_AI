# Backend Troubleshooting Guide

## Issue: Registration shows "Failed to fetch"

This means the backend at `http://localhost:8000` is not responding.

## Quick Fix Steps

**IMPORTANT:** All docker commands must be run from the `backend/` directory!

```bash
cd /Users/ekaterinamatyushina/Legally_AI/backend

# 1. Check if containers are running
docker compose ps

# 2. If not running or unhealthy, restart everything
docker compose down -v
docker compose build --no-cache
docker compose up -d

# 3. Wait 10 seconds for startup
sleep 10

# 4. Check logs for errors
docker compose logs api --tail 30

# 5. Test the health endpoint
curl http://localhost:8000/health
```

## Common Issues

### 1. Wrong Directory
❌ Running from `/Users/ekaterinamatyushina/Legally_AI/`
✅ Must run from `/Users/ekaterinamatyushina/Legally_AI/backend/`

### 2. Containers Not Running
```bash
cd backend
docker compose ps
```

If containers show as "exited" or not listed:
```bash
docker compose up -d
docker compose logs api --tail 50
```

### 3. Port 8000 Already in Use
```bash
lsof -i :8000
# Kill the process if needed
```

### 4. Database Connection Issues
```bash
docker compose logs postgres --tail 20
```

Make sure postgres container is healthy before API starts.

### 5. API Container Crashes on Startup

View logs:
```bash
docker compose logs api --tail 100
```

Common causes:
- Missing environment variables (GROQ_API_KEY)
- Database not ready
- Python import errors
- Port conflicts

## Step-by-Step Rebuild

```bash
# Navigate to backend directory
cd /Users/ekaterinamatyushina/Legally_AI/backend

# Pull latest code
cd ..
git pull origin claude/push-celery-duplicate-fix-0128AnbZuzaJLX1Qa3QUHqrA
cd backend

# Stop everything
docker compose down

# Remove volumes (recreate database with User table)
docker compose down -v

# Rebuild API container
docker compose build --no-cache api

# Start all services
docker compose up -d

# Monitor startup
docker compose logs -f api
# Press Ctrl+C when you see "Application startup complete"

# Test health endpoint
curl http://localhost:8000/health
# Should return: {"status":"healthy"}

# Test API docs
open http://localhost:8000/docs
# Should show FastAPI Swagger UI with auth endpoints
```

## Verify Backend is Working

1. **Health Check:**
   ```bash
   curl http://localhost:8000/health
   ```
   Expected: `{"status":"healthy"}`

2. **API Docs:**
   Open http://localhost:8000/docs in browser
   Should see:
   - POST /api/v1/auth/register
   - POST /api/v1/auth/login
   - GET /api/v1/auth/me
   - etc.

3. **Test Registration:**
   ```bash
   curl -X POST http://localhost:8000/api/v1/auth/register \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","password":"test123456"}'
   ```

   Expected: JSON response with `access_token` and `user` object

## Still Not Working?

Run these diagnostic commands and check for errors:

```bash
cd /Users/ekaterinamatyushina/Legally_AI/backend

# 1. Container status
docker compose ps

# 2. All logs
docker compose logs

# 3. API logs specifically
docker compose logs api --tail 100

# 4. Database logs
docker compose logs postgres --tail 20

# 5. Check if API process is running inside container
docker compose exec api ps aux | grep uvicorn

# 6. Test from inside the container
docker compose exec api curl http://localhost:8000/health
```

Send me the output from these commands and I can help debug further!
