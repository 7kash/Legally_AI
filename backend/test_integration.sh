#!/bin/bash

# Integration Testing Script for Legally AI
# This script tests all API endpoints systematically

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
API_BASE="http://localhost:8000/api"
TEST_EMAIL="test_$(date +%s)@example.com"
TEST_PASSWORD="TestPassword123!"

# Variables to store between tests
TOKEN=""
CONTRACT_ID=""
ANALYSIS_ID=""

echo -e "${BLUE}==================================${NC}"
echo -e "${BLUE}Legally AI Integration Testing${NC}"
echo -e "${BLUE}==================================${NC}"
echo ""

# Helper functions
pass() {
    echo -e "${GREEN}✅ PASS${NC}: $1"
}

fail() {
    echo -e "${RED}❌ FAIL${NC}: $1"
    exit 1
}

info() {
    echo -e "${YELLOW}ℹ️  INFO${NC}: $1"
}

test_header() {
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}Test: $1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

# Test 1: Health Check
test_header "Health Check"
RESPONSE=$(curl -s $API_BASE/../health)
STATUS=$(echo "$RESPONSE" | jq -r '.status' 2>/dev/null)

if [ "$STATUS" == "healthy" ]; then
    pass "API is healthy"
else
    fail "API health check failed. Response: $RESPONSE"
fi

# Test 2: User Registration
test_header "User Registration"
info "Registering user: $TEST_EMAIL"

RESPONSE=$(curl -s -X POST $API_BASE/auth/register \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"$TEST_EMAIL\",\"password\":\"$TEST_PASSWORD\"}")

TOKEN=$(echo "$RESPONSE" | jq -r '.access_token' 2>/dev/null)
USER_ID=$(echo "$RESPONSE" | jq -r '.user.id' 2>/dev/null)

if [ "$TOKEN" != "null" ] && [ -n "$TOKEN" ]; then
    pass "User registered successfully"
    info "User ID: $USER_ID"
    info "Token: ${TOKEN:0:20}..."
else
    fail "User registration failed. Response: $RESPONSE"
fi

# Test 3: Login
test_header "User Login"
info "Logging in as: $TEST_EMAIL"

RESPONSE=$(curl -s -X POST $API_BASE/auth/login \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"$TEST_EMAIL\",\"password\":\"$TEST_PASSWORD\"}")

LOGIN_TOKEN=$(echo "$RESPONSE" | jq -r '.access_token' 2>/dev/null)

if [ "$LOGIN_TOKEN" != "null" ] && [ -n "$LOGIN_TOKEN" ]; then
    pass "Login successful"
    TOKEN=$LOGIN_TOKEN  # Use new token
else
    fail "Login failed. Response: $RESPONSE"
fi

# Test 4: Get User Profile
test_header "Get User Profile"

RESPONSE=$(curl -s $API_BASE/auth/me \
    -H "Authorization: Bearer $TOKEN")

EMAIL=$(echo "$RESPONSE" | jq -r '.email' 2>/dev/null)
TIER=$(echo "$RESPONSE" | jq -r '.tier' 2>/dev/null)
REMAINING=$(echo "$RESPONSE" | jq -r '.analyses_remaining' 2>/dev/null)

if [ "$EMAIL" == "$TEST_EMAIL" ]; then
    pass "Profile retrieved successfully"
    info "Tier: $TIER"
    info "Analyses Remaining: $REMAINING"
else
    fail "Get profile failed. Response: $RESPONSE"
fi

# Test 5: Upload Contract
test_header "Contract Upload"

# Create a test file
echo "This is a test contract for integration testing." > /tmp/test_contract.txt

RESPONSE=$(curl -s -X POST $API_BASE/contracts/upload \
    -H "Authorization: Bearer $TOKEN" \
    -F "file=@/tmp/test_contract.txt")

CONTRACT_ID=$(echo "$RESPONSE" | jq -r '.contract_id' 2>/dev/null)
FILENAME=$(echo "$RESPONSE" | jq -r '.filename' 2>/dev/null)

if [ "$CONTRACT_ID" != "null" ] && [ -n "$CONTRACT_ID" ]; then
    pass "Contract uploaded successfully"
    info "Contract ID: $CONTRACT_ID"
    info "Filename: $FILENAME"
