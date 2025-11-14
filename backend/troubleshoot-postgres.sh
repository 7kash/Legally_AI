#!/bin/bash
# PostgreSQL Container Troubleshooting Script

echo "🔧 Troubleshooting PostgreSQL Container"
echo "========================================"
echo ""

# Check if postgres container exists
echo "1. Checking for existing containers..."
docker ps -a | grep postgres

echo ""
echo "2. Checking PostgreSQL logs..."
docker compose logs postgres

echo ""
echo "3. Checking if port 5432 is in use..."
lsof -i :5432 || netstat -tuln | grep 5432 || ss -tuln | grep 5432

echo ""
echo "4. Checking Docker volumes..."
docker volume ls | grep legally

echo ""
echo "========================================"
echo "Common Fixes:"
echo "========================================"
echo ""
echo "Fix 1: Port 5432 is already in use"
echo "  → Stop local PostgreSQL: sudo systemctl stop postgresql"
echo "  → Or change port in docker-compose.yml"
echo ""
echo "Fix 2: Corrupted volume data"
echo "  → docker compose down -v"
echo "  → docker compose up -d"
echo ""
echo "Fix 3: Permission issues"
echo "  → docker compose down"
echo "  → docker volume rm legally_ai_postgres_data"
echo "  → docker compose up -d"
echo ""
echo "Fix 4: Previous container conflicts"
echo "  → docker rm -f legally-ai-db"
echo "  → docker compose up -d"
echo ""
