#!/bin/bash

echo "=== Backend Rebuild Script ==="
echo "This script must be run from the backend/ directory"
echo ""

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Error: docker-compose.yml not found"
    echo "Please run this from the backend/ directory:"
    echo "  cd /Users/ekaterinamatyushina/Legally_AI/backend"
    echo "  ./rebuild_backend.sh"
    exit 1
fi

echo "✅ Found docker-compose.yml"
echo ""

# Stop all containers
echo "1. Stopping all containers..."
docker compose down
echo ""

# Remove volumes
echo "2. Removing volumes to recreate database..."
docker compose down -v
echo ""

# Rebuild
echo "3. Rebuilding API container (this may take 2-3 minutes)..."
docker compose build --no-cache api
echo ""

# Start services
echo "4. Starting all services..."
docker compose up -d
echo ""

# Wait for startup
echo "5. Waiting 15 seconds for services to start..."
sleep 15
echo ""

# Show status
echo "6. Container status:"
docker compose ps
echo ""

# Show logs
echo "7. API logs (last 20 lines):"
docker compose logs api --tail 20
echo ""

# Test health
echo "8. Testing health endpoint..."
HEALTH=$(curl -s http://localhost:8000/health 2>&1)
if [ $? -eq 0 ]; then
    echo "✅ Backend is responding!"
    echo "Response: $HEALTH"
else
    echo "❌ Backend not responding yet"
    echo "Check logs: docker compose logs api --tail 50"
fi
echo ""

echo "9. Testing API docs..."
echo "Visit http://localhost:8000/docs in your browser"
echo ""

echo "=== Rebuild Complete! ==="
echo ""
echo "If backend is running, try registration at:"
echo "  http://localhost:3000/register"
echo ""
echo "If still having issues, check:"
echo "  docker compose logs api --tail 100"
