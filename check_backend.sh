#!/bin/bash

echo "=== Backend Diagnostic Script ==="
echo ""

# Check if containers are running
echo "1. Checking Docker containers status..."
docker compose ps
echo ""

# Check API container logs
echo "2. Checking API container logs (last 30 lines)..."
docker compose logs api --tail 30
echo ""

# Check if backend is responding
echo "3. Testing backend health endpoint..."
curl -v http://localhost:8000/health 2>&1 | head -20
echo ""

# Check if register endpoint exists
echo "4. Testing auth register endpoint..."
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123456"}' \
  -v 2>&1 | head -30
echo ""

echo "=== Diagnostic complete ==="
