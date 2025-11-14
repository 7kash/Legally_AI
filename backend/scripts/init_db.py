#!/usr/bin/env python3
"""
Database initialization script.

This script:
1. Creates all database tables
2. Inserts sample data for testing (optional)
3. Verifies the database is set up correctly
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import engine, Base, SessionLocal
from app.models import Contract, Analysis, AnalysisEvent
import uuid
from datetime import datetime


def init_database():
    """Initialize the database"""
    print("🔧 Initializing database...")

    try:
        # Create all tables
        print("  Creating tables...")
        Base.metadata.create_all(bind=engine)
        print("  ✅ Tables created successfully")

        # Verify tables exist
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()

        print(f"\n  📋 Tables in database:")
        for table in sorted(tables):
            print(f"     - {table}")

        if 'contracts' in tables and 'analyses' in tables and 'analysis_events' in tables:
            print("\n✅ Database initialized successfully")
            print(f"✅ All required tables created: {', '.join(sorted(tables))}")
            return True
        else:
            print("\n❌ Error: Some tables are missing")
            return False

    except Exception as e:
        print(f"\n❌ Error initializing database: {e}")
        import traceback
        traceback.print_exc()
        return False


def create_sample_data():
    """Create sample data for testing (optional)"""
    print("\n🔧 Creating sample data...")

    db = SessionLocal()

    try:
        # Create a sample contract
        contract = Contract(
            id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            filename="sample-employment-contract.pdf",
            file_path="/tmp/sample.pdf",
            file_size=102400,
            mime_type="application/pdf",
            extracted_text="""
            EMPLOYMENT AGREEMENT

            This Employment Agreement is entered into on January 1, 2024,
            between ABC Corporation and John Doe.

            1. Position: Software Engineer
            2. Salary: $100,000 per year
            3. Start Date: February 1, 2024
            4. Benefits: Health insurance, 401k matching
            """,
            detected_language="english",
            jurisdiction="California, USA",
            uploaded_at=datetime.utcnow()
        )

        db.add(contract)
        db.commit()
        db.refresh(contract)

        print(f"  ✅ Sample contract created: {contract.id}")
        print(f"     Filename: {contract.filename}")
        print(f"     Language: {contract.detected_language}")

        return True

    except Exception as e:
        print(f"\n  ❌ Error creating sample data: {e}")
        db.rollback()
        return False
    finally:
        db.close()


def verify_database():
    """Verify database is working correctly"""
    print("\n🔧 Verifying database connection...")

    db = SessionLocal()

    try:
        # Test query
        count = db.query(Contract).count()
        print(f"  ✅ Database connection working")
        print(f"  📊 Contracts in database: {count}")
        return True

    except Exception as e:
        print(f"\n  ❌ Error connecting to database: {e}")
        return False
    finally:
        db.close()


def main():
    """Main entry point"""
    print("="*60)
    print("Legally AI - Database Initialization")
    print("="*60)

    # Initialize database
    if not init_database():
        sys.exit(1)

    # Verify connection
    if not verify_database():
        sys.exit(1)

    # Ask if user wants sample data
    response = input("\n❓ Create sample data for testing? (y/n): ").strip().lower()
    if response == 'y':
        create_sample_data()

    print("\n" + "="*60)
    print("✅ Database setup complete!")
    print("="*60)
    print("\nNext steps:")
    print("  1. Start the API server:     python -m app.main")
    print("  2. Start Celery worker:      celery -A app.celery_app worker --loglevel=info")
    print("  3. Run tests:                python tests/test_bug_fix.py")
    print()


if __name__ == "__main__":
    main()
