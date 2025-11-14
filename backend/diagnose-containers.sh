#!/bin/bash
# Quick diagnostic script to check what's wrong

echo "🔍 Diagnosing Docker Compose Issues"
echo "===================================="
echo ""

echo "1️⃣ Container Status:"
echo "-------------------"
docker compose ps
echo ""

echo "2️⃣ API Container Logs (last 30 lines):"
echo "--------------------------------------"
docker compose logs --tail=30 api
echo ""

echo "3️⃣ Celery Worker Logs (last 30 lines):"
echo "---------------------------------------"
docker compose logs --tail=30 celery
echo ""

echo "4️⃣ PostgreSQL Logs (last 15 lines):"
echo "------------------------------------"
docker compose logs --tail=15 postgres
echo ""

echo "5️⃣ Redis Logs (last 15 lines):"
echo "-------------------------------"
docker compose logs --tail=15 redis
echo ""

echo "===================================="
echo "💡 Common Issues:"
echo "===================================="
echo ""
echo "If you see 'ModuleNotFoundError':"
echo "  → Run: docker compose build --no-cache"
echo ""
echo "If you see 'Connection refused' to database:"
echo "  → Database might still be starting"
echo "  → Wait 30 seconds and try again"
echo ""
echo "If you see 'Address already in use':"
echo "  → Port conflict with another service"
echo "  → Stop the conflicting service"
echo ""
echo "If containers keep restarting:"
echo "  → Check logs above for the error"
echo "  → Usually a configuration or dependency issue"
echo ""
