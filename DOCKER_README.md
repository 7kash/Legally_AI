# Legally AI - Docker Setup

This directory contains Docker configuration for the Legally AI backend.

## Quick Start

### 1. Prerequisites

- Docker 20.10+
- Docker Compose 2.0+

### 2. Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your Groq API key
nano .env
```

Required environment variables:
- `GROQ_API_KEY` - Your Groq API key (get from https://console.groq.com)
- `SECRET_KEY` - Random string for JWT signing
- `POSTGRES_PASSWORD` - Database password
- `REDIS_PASSWORD` - Redis password

### 3. Start Services

```bash
# Start all services (backend, postgres, redis, celery)
docker-compose up -d

# View logs
docker-compose logs -f backend

# Check status
docker-compose ps
```

### 4. Access Services

- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Flower (Celery Monitor)**: http://localhost:5555 (dev profile only)

### 5. Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: deletes all data)
docker-compose down -v
```

## Architecture

```
┌─────────────────────────────────────────┐
│          Docker Compose Stack           │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────────┐  ┌──────────────┐   │
│  │   Backend    │  │   Celery     │   │
│  │   FastAPI    │  │   Worker     │   │
│  │   Port: 8000 │  │              │   │
│  └──────┬───────┘  └──────┬───────┘   │
│         │                  │            │
│         └──────┬───────────┘            │
│                │                        │
│     ┌──────────▼──────────┐            │
│     │    PostgreSQL       │            │
│     │    Port: 5432       │            │
│     └─────────────────────┘            │
│                                         │
│     ┌─────────────────────┐            │
│     │      Redis          │            │
│     │    Port: 6379       │            │
│     └─────────────────────┘            │
│                                         │
└─────────────────────────────────────────┘
```

## Services

### Backend (FastAPI)
- **Image**: Built from `Dockerfile`
- **Port**: 8000
- **Features**:
  - FastAPI REST API
  - JWT authentication
  - File upload
  - Health checks
  - Hot reload (dev mode)

### PostgreSQL
- **Image**: postgres:15-alpine
- **Port**: 5432
- **Persistent Storage**: `postgres_data` volume
- **Initialization**: `backend/db/init.sql`

### Redis
- **Image**: redis:7-alpine
- **Port**: 6379
- **Persistent Storage**: `redis_data` volume
- **Use**: Celery queue + cache

### Celery Worker
- **Image**: Same as backend
- **Features**:
  - Async contract analysis
  - Background jobs
  - 2 concurrent workers

### Celery Beat (optional)
- **Image**: Same as backend
- **Features**:
  - Scheduled tasks
  - Deadline reminders

### Flower (dev only)
- **Image**: Same as backend
- **Port**: 5555
- **Features**:
  - Celery monitoring
  - Task inspection
  - Worker stats

## Development Workflow

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f postgres
docker-compose logs -f celery_worker
```

### Rebuild After Code Changes

```bash
# Rebuild and restart
docker-compose up -d --build backend

# Or rebuild specific service
docker-compose build backend
docker-compose restart backend
```

### Run Migrations (when implemented)

```bash
docker-compose exec backend alembic upgrade head
```

### Access Database

```bash
# PostgreSQL shell
docker-compose exec postgres psql -U legally_ai -d legally_ai

# Run SQL commands
docker-compose exec postgres psql -U legally_ai -d legally_ai -c "SELECT * FROM users;"
```

### Access Redis

```bash
# Redis CLI
docker-compose exec redis redis-cli -a legally_ai_redis_dev

# Check keys
docker-compose exec redis redis-cli -a legally_ai_redis_dev KEYS '*'
```

### Run Commands in Backend Container

```bash
# Shell access
docker-compose exec backend bash

# Run Python script
docker-compose exec backend python -c "print('Hello from backend')"

# Run tests
docker-compose exec backend pytest
```

## Troubleshooting

### Backend won't start

```bash
# Check logs
docker-compose logs backend

# Common issues:
# 1. GROQ_API_KEY not set → add to .env
# 2. Port 8000 already in use → change BACKEND_PORT in .env
# 3. Postgres not ready → wait 10s and restart
```

### Database connection errors

```bash
# Check if postgres is running
docker-compose ps postgres

# Check postgres logs
docker-compose logs postgres

# Verify connection string
docker-compose exec backend env | grep DATABASE_URL
```

### Redis connection errors

```bash
# Check if redis is running
docker-compose ps redis

# Test connection
docker-compose exec redis redis-cli -a legally_ai_redis_dev PING
```

### Pydantic warning about "model_used"

**Fixed!** The warning:
```
Field "model_used" in AnalysisResponse has conflict with protected namespace "model_"
```

Is fixed in `backend/main.py` by adding:
```python
model_config = ConfigDict(protected_namespaces=())
```

### Reset Everything

```bash
# Stop and remove everything (including volumes)
docker-compose down -v

# Start fresh
docker-compose up -d
```

## Production Deployment

For production (Fly.io), see `DEPLOYMENT_GUIDE.md`.

Key differences:
- Use production environment variables
- Enable health checks
- Set proper resource limits
- Use secrets management
- Enable monitoring (Sentry)

## Next Steps

1. ✅ Docker setup complete
2. Implement API endpoints (contracts, analyses)
3. Add authentication (FastAPI-Users)
4. Connect to LLM providers
5. Implement Celery tasks
6. Add frontend (Nuxt 3)

## Resources

- [Docker Compose Docs](https://docs.docker.com/compose/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [Celery Docs](https://docs.celeryproject.org/)

---

**Last Updated**: 2025-11-09
