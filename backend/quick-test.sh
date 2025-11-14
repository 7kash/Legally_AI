#!/bin/bash
# Quick test script for the bug fix

set -e

echo "=================================="
echo "Legally AI - Quick Test Setup"
echo "=================================="
echo ""

# Check if Docker is available
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    echo "✅ Docker and Docker Compose found"
    echo ""
    echo "Starting services with Docker Compose..."
    echo ""

    # Start services
    docker-compose up -d postgres redis

    echo "⏳ Waiting for services to be ready..."
    sleep 5

    echo ""
    echo "✅ Services started"
    echo ""
    echo "Setting up Python environment..."

    # Create venv if it doesn't exist
    if [ ! -d "venv" ]; then
        python3 -m venv venv
    fi

    source venv/bin/activate
    pip install -q -r requirements.txt

    echo "✅ Python environment ready"
    echo ""
    echo "Initializing database..."
    echo ""

    python scripts/init_db.py <<EOF
n
EOF

    echo ""
    echo "=================================="
    echo "✅ Setup Complete!"
    echo "=================================="
    echo ""
    echo "Now open 3 terminal windows:"
    echo ""
    echo "Terminal 1 - Start API:"
    echo "  cd backend"
    echo "  source venv/bin/activate"
    echo "  python -m app.main"
    echo ""
    echo "Terminal 2 - Start Celery:"
    echo "  cd backend"
    echo "  source venv/bin/activate"
    echo "  celery -A app.celery_app worker --loglevel=info"
    echo ""
    echo "Terminal 3 - Run Test:"
    echo "  cd backend"
    echo "  source venv/bin/activate"
    echo "  python tests/test_bug_fix.py"
    echo ""
    echo "Or use Docker Compose for all services:"
    echo "  docker-compose up"
    echo ""

else
    echo "❌ Docker not found. Please install Docker and Docker Compose"
    echo ""
    echo "Manual setup:"
    echo "1. Install PostgreSQL and Redis"
    echo "2. Run: python3 -m venv venv"
    echo "3. Run: source venv/bin/activate"
    echo "4. Run: pip install -r requirements.txt"
    echo "5. Run: python scripts/init_db.py"
    echo "6. See TESTING.md for full instructions"
    exit 1
fi
