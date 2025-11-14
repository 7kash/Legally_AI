#!/bin/bash
# Docker Compose Test Runner
# This script starts all services and runs the bug fix test

set -e

echo "========================================"
echo "  Legally AI - Docker Compose Test"
echo "========================================"
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ docker-compose not found${NC}"
    echo "Please install Docker Compose"
    exit 1
fi

echo "🐳 Starting Docker Compose services..."
echo ""

# Start services in background
docker-compose up -d postgres redis api celery

echo ""
echo "⏳ Waiting for services to be ready..."
echo ""

# Wait for postgres
echo -n "  Waiting for PostgreSQL... "
for i in {1..30}; do
    if docker-compose exec -T postgres pg_isready -U postgres &> /dev/null; then
        echo -e "${GREEN}✅${NC}"
        break
    fi
    sleep 1
done

# Wait for redis
echo -n "  Waiting for Redis... "
for i in {1..30}; do
    if docker-compose exec -T redis redis-cli ping &> /dev/null; then
        echo -e "${GREEN}✅${NC}"
        break
    fi
    sleep 1
done

# Wait for API
echo -n "  Waiting for API... "
for i in {1..30}; do
    if docker-compose exec -T api curl -s http://localhost:8000/health &> /dev/null; then
        echo -e "${GREEN}✅${NC}"
        break
    fi
    sleep 1
done

# Wait for Celery
echo -n "  Waiting for Celery worker... "
sleep 5  # Give Celery time to start
if docker-compose ps celery | grep -q "Up"; then
    echo -e "${GREEN}✅${NC}"
else
    echo -e "${RED}❌${NC}"
    echo ""
    echo -e "${YELLOW}Warning: Celery worker may not be running properly${NC}"
    echo "Check logs with: docker-compose logs celery"
fi

echo ""
echo "========================================"
echo "  🧪 Running Bug Fix Test"
echo "========================================"
echo ""

# Run the test
docker-compose exec -T api python tests/docker_test.py

TEST_RESULT=$?

echo ""
echo "========================================"

if [ $TEST_RESULT -eq 0 ]; then
    echo -e "  ${GREEN}✅ TEST PASSED${NC}"
    echo "========================================"
    echo ""
    echo "The duplicate analysis bug is FIXED! 🎉"
    echo ""
    echo "To view logs:"
    echo "  docker-compose logs api"
    echo "  docker-compose logs celery"
    echo ""
    echo "To stop services:"
    echo "  docker-compose down"
else
    echo -e "  ${RED}❌ TEST FAILED${NC}"
    echo "========================================"
    echo ""
    echo "Troubleshooting:"
    echo ""
    echo "1. Check Celery worker logs:"
    echo "   docker-compose logs celery"
    echo ""
    echo "2. Check API logs:"
    echo "   docker-compose logs api"
    echo ""
    echo "3. Check database state:"
    echo "   docker-compose exec api python scripts/diagnose.py"
    echo ""
    echo "4. View all logs:"
    echo "   docker-compose logs"
    echo ""
    echo "To stop and clean up:"
    echo "  docker-compose down -v"
fi

echo ""

exit $TEST_RESULT
