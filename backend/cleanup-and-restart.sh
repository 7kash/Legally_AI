#!/bin/bash
# Clean up old containers and start fresh with the bug-fixed backend

set -e

echo "🧹 Cleaning up old Docker containers..."
echo ""

# Stop and remove old containers
echo "Stopping old containers..."
docker stop legally_ai_backend legally_ai_worker 2>/dev/null || true
docker rm legally_ai_backend legally_ai_worker 2>/dev/null || true

echo "✅ Old containers removed"
echo ""

# Navigate to backend directory
cd "$(dirname "$0")"

echo "🐳 Starting new Docker Compose setup..."
echo ""

# Stop any existing docker-compose services
docker compose down -v 2>/dev/null || true

# Start fresh
docker compose up -d

echo ""
echo "⏳ Waiting for services to start..."
sleep 10

echo ""
echo "📊 Service Status:"
docker compose ps

echo ""
echo "✅ New setup is running!"
echo ""
echo "Now run the test:"
echo "  ./test-docker.sh"
echo ""
