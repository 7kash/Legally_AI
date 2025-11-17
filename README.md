# Legally AI

> AI-powered multilingual contract analysis platform

**Legally AI** helps users understand complex legal contracts by providing automated analysis, risk assessment, and actionable insights in simple language.

---

## 🎯 What Is This?

Legally AI is a full-stack web application that:
- Accepts contract uploads (PDF, DOCX)
- Extracts and analyzes contract text using AI
- Identifies obligations, rights, risks, and key terms
- Provides simplified explanations ("Explain Like I'm 5" mode)
- Supports multiple languages (English, Russian, Serbian, French)
- Offers bilingual quote extraction from original contracts

---

## 🏗️ Architecture

**Frontend**: Nuxt 3 (Vue 3 + TypeScript)
**Backend**: FastAPI (Python 3.11+)
**Database**: PostgreSQL
**Queue**: Redis + Celery
**AI**: GROQ API (Llama 3.3-70B)

```
┌──────────────┐
│   Frontend   │  Nuxt 3 SSR
│ (Port 3000)  │  + Tailwind CSS
└──────┬───────┘
       │
       │ HTTP/SSE
       ▼
┌──────────────┐
│   Backend    │  FastAPI
│ (Port 8000)  │  + JWT Auth
└──────┬───────┘
       │
       ├──►  PostgreSQL (Database)
       ├──►  Redis (Queue)
       ├──►  Celery (Workers)
       └──►  GROQ API (LLM)
```

---

## 📁 Project Structure

```
Legally_AI/
├── frontend/                # Nuxt 3 frontend application
│   ├── pages/              # File-based routing
│   ├── components/         # Vue components
│   │   └── analysis/       # Analysis result widgets
│   ├── stores/             # Pinia state management
│   ├── layouts/            # Page layouts
│   └── public/             # Static assets
│
├── backend/                # FastAPI backend application
│   ├── app/
│   │   ├── api/           # API endpoints
│   │   ├── models/        # SQLAlchemy models
│   │   ├── services/      # Business logic
│   │   │   ├── document_parser.py
│   │   │   ├── llm_analysis/    # AI analysis modules
│   │   │   ├── eli5_service.py  # Text simplification
│   │   │   └── deadline_service.py
│   │   ├── tasks/         # Celery background tasks
│   │   └── migrations/    # Database migrations
│   ├── docker-compose.yml
│   └── requirements.txt
│
└── prototype/              # Original Gradio prototype (reference)
```

---

## 🚀 Quick Start

### Prerequisites

- **Docker & Docker Compose** (recommended)
- OR: Node.js 18+, Python 3.11+, PostgreSQL 15+, Redis 7+

### 1. Clone the Repository

```bash
git clone https://github.com/7kash/Legally_AI.git
cd Legally_AI
```

### 2. Backend Setup

```bash
cd backend

# Create environment file
cp .env.example .env

# Add your GROQ API key to .env
echo "GROQ_API_KEY=your_key_here" >> .env

# Start all services with Docker Compose
docker compose up -d --build

# Check logs
docker compose logs -f
```

**Services will start on:**
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- PostgreSQL: localhost:5432
- Redis: localhost:6379

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

**Frontend will be available at:** http://localhost:3000

### 4. Test the Application

1. Register a new account at http://localhost:3000/register
2. Upload a contract (PDF or DOCX)
3. Watch real-time analysis progress
4. View results with AI-powered insights

---

## ✨ Key Features

### Core Features

- **Contract Upload**: PDF and DOCX support with validation
- **Real-time Analysis**: Server-Sent Events (SSE) for live progress updates
- **AI-Powered Analysis**:
  - Agreement type identification
  - Parties extraction
  - Obligations and rights analysis
  - Risk assessment with severity levels
  - Payment terms extraction
  - Key dates and deadlines
  - Suggested changes and risk mitigations

### Advanced Features

- **"Explain Like I'm 5" Mode** 🎓
  - Simplifies legal jargon into everyday language
  - One-click toggle between legal and simple modes
  - Pre-generated during analysis for instant switching

