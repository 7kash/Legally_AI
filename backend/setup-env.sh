#!/bin/bash

# Interactive .env Setup Script
# Helps create .env file with all required keys

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Legally AI - Environment Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${NC}"
echo ""

# Check if .env already exists
if [ -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env file already exists${NC}"
    echo "Do you want to overwrite it? (y/N)"
    read -r overwrite

    if [[ $overwrite != "y" && $overwrite != "Y" ]]; then
        echo "Keeping existing .env file. Exiting."
        exit 0
    fi

    # Backup existing .env
    cp .env .env.backup
    echo -e "${GREEN}✅ Backed up existing .env to .env.backup${NC}"
fi

# Generate SECRET_KEY
echo -e "${BLUE}Step 1: Generating SECRET_KEY...${NC}"

if command -v python3 &> /dev/null; then
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
    echo -e "${GREEN}✅ Generated SECRET_KEY using Python${NC}"
elif command -v openssl &> /dev/null; then
    SECRET_KEY=$(openssl rand -hex 32)
    echo -e "${GREEN}✅ Generated SECRET_KEY using OpenSSL${NC}"
else
    echo -e "${RED}❌ Cannot generate SECRET_KEY${NC}"
    echo "Please install Python or OpenSSL, or manually create one."
    exit 1
fi

echo -e "${YELLOW}Your SECRET_KEY: ${SECRET_KEY}${NC}"
echo ""

# Get GROQ_API_KEY
echo -e "${BLUE}Step 2: Setting up GROQ_API_KEY...${NC}"
echo ""
echo "Do you have a Groq API key? (y/N)"
echo "If not, get one at: https://console.groq.com/keys"
read -r has_groq

if [[ $has_groq == "y" || $has_groq == "Y" ]]; then
    echo "Enter your GROQ_API_KEY:"
    read -r GROQ_API_KEY

    if [ -z "$GROQ_API_KEY" ]; then
        echo -e "${RED}❌ GROQ_API_KEY cannot be empty${NC}"
        exit 1
    fi

    echo -e "${GREEN}✅ GROQ_API_KEY set${NC}"
else
    echo -e "${YELLOW}⚠️  You need a Groq API key for contract analysis${NC}"
    echo ""
    echo "Quick steps to get one:"
    echo "1. Visit: https://console.groq.com/"
    echo "2. Sign up (free)"
    echo "3. Go to API Keys section"
    echo "4. Create new key"
    echo ""
    echo "Press Enter when you have your key..."
    read

    echo "Enter your GROQ_API_KEY:"
    read -r GROQ_API_KEY

    if [ -z "$GROQ_API_KEY" ]; then
        echo -e "${RED}❌ GROQ_API_KEY is required${NC}"
        exit 1
    fi

    echo -e "${GREEN}✅ GROQ_API_KEY set${NC}"
fi

echo ""

# Get SENDGRID_API_KEY (optional)
echo -e "${BLUE}Step 3: Setting up SENDGRID_API_KEY (optional)...${NC}"
echo ""
echo "SendGrid is used for sending emails (password reset, verification)."
echo "For development, you can skip this - emails will be logged instead."
echo ""
echo "Do you want to set up SendGrid? (y/N)"
read -r setup_sendgrid

if [[ $setup_sendgrid == "y" || $setup_sendgrid == "Y" ]]; then
    echo ""
    echo "Get a SendGrid API key:"
    echo "1. Visit: https://signup.sendgrid.com/ (free tier available)"
    echo "2. Create account and verify email"
    echo "3. Go to Settings > API Keys"
    echo "4. Create new key with Full Access"
    echo ""
    echo "Enter your SENDGRID_API_KEY (or leave empty to skip):"
    read -r SENDGRID_API_KEY

    if [ -n "$SENDGRID_API_KEY" ]; then
        echo -e "${GREEN}✅ SENDGRID_API_KEY set${NC}"

        echo ""
        echo "Enter FROM_EMAIL (the verified sender email):"
        echo "Example: noreply@legally-ai.com"
        read -r FROM_EMAIL

        if [ -z "$FROM_EMAIL" ]; then
            FROM_EMAIL="noreply@legally-ai.com"
        fi
    else
        SENDGRID_API_KEY=""
        FROM_EMAIL="noreply@legally-ai.com"
        echo -e "${YELLOW}⚠️  Skipping SendGrid - emails will be logged to console${NC}"
    fi
else
    SENDGRID_API_KEY=""
    FROM_EMAIL="noreply@legally-ai.com"
    echo -e "${YELLOW}⚠️  Skipping SendGrid - emails will be logged to console${NC}"
fi

echo ""

# Create .env file
echo -e "${BLUE}Step 4: Creating .env file...${NC}"

cat > .env << EOF
# Legally AI Environment Configuration
# Generated: $(date)

# ====================================
# Database Configuration
# ====================================
# These are configured by docker-compose.yml
DATABASE_URL=postgresql://legally_ai:password@postgres:5432/legally_ai
REDIS_URL=redis://redis:6379/0

# ====================================
# Security
# ====================================
SECRET_KEY=${SECRET_KEY}

# ====================================
# LLM Provider
# ====================================
LLM_PROVIDER=groq
GROQ_API_KEY=${GROQ_API_KEY}

# Optional: DeepSeek API (alternative to Groq)
# DEEPSEEK_API_KEY=sk_your_deepseek_key_here

# ====================================
# Email Configuration (Optional)
# ====================================
EOF

if [ -n "$SENDGRID_API_KEY" ]; then
    echo "SENDGRID_API_KEY=${SENDGRID_API_KEY}" >> .env
else
    echo "# SENDGRID_API_KEY=  # Uncomment and add key to enable emails" >> .env
fi

cat >> .env << EOF
FROM_EMAIL=${FROM_EMAIL}

# ====================================
# Application Settings
# ====================================
FRONTEND_URL=http://localhost:3000
DEBUG=True

# CORS Origins (comma-separated)
# CORS_ORIGINS=http://localhost:3000,http://localhost:8080

# ====================================
# Monitoring (Optional)
# ====================================
# SENTRY_DSN=https://your-sentry-dsn@sentry.io/project-id

# ====================================
# Celery Configuration
# ====================================
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
EOF

echo -e "${GREEN}✅ Created .env file${NC}"
echo ""

# Show summary
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}Setup Complete! ✅${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "Configuration summary:"
echo "  ✅ SECRET_KEY: Generated"
echo "  ✅ GROQ_API_KEY: Set"

if [ -n "$SENDGRID_API_KEY" ]; then
    echo "  ✅ SENDGRID_API_KEY: Set"
else
    echo "  ⚪ SENDGRID_API_KEY: Skipped (emails will be logged)"
fi

echo ""
echo "Your .env file is ready!"
echo ""
echo -e "${YELLOW}Important:${NC}"
echo "  • Keep your .env file secret"
echo "  • Never commit it to Git (already in .gitignore)"
echo "  • Use different keys for production"
echo ""
echo "Next steps:"
echo "  1. Review .env file: cat .env"
echo "  2. Start application: ./quick-start.sh"
echo "  3. Open: http://localhost:8000/docs"
echo ""
