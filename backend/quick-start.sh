#!/bin/bash

# Quick Start Script for Legally AI
# Gets everything running in one command

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Legally AI - Quick Start"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${NC}"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed${NC}"
    echo "Please install Docker Desktop:"
    echo "  macOS/Windows: https://www.docker.com/products/docker-desktop/"
    echo "  Linux: https://docs.docker.com/engine/install/"
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker is installed${NC}"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  No .env file found${NC}"
    echo "Creating from .env.example..."

    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo -e "${GREEN}✅ Created .env file${NC}"
        echo -e "${YELLOW}⚠️  Please edit .env with your API keys before continuing${NC}"
        echo ""
        echo "Required variables:"
        echo "  - SECRET_KEY (generate a random string)"
        echo "  - GROQ_API_KEY (get from https://console.groq.com/)"
        echo ""
        echo "Optional but recommended:"
        echo "  - SENDGRID_API_KEY (for email functionality)"
        echo ""
        echo "Press Enter when you've configured .env..."
        read
    else
        echo -e "${RED}❌ .env.example not found${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}✅ .env file exists${NC}"

# Check if containers are already running
if docker-compose ps | grep -q "Up"; then
    echo -e "${YELLOW}⚠️  Services are already running${NC}"
    echo "Do you want to restart them? (y/N)"
    read -r restart

    if [[ $restart == "y" || $restart == "Y" ]]; then
        echo "Stopping services..."
        docker-compose down
    else
        echo "Keeping services running"
        echo ""
        echo -e "${GREEN}Backend API:${NC} http://localhost:8000"
        echo -e "${GREEN}API Docs:${NC} http://localhost:8000/docs"
        echo ""
        echo "To view logs: docker-compose logs -f"
        echo "To stop: docker-compose down"
        exit 0
    fi
fi

# Start services
echo ""
echo -e "${BLUE}Starting services...${NC}"
echo "This may take a few minutes on first run (downloading images)"
echo ""

# Use docker-compose or docker compose depending on what's available
if command -v docker-compose &> /dev/null; then
    docker-compose up -d
else
    docker compose up -d
fi

echo ""
echo -e "${BLUE}Waiting for services to be ready...${NC}"

# Wait for backend to be ready
MAX_ATTEMPTS=30
ATTEMPT=0

while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Backend is ready!${NC}"
        break
    fi

    ATTEMPT=$((ATTEMPT + 1))
    echo "Waiting for backend... ($ATTEMPT/$MAX_ATTEMPTS)"
    sleep 2
done

if [ $ATTEMPT -eq $MAX_ATTEMPTS ]; then
    echo -e "${RED}❌ Backend failed to start${NC}"
    echo "Check logs with: docker-compose logs backend"
    exit 1
fi

# Run database migrations
echo ""
echo -e "${BLUE}Running database migrations...${NC}"

if command -v docker-compose &> /dev/null; then
    docker-compose exec -T backend alembic upgrade head
else
    docker compose exec -T backend alembic upgrade head
fi

echo -e "${GREEN}✅ Migrations complete${NC}"

# Success message
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}  🎉 Legally AI is running!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "Services:"
echo -e "  ${BLUE}Backend API:${NC}     http://localhost:8000"
echo -e "  ${BLUE}API Docs:${NC}        http://localhost:8000/docs"
echo -e "  ${BLUE}Health Check:${NC}    http://localhost:8000/health"
echo ""
echo "Useful commands:"
echo "  View logs:         docker-compose logs -f"
echo "  Stop services:     docker-compose down"
echo "  Restart services:  docker-compose restart"
echo "  Run tests:         ./test_integration.sh"
echo ""
echo "Next steps:"
echo "  1. Open http://localhost:8000/docs in your browser"
echo "  2. Try the API endpoints"
echo "  3. Run integration tests: ./test_integration.sh"
echo "  4. Start frontend: cd ../frontend && npm run dev"
echo ""