- **Bilingual Quote Extraction** 🌍
  - Extracts original contract quotes
  - Provides translations in user's preferred language
  - Side-by-side display with visual indicators

- **Deadline Radar** 📅
  - Automatic deadline extraction
  - Calendar export (.ics format)
  - Integration with Google Calendar, Apple Calendar, Outlook

- **Feedback System** 👍👎
  - Thumbs up/down on analysis items
  - Helps improve AI accuracy over time
  - Confidence calibration

- **GDPR Compliance** 🔒
  - PII redaction before sending to LLM
  - Data export (JSON)
  - Account deletion (Right to Erasure)
  - Audit logging

### User Experience

- **Multilingual Support**: English, Russian, Serbian, French
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Dark Mode Ready**: System preference detection
- **Professional Exports**: PDF, DOCX, Lawyer Handoff Pack

---

## 🔧 Development

### Backend Development

```bash
cd backend

# Run API server (with hot reload)
uvicorn app.main:app --reload --port 8000

# Run Celery worker (separate terminal)
celery -A app.celery_app worker --loglevel=info

# Run database migrations
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "description"
```

### Frontend Development

```bash
cd frontend

# Development server (hot reload)
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Type checking
npm run typecheck

# Linting
npm run lint
```

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm run test
```

---

## 📊 API Endpoints

### Authentication
```
POST   /api/v1/auth/register
POST   /api/v1/auth/login
GET    /api/v1/auth/me
POST   /api/v1/auth/logout
```

### Contracts
```
POST   /api/v1/contracts/upload
GET    /api/v1/contracts
GET    /api/v1/contracts/{id}
DELETE /api/v1/contracts/{id}
```

### Analysis
```
POST   /api/v1/analyses
GET    /api/v1/analyses/{id}
GET    /api/v1/analyses/{id}/stream     # SSE
POST   /api/v1/analyses/{id}/feedback
```

### Advanced Features
```
GET    /api/v1/deadlines
GET    /api/v1/deadlines/{id}/export    # .ics file
POST   /api/v1/feedback
GET    /api/v1/account/export            # GDPR data export
DELETE /api/v1/account                   # GDPR account deletion
```

Full API documentation: http://localhost:8000/docs

---

## 🔑 Environment Variables

### Backend (.env)

```bash
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/legally_ai

# Redis
REDIS_URL=redis://localhost:6379/0

# LLM API
GROQ_API_KEY=your_groq_api_key_here

# Security
SECRET_KEY=your-secret-key-here
JWT_SECRET=your-jwt-secret-here

# Application
APP_NAME="Legally AI"
DEBUG=True
CORS_ORIGINS=["http://localhost:3000"]