else
    fail "Contract upload failed. Response: $RESPONSE"
fi

# Clean up test file
rm /tmp/test_contract.txt

# Test 6: List Contracts
test_header "List Contracts"

RESPONSE=$(curl -s "$API_BASE/contracts?page=1&page_size=10" \
    -H "Authorization: Bearer $TOKEN")

TOTAL=$(echo "$RESPONSE" | jq -r '.total' 2>/dev/null)
CONTRACTS_COUNT=$(echo "$RESPONSE" | jq -r '.contracts | length' 2>/dev/null)

if [ "$TOTAL" -ge 1 ]; then
    pass "Contracts listed successfully"
    info "Total contracts: $TOTAL"
else
    fail "List contracts failed. Response: $RESPONSE"
fi

# Test 7: Get Contract Details
test_header "Get Contract Details"

RESPONSE=$(curl -s $API_BASE/contracts/$CONTRACT_ID \
    -H "Authorization: Bearer $TOKEN")

RETRIEVED_ID=$(echo "$RESPONSE" | jq -r '.id' 2>/dev/null)

if [ "$RETRIEVED_ID" == "$CONTRACT_ID" ]; then
    pass "Contract details retrieved successfully"
else
    fail "Get contract failed. Response: $RESPONSE"
fi

# Test 8: Create Analysis
test_header "Create Analysis"
info "Starting analysis for contract: $CONTRACT_ID"

RESPONSE=$(curl -s -X POST $API_BASE/analyses \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"contract_id\":\"$CONTRACT_ID\",\"output_language\":\"english\"}")

ANALYSIS_ID=$(echo "$RESPONSE" | jq -r '.id' 2>/dev/null)
STATUS=$(echo "$RESPONSE" | jq -r '.status' 2>/dev/null)

if [ "$ANALYSIS_ID" != "null" ] && [ -n "$ANALYSIS_ID" ]; then
    pass "Analysis created successfully"
    info "Analysis ID: $ANALYSIS_ID"
    info "Status: $STATUS"
else
    fail "Create analysis failed. Response: $RESPONSE"
fi

# Test 9: Get Analysis Status
test_header "Get Analysis Status"

RESPONSE=$(curl -s $API_BASE/analyses/$ANALYSIS_ID \
    -H "Authorization: Bearer $TOKEN")

STATUS=$(echo "$RESPONSE" | jq -r '.status' 2>/dev/null)

if [ "$STATUS" != "null" ] && [ -n "$STATUS" ]; then
    pass "Analysis status retrieved"
    info "Current status: $STATUS"
else
    fail "Get analysis failed. Response: $RESPONSE"
fi

# Test 10: Account Details
test_header "Get Account Details"

RESPONSE=$(curl -s $API_BASE/account \
    -H "Authorization: Bearer $TOKEN")

TOTAL_CONTRACTS=$(echo "$RESPONSE" | jq -r '.total_contracts' 2>/dev/null)
TOTAL_ANALYSES=$(echo "$RESPONSE" | jq -r '.total_analyses' 2>/dev/null)
TIER_LIMIT=$(echo "$RESPONSE" | jq -r '.tier_limit' 2>/dev/null)

if [ "$TOTAL_CONTRACTS" != "null" ]; then
    pass "Account details retrieved"
    info "Total contracts: $TOTAL_CONTRACTS"
    info "Total analyses: $TOTAL_ANALYSES"
    info "Tier limit: $TIER_LIMIT"
else
    fail "Get account failed. Response: $RESPONSE"
fi

# Test 11: Update Account Email
test_header "Update Account Email"
NEW_EMAIL="updated_$TEST_EMAIL"

RESPONSE=$(curl -s -X PATCH $API_BASE/account \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"$NEW_EMAIL\"}")

UPDATED_EMAIL=$(echo "$RESPONSE" | jq -r '.email' 2>/dev/null)

if [ "$UPDATED_EMAIL" == "$NEW_EMAIL" ]; then
    pass "Email updated successfully"
    info "New email: $UPDATED_EMAIL"
else
    fail "Update email failed. Response: $RESPONSE"
fi

# Test 12: GDPR Data Export
test_header "GDPR Data Export"

RESPONSE=$(curl -s $API_BASE/account/export \
    -H "Authorization: Bearer $TOKEN")

