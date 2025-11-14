# Docker Compose Troubleshooting Guide

## Error: "Container legally-ai-db exited (1)"

This means PostgreSQL container failed to start. Follow these steps:

### Step 1: Check PostgreSQL Logs

```bash
cd backend
docker compose logs postgres
```

Look for error messages like:
- `port 5432 is already in use`
- `permission denied`
- `database files incompatible`

### Step 2: Quick Fixes

Try these fixes in order:

#### Fix A: Stop Local PostgreSQL (if running)

```bash
# Check if local PostgreSQL is using port 5432
sudo lsof -i :5432

# Stop local PostgreSQL
sudo systemctl stop postgresql
# or on Mac:
brew services stop postgresql

# Try again
docker compose up -d
```

#### Fix B: Remove Corrupted Data Volume

```bash
# Stop and remove everything including volumes
docker compose down -v

# Start fresh
docker compose up -d
```

#### Fix C: Force Remove Old Container

```bash
# Stop everything
docker compose down

# Force remove the specific container
docker rm -f legally-ai-db

# Remove volume
docker volume rm backend_postgres_data

# Start again
docker compose up -d
```

#### Fix D: Change PostgreSQL Port

If port 5432 is in use by something you can't stop, edit `docker-compose.yml`:

```yaml
postgres:
  ports:
    - "5433:5432"  # Change 5432 to 5433
```

Then update `.env` or environment variables:
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/legally_ai
```

### Step 3: Verify Services Are Running

```bash
# Check all containers
docker compose ps

# Should show:
#   legally-ai-db      running
#   legally-ai-redis   running
#   legally-ai-api     running
#   legally-ai-celery  running
```

### Step 4: Test Database Connection

```bash
# Connect to PostgreSQL
docker compose exec postgres psql -U postgres -d legally_ai -c "SELECT 1;"

# Expected output:
#  ?column?
# ----------
#         1
```

---

## Error: "Celery worker not processing tasks"

### Check Celery Logs

```bash
docker compose logs celery
```

Look for:
- ✅ `celery@hostname ready.`
- ✅ `Task analyze_contract[...] received`
- ❌ Connection errors to Redis
- ❌ Import errors

### Fix: Rebuild Celery Container

```bash
docker compose down
docker compose build celery
docker compose up -d
```

---

## Error: "Cannot connect to Redis"

### Check Redis Status

```bash
# Check if Redis is running
docker compose ps redis

# Test Redis connection
docker compose exec redis redis-cli ping
# Expected: PONG
```

### Fix: Restart Redis

```bash
docker compose restart redis
```

---

## Error: "API not responding"

### Check API Logs

```bash
docker compose logs api
```

### Fix: Rebuild API Container

```bash
docker compose down
docker compose build api
docker compose up -d
```

---

## Complete Reset (Nuclear Option)

If nothing works, do a complete reset:

```bash
# Stop all containers
docker compose down -v

# Remove all images
docker compose rm -f

# Remove volumes
docker volume prune -f

# Rebuild everything from scratch
docker compose build --no-cache

# Start fresh
docker compose up -d

# Wait for services to be ready
sleep 10

# Run test
./test-docker.sh
```

---

## Checking Service Health

### Quick Health Check

```bash
# API
curl http://localhost:8000/health
# Expected: {"status":"healthy"}

# Redis
docker compose exec redis redis-cli ping
# Expected: PONG

# PostgreSQL
docker compose exec postgres pg_isready -U postgres
# Expected: postgres:5432 - accepting connections
```

### View All Logs in Real-Time

```bash
docker compose logs -f
```

Press `Ctrl+C` to stop.

### View Specific Service Logs

```bash
# API only
docker compose logs -f api

# Celery only
docker compose logs -f celery

# PostgreSQL only
docker compose logs -f postgres

# Redis only
docker compose logs -f redis
```

---

## Common Issues & Solutions

### Issue: "Port already in use"

**Symptoms:**
- `bind: address already in use`
- Container fails to start

**Solution:**
```bash
# Find what's using the port
sudo lsof -i :8000   # API port
sudo lsof -i :5432   # PostgreSQL port
sudo lsof -i :6379   # Redis port

# Kill the process or change ports in docker-compose.yml
```

### Issue: "Permission denied"

**Symptoms:**
- `permission denied while trying to connect`
- Volume mount errors

**Solution:**
```bash
# On Linux, fix permissions
sudo chown -R $USER:$USER backend/

# Remove and recreate volumes
docker compose down -v
docker compose up -d
```

### Issue: "Database does not exist"

**Symptoms:**
- `database "legally_ai" does not exist`

**Solution:**
```bash
# The database is auto-created, but if not:
docker compose exec postgres psql -U postgres -c "CREATE DATABASE legally_ai;"

# Or restart to trigger auto-creation
docker compose restart postgres
```

### Issue: "Module not found"

**Symptoms:**
- `ModuleNotFoundError: No module named 'app'`
- Import errors in logs

**Solution:**
```bash
# Rebuild containers
docker compose down
docker compose build --no-cache
docker compose up -d
```

---

## Getting Help

If issues persist:

1. **Collect logs:**
```bash
docker compose logs > docker-logs.txt
```

2. **Check environment:**
```bash
docker compose config
```

3. **Check system resources:**
```bash
docker stats
```

4. **Verify Docker version:**
```bash
docker --version
docker compose version
```

---

## Working Configuration Checklist

Before running tests, verify:

- [ ] Docker is installed and running
- [ ] Docker Compose is installed (v2.0+)
- [ ] Ports 5432, 6379, 8000 are available
- [ ] At least 2GB RAM available for containers
- [ ] No local PostgreSQL/Redis conflicting
- [ ] Files have correct permissions

Once everything is green, run:
```bash
./test-docker.sh
```
