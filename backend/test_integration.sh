#!/bin/bash

# Integration Testing Script for Legally AI
# This script tests all API endpoints systematically
#
# FIXES APPLIED:
# - Password changed to testpass123 (from TestPassword123!)
# - File type changed to .pdf (from .txt)
# - Script uses proper error handling

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
TEST_PASSWORD="testpass123"  # FIXED: Changed from TestPassword123!

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
RESPONSE=$(curl -s http://localhost:8000/health)
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

RESPONSE=$(curl -s -X GET $API_BASE/auth/me \
    -H "Authorization: Bearer $TOKEN")

EMAIL=$(echo "$RESPONSE" | jq -r '.email' 2>/dev/null)

if [ "$EMAIL" == "$TEST_EMAIL" ]; then
    pass "Profile retrieved successfully"
else
    fail "Failed to get profile. Response: $RESPONSE"
fi

# Test 5: Contract Upload
test_header "Contract Upload"
info "Uploading test PDF contract"

# Check if test_contract.pdf exists
if [ ! -f "test_contract.pdf" ]; then
    info "test_contract.pdf not found. Creating a minimal PDF for testing..."
    # Create a minimal PDF if it doesn't exist
    echo "%PDF-1.4
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj
2 0 obj
<<
/Type /Pages
/Kids [3 0 R]
/Count 1
>>
endobj
3 0 obj
<<
/Type /Page
/Parent 2 0 R
/Resources <<
/Font <<
/F1 <<
/Type /Font
/Subtype /Type1
/BaseFont /Helvetica
>>
>>
>>
/MediaBox [0 0 612 792]
/Contents 4 0 R
>>
endobj
4 0 obj
<<
/Length 44
>>
stream
BT
/F1 12 Tf
100 700 Td
(Test Contract) Tj
ET
endstream
endobj
xref
0 5
0000000000 65535 f
0000000009 00000 n
0000000058 00000 n
0000000115 00000 n
0000000317 00000 n
trailer
<<
/Size 5
/Root 1 0 R
>>
startxref
410
%%EOF" > test_contract.pdf
fi

# FIXED: Changed from .txt to .pdf
# FIXED: Changed endpoint from /contracts/ to /contracts/upload
RESPONSE=$(curl -s -X POST $API_BASE/contracts/upload \
    -H "Authorization: Bearer $TOKEN" \
    -F "file=@test_contract.pdf")

CONTRACT_ID=$(echo "$RESPONSE" | jq -r '.contract_id' 2>/dev/null)

if [ "$CONTRACT_ID" != "null" ] && [ -n "$CONTRACT_ID" ]; then
    pass "Contract uploaded successfully"
    info "Contract ID: $CONTRACT_ID"
else
    fail "Contract upload failed. Response: $RESPONSE"
fi

# Test 6: List Contracts
test_header "List Contracts"

# FIXED: Use trailing slash to avoid 307 redirect
RESPONSE=$(curl -s -X GET "$API_BASE/contracts/?page=1&page_size=10" \
    -H "Authorization: Bearer $TOKEN")

TOTAL=$(echo "$RESPONSE" | jq -r '.total' 2>/dev/null)

if [ "$TOTAL" != "null" ] && [ -n "$TOTAL" ] && [ "$TOTAL" -ge 0 ] 2>/dev/null; then
    pass "Contracts listed successfully (Total: $TOTAL)"
else
    fail "Failed to list contracts. Response: $RESPONSE"
fi

# Test 7: Get Contract Details
test_header "Get Contract Details"

RESPONSE=$(curl -s -X GET "$API_BASE/contracts/$CONTRACT_ID" \
    -H "Authorization: Bearer $TOKEN")

FILENAME=$(echo "$RESPONSE" | jq -r '.filename' 2>/dev/null)

if [ "$FILENAME" != "null" ] && [ -n "$FILENAME" ]; then
    pass "Contract details retrieved"
    info "Filename: $FILENAME"
else
    fail "Failed to get contract details. Response: $RESPONSE"
fi

# Test 8: Start Analysis
test_header "Start Analysis"

RESPONSE=$(curl -s -X POST "$API_BASE/analyses/" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"contract_id\":\"$CONTRACT_ID\"}")

ANALYSIS_ID=$(echo "$RESPONSE" | jq -r '.id' 2>/dev/null)

if [ "$ANALYSIS_ID" != "null" ] && [ -n "$ANALYSIS_ID" ]; then
    pass "Analysis started"
    info "Analysis ID: $ANALYSIS_ID"
else
    fail "Failed to start analysis. Response: $RESPONSE"
fi

# Test 9: Get Analysis Status
test_header "Get Analysis Status"
info "Waiting 2 seconds for analysis to process..."
sleep 2

RESPONSE=$(curl -s -X GET "$API_BASE/analyses/$ANALYSIS_ID" \
    -H "Authorization: Bearer $TOKEN")

STATUS=$(echo "$RESPONSE" | jq -r '.status' 2>/dev/null)

if [ "$STATUS" != "null" ] && [ -n "$STATUS" ]; then
    pass "Analysis status retrieved: $STATUS"
else
    fail "Failed to get analysis status. Response: $RESPONSE"
fi

# Test 10: List Analyses
test_header "List Analyses"

RESPONSE=$(curl -s -X GET "$API_BASE/analyses/?page=1&page_size=10" \
    -H "Authorization: Bearer $TOKEN")

ANALYSES_TOTAL=$(echo "$RESPONSE" | jq -r '.total' 2>/dev/null)

if [ "$ANALYSES_TOTAL" != "null" ] && [ -n "$ANALYSES_TOTAL" ] && [ "$ANALYSES_TOTAL" -ge 0 ] 2>/dev/null; then
    pass "Analyses listed successfully (Total: $ANALYSES_TOTAL)"
else
    fail "Failed to list analyses. Response: $RESPONSE"
fi

# Summary
echo ""
echo -e "${BLUE}==================================${NC}"
echo -e "${GREEN}✅ All Tests Passed!${NC}"
echo -e "${BLUE}==================================${NC}"
echo ""
echo -e "${YELLOW}Summary:${NC}"
echo -e "  • Test User: $TEST_EMAIL"
echo -e "  • Contract ID: $CONTRACT_ID"
echo -e "  • Analysis ID: $ANALYSIS_ID"
echo -e "  • Total Contracts: $TOTAL"
echo -e "  • Total Analyses: $ANALYSES_TOTAL"
echo ""