USER_DATA=$(echo "$RESPONSE" | jq -r '.user.email' 2>/dev/null)
CONTRACTS_DATA=$(echo "$RESPONSE" | jq -r '.contracts | length' 2>/dev/null)

if [ "$USER_DATA" != "null" ] && [ "$CONTRACTS_DATA" -ge 0 ]; then
    pass "GDPR data export successful"
    info "Exported user data"
    info "Exported $CONTRACTS_DATA contracts"
else
    fail "GDPR export failed. Response: $RESPONSE"
fi

# Test 13: Free Tier Limit Enforcement
test_header "Free Tier Limit Enforcement"
info "Testing 4th analysis (should fail)"

# Create 2 more contracts and analyses
for i in {2..3}; do
    # Upload contract
    echo "Test contract $i" > /tmp/test_contract_$i.txt
    UPLOAD=$(curl -s -X POST $API_BASE/contracts/upload \
        -H "Authorization: Bearer $TOKEN" \
        -F "file=@/tmp/test_contract_$i.txt")
    NEW_CONTRACT_ID=$(echo "$UPLOAD" | jq -r '.contract_id')

    # Create analysis
    curl -s -X POST $API_BASE/analyses \
        -H "Authorization: Bearer $TOKEN" \
        -H "Content-Type: application/json" \
        -d "{\"contract_id\":\"$NEW_CONTRACT_ID\",\"output_language\":\"english\"}" > /dev/null

    rm /tmp/test_contract_$i.txt
    sleep 1
done

# Try 4th analysis (should fail)
echo "Test contract 4" > /tmp/test_contract_4.txt
UPLOAD=$(curl -s -X POST $API_BASE/contracts/upload \
    -H "Authorization: Bearer $TOKEN" \
    -F "file=@/tmp/test_contract_4.txt")
FOURTH_CONTRACT_ID=$(echo "$UPLOAD" | jq -r '.contract_id')

RESPONSE=$(curl -s -X POST $API_BASE/analyses \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"contract_id\":\"$FOURTH_CONTRACT_ID\",\"output_language\":\"english\"}")

ERROR=$(echo "$RESPONSE" | jq -r '.detail' 2>/dev/null)

if [[ "$ERROR" == *"Free tier limit reached"* ]]; then
    pass "Free tier limit properly enforced"
    info "Error message: $ERROR"
else
    fail "Free tier limit NOT enforced. Response: $RESPONSE"
fi

rm /tmp/test_contract_4.txt

# Test 14: Unauthorized Access
test_header "Unauthorized Access Protection"
info "Testing endpoint without token"

RESPONSE=$(curl -s -w "\n%{http_code}" $API_BASE/auth/me)
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)

if [ "$HTTP_CODE" == "403" ] || [ "$HTTP_CODE" == "401" ]; then
    pass "Unauthorized access properly blocked"
    info "HTTP Code: $HTTP_CODE"
else
    fail "Unauthorized access NOT blocked. HTTP Code: $HTTP_CODE"
fi

# Test 15: Invalid Token
test_header "Invalid Token Protection"
info "Testing with invalid token"

RESPONSE=$(curl -s -w "\n%{http_code}" $API_BASE/auth/me \
    -H "Authorization: Bearer invalid_token_here")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)

if [ "$HTTP_CODE" == "401" ]; then
    pass "Invalid token properly rejected"
    info "HTTP Code: $HTTP_CODE"
else
    fail "Invalid token NOT rejected. HTTP Code: $HTTP_CODE"
fi

# Final Summary
echo ""
echo -e "${BLUE}==================================${NC}"
echo -e "${BLUE}Test Summary${NC}"
echo -e "${BLUE}==================================${NC}"
echo -e "${GREEN}All tests passed! ✅${NC}"
echo ""
echo "Test Details:"
echo "  • User: $TEST_EMAIL"
echo "  • Contracts created: 4"
echo "  • Analyses created: 3 (4th blocked by limit)"
echo "  • Free tier enforcement: Working"
echo "  • Authorization: Working"
echo ""
echo -e "${YELLOW}Note: Test user and data remain in database${NC}"
echo -e "${YELLOW}To clean up, delete user via: DELETE $API_BASE/account${NC}"
echo ""
