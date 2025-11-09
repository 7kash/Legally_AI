# Legally AI Backend

FastAPI backend for the Legally AI contract analysis platform.

## Architecture

- **Framework**: FastAPI 0.110+
- **Database**: PostgreSQL 16
- **ORM**: SQLAlchemy 2.0
- **Auth**: FastAPI-Users + JWT
- **Tasks**: Celery + Redis
- **LLM**: Groq API (with DeepSeek fallback)

## Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- PostgreSQL 16 (or use Docker)
- Redis 7 (or use Docker)

### Development Setup

1. **Clone and navigate**:
   ```bash
   cd backend
   ```

2. **Create environment file**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Start services with Docker Compose**:
   ```bash
   docker-compose up -d
   ```

   This starts:
   - PostgreSQL on port 5432
   - Redis on port 6379
   - Backend API on port 8000
   - Celery worker

4. **Run migrations** (first time only):
   ```bash
   docker-compose exec backend alembic upgrade head
   ```

5. **Access the API**:
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs
   - Health: http://localhost:8000/health

### Local Development (without Docker)

1. **Install dependencies**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Start PostgreSQL and Redis** (locally or via Docker):
   ```bash
   # Option 1: Docker containers only for DB/Redis
   docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=password postgres:16-alpine
   docker run -d -p 6379:6379 redis:7-alpine
   ```

3. **Run migrations**:
   ```bash
   alembic upgrade head
   ```

4. **Start the backend**:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

5. **Start Celery worker** (in another terminal):
   ```bash
   celery -A app.tasks.celery_app worker --loglevel=info
   ```

## Project Structure

```
backend/
├── app/
│   ├── api/              # API endpoints
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   ├── services/         # Business logic (LLM, parsers, etc.)
│   ├── tasks/            # Celery tasks
│   ├── db/               # Database config
│   ├── core/             # Core utilities (auth, security)
│   ├── utils/            # Helper functions
│   ├── config.py         # Settings
│   └── main.py           # FastAPI app
├── alembic/              # Database migrations
├── prompts/              # LLM prompts
├── tests/                # Unit and integration tests
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT token
- `POST /api/auth/logout` - Logout
- `GET /api/auth/me` - Get current user

### Contracts
- `POST /api/contracts/upload` - Upload contract
- `GET /api/contracts` - List user's contracts
- `GET /api/contracts/{id}` - Get contract details
- `DELETE /api/contracts/{id}` - Delete contract
- `POST /api/contracts/{id}/analyze` - Start analysis

### Analyses
- `GET /api/analyses/{id}` - Get analysis results
- `GET /api/analyses/{id}/stream` - SSE stream for progress
- `POST /api/analyses/{id}/feedback` - Submit feedback

See `/docs` for full API documentation.

## Database Migrations

### Create a new migration:
```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply migrations:
```bash
alembic upgrade head
```

### Rollback migration:
```bash
alembic downgrade -1
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_api/test_auth.py
```

## Environment Variables

See `.env.example` for all available configuration options.

### Required:
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - JWT signing key (generate with `openssl rand -hex 32`)
- `GROQ_API_KEY` or `DEEPSEEK_API_KEY` - LLM provider API key

### Optional:
- `REDIS_URL` - Redis connection (default: localhost)
- `STRIPE_API_KEY` - For payments
- `SENDGRID_API_KEY` - For emails
- `SENTRY_DSN` - For error tracking

## Deployment

### Fly.io (Recommended)

1. **Install Fly CLI**:
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login**:
   ```bash
   fly auth login
   ```

3. **Create app**:
   ```bash
   fly launch
   ```

4. **Set secrets**:
   ```bash
   fly secrets set SECRET_KEY=your-secret-key
   fly secrets set GROQ_API_KEY=your-groq-key
   fly secrets set DATABASE_URL=your-database-url
   ```

5. **Deploy**:
   ```bash
   fly deploy
   ```

## Monitoring

- **Health check**: `GET /health`
- **Logs**: `docker-compose logs -f backend`
- **Fly logs**: `fly logs`
- **Sentry**: Automatic error tracking if `SENTRY_DSN` is set

## Development

### Code Style

```bash
# Format code
black app/

# Lint
ruff check app/

# Type check
mypy app/
```

### Adding New Endpoints

1. Create schema in `app/schemas/`
2. Create model in `app/models/` (if needed)
3. Create endpoint in `app/api/`
4. Register router in `app/main.py`
5. Write tests in `tests/`

## Troubleshooting

### Database connection issues
```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# Check logs
docker-compose logs postgres
```

### Redis connection issues
```bash
# Check if Redis is running
docker-compose ps redis

# Test connection
docker-compose exec redis redis-cli ping
```

### Celery tasks not running
```bash
# Check worker status
docker-compose logs celery_worker

# Restart worker
docker-compose restart celery_worker
```

## License

MIT

## Support

For issues or questions:
- GitHub Issues: https://github.com/7kash/Legally_AI/issues
- Email: support@legally-ai.com