# File Upload
UPLOAD_DIR=/app/uploads
MAX_FILE_SIZE_MB=10
```

### Frontend (.env)

```bash
# API Base URL
NUXT_PUBLIC_API_BASE=http://localhost:8000/api/v1
```

---

## 🛠️ Tech Stack Details

### Frontend
- **Framework**: Nuxt 3.8+ (Vue 3 + TypeScript)
- **Styling**: Tailwind CSS 3.x
- **State Management**: Pinia
- **HTTP Client**: $fetch (Nuxt built-in)
- **Forms**: Native Vue Composition API
- **Icons**: Heroicons

### Backend
- **Framework**: FastAPI 0.110+
- **Language**: Python 3.11+
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic
- **Validation**: Pydantic v2
- **Auth**: JWT (python-jose)
- **Task Queue**: Celery 5.x + Redis
- **Document Parsing**: PyPDF2, python-docx, pdfplumber
- **AI**: GROQ API (Llama 3.3-70B)

### Infrastructure
- **Database**: PostgreSQL 15+
- **Cache/Queue**: Redis 7+
- **Container**: Docker + Docker Compose
- **Deployment**: Fly.io (backend), Vercel (frontend)

---

## 📝 Recent Updates

### Latest Changes (Current Branch)
- ✅ Fixed 404 error on contracts list endpoint
- ✅ Improved ELI5 prompt to eliminate meta-commentary
- ✅ Added proper line breaks in ELI5 simplified text
- ✅ Fixed CORS issues with trailing slash redirects
- ✅ Enhanced history page with date filters
- ✅ Improved error handling for new users

### Recent Features
- ✅ ELI5 "Explain Like I'm 5" simplification mode
- ✅ Deadline Radar system with calendar export
- ✅ Feedback system (thumbs up/down)
- ✅ Bilingual quote extraction
- ✅ GDPR compliance features
- ✅ Quality scoring and confidence levels
- ✅ Multi-language support

See [CURRENT_STATUS.md](./CURRENT_STATUS.md) for detailed status.

---

## 🐛 Troubleshooting

### Backend Issues

**Services won't start:**
```bash
cd backend
docker compose down -v  # Remove volumes
docker compose up -d --build
```

**Database connection errors:**
- Check PostgreSQL is running: `docker compose ps`
- Verify DATABASE_URL in .env
- Check logs: `docker compose logs postgres`

**Celery tasks not processing:**
- Check Redis is running: `docker compose ps`
- Verify REDIS_URL in .env
- Check Celery logs: `docker compose logs celery`

### Frontend Issues

**API connection errors:**
- Verify backend is running on port 8000
- Check NUXT_PUBLIC_API_BASE in .env
- Check browser console for CORS errors

**Build errors:**
```bash
rm -rf node_modules .nuxt
npm install
npm run dev
```

See [backend/TROUBLESHOOTING.md](./backend/TROUBLESHOOTING.md) for more details.

---

## 📚 Documentation

- [Architecture](./architecture.md) - System architecture and design decisions
- [Current Status](./CURRENT_STATUS.md) - Latest development status
- [Features Implemented](./FEATURES_IMPLEMENTED.md) - Complete feature list
- [Backend README](./backend/README.md) - Backend-specific documentation
- [Frontend README](./frontend/README.md) - Frontend-specific documentation
- [GDPR Compliance](./GDPR_COMPLIANCE.md) - Privacy and compliance details
- [Deployment Guide](./DEPLOYMENT_GUIDE.md) - Production deployment instructions

---

## 🔐 Security

- **Authentication**: JWT-based with httpOnly cookies
- **Password Hashing**: bcrypt (cost factor: 12)
- **PII Redaction**: Automatic before sending to LLM
- **Input Validation**: Pydantic schemas
- **File Upload**: Size limits, type validation
- **Rate Limiting**: 100 requests/minute per IP
- **CORS**: Whitelist frontend domain only
- **Audit Logging**: All critical operations logged

---

## 🧪 Testing

The application includes automated testing:

```bash
# Backend API tests
cd backend
pytest tests/ -v

# Frontend component tests
cd frontend
npm run test

# End-to-end tests
npm run test:e2e
```

---

## 🚀 Deployment

### Production Deployment

**Backend (Fly.io):**
```bash
cd backend
fly deploy
```

**Frontend (Vercel):**
```bash
cd frontend
vercel --prod
```

See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) for detailed instructions.

---

## 🤝 Contributing

This is a proprietary project. For internal contributors:

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Run tests: `pytest` (backend) and `npm run test` (frontend)
4. Commit with clear messages
5. Push and create a Pull Request

---

## 📄 License

Proprietary - All rights reserved.

---

## 🙏 Acknowledgments

- **GROQ** - Fast, affordable LLM inference
- **FastAPI** - Modern Python web framework
- **Nuxt** - Vue.js meta-framework
- **Tailwind CSS** - Utility-first CSS framework

---

## 📞 Support

For issues or questions:
- Check [TROUBLESHOOTING.md](./backend/TROUBLESHOOTING.md)
- Review [API Documentation](http://localhost:8000/docs)
- Contact the development team

---

**Built with ❤️ for simplifying legal complexity**
