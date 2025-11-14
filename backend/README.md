# Legally AI Backend

Production-grade backend for the Legally AI contract analysis platform.

## Architecture

- **FastAPI**: RESTful API and Server-Sent Events (SSE)
- **Celery**: Asynchronous task processing
- **PostgreSQL**: Persistent data storage
- **Redis**: Message broker and caching

## Bug Fix: Duplicate Analysis Records

### The Problem

Previously, the API endpoint and Celery task were creating two separate `Analysis` records with different UUIDs:

1. **API Endpoint**: Created `Analysis` with UUID `A` and set status to "queued"
2. **Celery Task**: Created NEW `Analysis` with UUID `B` and processed it
3. **SSE Stream**: Polled for events with UUID `A`, but events were created for UUID `B`
4. **Result**: Frontend stuck in "queued" state forever

### The Solution

**API Endpoint (`backend/app/api/analyses.py:83-86`)**:
```python
# ✅ Pass analysis_id instead of contract_id
analyze_contract_task.delay(
    analysis_id=str(analysis.id),  # ✅ Fixed
    output_language=data.output_language
)
```

**Celery Task (`backend/app/tasks/analyze_contract.py:60-95`)**:
```python
@celery_app.task(bind=True, name="analyze_contract")
def analyze_contract_task(
    self,
    analysis_id: str,  # ✅ Receives analysis_id
    output_language: str = "english"
):
    # ✅ Get existing analysis record (don't create new one)
    analysis = db.query(Analysis).filter(Analysis.id == analysis_uuid).first()
    if not analysis:
        raise ValueError(f"Analysis {analysis_id} not found")

    # ✅ Update status (don't create new record)
    analysis.status = "running"
    analysis.started_at = datetime.utcnow()
    db.commit()
```

### Flow Diagram

**Before Fix (Bug)**:
```
┌─────────┐         ┌───────────┐         ┌─────────┐
│  API    │ ID: A   │  Celery   │ ID: B   │   SSE   │
│ Creates ├────────>│  Creates  ├────────>│ Polls A │
│ Analysis│         │ Analysis  │ Events  │         │
│   (A)   │         │   (B)     │ for B   │ STUCK!  │
└─────────┘         └───────────┘         └─────────┘
```

**After Fix (Working)**:
```
┌─────────┐         ┌───────────┐         ┌─────────┐
│  API    │ ID: A   │  Celery   │         │   SSE   │
│ Creates ├────────>│  Updates  ├────────>│ Polls A │
│ Analysis│         │ Analysis  │ Events  │ ✓ Works │
│   (A)   │         │   (A)     │ for A   │         │
└─────────┘         └───────────┘         └─────────┘
```

## Installation

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Set up environment**:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Initialize database**:
```bash
# Create database
createdb legally_ai

# Run migrations (or init_db on startup)
python -c "from app.database import init_db; init_db()"
```

4. **Start Redis** (if not running):
```bash
redis-server
```

## Running

### Development

**Terminal 1 - API Server**:
```bash
python -m app.main
# or
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Celery Worker**:
```bash
celery -A app.celery_app worker --loglevel=info
```

**Terminal 3 - Celery Beat (optional, for scheduled tasks)**:
```bash
celery -A app.celery_app beat --loglevel=info
```

### Production (Fly.io)

See `../DEPLOYMENT_GUIDE.md` for production deployment instructions.

## API Endpoints

### Create Analysis
```http
POST /api/v1/analyses
Content-Type: application/json

{
  "contract_id": "123e4567-e89b-12d3-a456-426614174000",
  "output_language": "english"
}
```

### Get Analysis
```http
GET /api/v1/analyses/{analysis_id}
```

### Stream Analysis Events (SSE)
```http
GET /api/v1/analyses/{analysis_id}/stream
```

### Delete Analysis
```http
DELETE /api/v1/analyses/{analysis_id}
```

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app
│   ├── config.py            # Configuration
│   ├── database.py          # DB connection
│   ├── celery_app.py        # Celery config
│   ├── models/
│   │   ├── __init__.py
│   │   ├── contract.py
│   │   └── analysis.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── analyses.py      # ✅ Bug fix applied
│   └── tasks/
│       ├── __init__.py
│       └── analyze_contract.py  # ✅ Bug fix applied
├── requirements.txt
├── .env.example
└── README.md
```

## Testing

```bash
# Test API
curl http://localhost:8000/health

# Test creating analysis (requires database setup)
curl -X POST http://localhost:8000/api/v1/analyses \
  -H "Content-Type: application/json" \
  -d '{"contract_id": "uuid-here", "output_language": "english"}'

# Stream events
curl http://localhost:8000/api/v1/analyses/{analysis_id}/stream
```

## Environment Variables

See `.env.example` for all available configuration options.

## License

Proprietary - All rights reserved.
