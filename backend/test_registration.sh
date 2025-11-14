#!/bin/bash

echo "=== Testing Registration Endpoint ==="
echo ""

echo "Testing registration with curl..."
RESPONSE=$(curl -s -w "\nHTTP_CODE:%{http_code}" -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"testuser@example.com","password":"testpass123"}' 2>&1)

HTTP_CODE=$(echo "$RESPONSE" | grep "HTTP_CODE" | cut -d: -f2)
BODY=$(echo "$RESPONSE" | grep -v "HTTP_CODE")

echo "HTTP Status Code: $HTTP_CODE"
echo ""
echo "Response Body:"
echo "$BODY" | python3 -m json.tool 2>/dev/null || echo "$BODY"
echo ""

if [ "$HTTP_CODE" = "201" ] || [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Registration successful!"
elif [ "$HTTP_CODE" = "400" ]; then
    echo "⚠️  Bad request (probably email already exists)"
elif [ "$HTTP_CODE" = "500" ]; then
    echo "❌ Server error! Check backend logs:"
    echo "   docker compose logs api --tail 50"
else
    echo "❓ Unexpected response code: $HTTP_CODE"
fi
