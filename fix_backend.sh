#!/bin/bash

echo "=== Fixing Backend Setup ==="
echo ""

# Pull latest code
echo "1. Pulling latest code from branch..."
git pull origin claude/push-celery-duplicate-fix-0128AnbZuzaJLX1Qa3QUHqrA
echo ""

# Stop all containers
echo "2. Stopping all containers..."
docker compose down
echo ""

# Remove volumes to recreate database with User table
echo "3. Removing volumes to recreate database..."
docker compose down -v
echo ""

# Rebuild backend container with new dependencies
echo "4. Rebuilding backend API container..."
docker compose build --no-cache api
echo ""

# Start all services
echo "5. Starting all services..."
docker compose up -d
echo ""

# Wait for services to start
echo "6. Waiting 10 seconds for services to initialize..."
sleep 10
echo ""

# Show container status
echo "7. Container status:"
docker compose ps
echo ""

# Show API logs
echo "8. API container logs (last 20 lines):"
docker compose logs api --tail 20
echo ""

# Test health endpoint
echo "9. Testing backend health endpoint..."
curl -s http://localhost:8000/health | python3 -m json.tool || echo "Backend not responding yet"
echo ""

echo "=== Setup complete! ==="
echo ""
echo "Backend should be running at: http://localhost:8000"
echo "API docs at: http://localhost:8000/docs"
echo ""
echo "If you see errors, check the logs with:"
echo "  docker compose logs api --tail 50"
