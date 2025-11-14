#!/usr/bin/env python3
"""
Diagnostic script to check the state of the analysis and events.

Run this to see what's in your database and diagnose the issue.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def diagnose():
    """Run diagnostics"""
    print("="*60)
    print("Legally AI - Database Diagnostic")
    print("="*60)

    try:
        from sqlalchemy import create_engine, text, inspect
        from app.config import settings

        engine = create_engine(settings.DATABASE_URL)

        # Check what tables exist
        print("\n📋 Tables in database:")
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        for table in sorted(tables):
            print(f"   - {table}")

        with engine.connect() as conn:
            # Check analyses count
            result = conn.execute(text("SELECT COUNT(*) FROM analyses"))
            analyses_count = result.scalar()
            print(f"\n📊 Total analyses: {analyses_count}")

            # Check latest analysis
            result = conn.execute(text("""
                SELECT id, status, created_at, started_at, completed_at
                FROM analyses
                ORDER BY created_at DESC
                LIMIT 1
            """))
            latest = result.fetchone()

            if latest:
                print(f"\n🔍 Latest analysis:")
                print(f"   ID: {latest[0]}")
                print(f"   Status: {latest[1]}")
                print(f"   Created: {latest[2]}")
                print(f"   Started: {latest[3]}")
                print(f"   Completed: {latest[4]}")

                analysis_id = latest[0]

                # Check events for this analysis
                if 'events' in tables:
                    result = conn.execute(text("""
                        SELECT COUNT(*) FROM events
                        WHERE analysis_id = :aid
                    """), {"aid": str(analysis_id)})
                    event_count = result.scalar()
                    print(f"\n📡 Events for this analysis: {event_count}")

                    if event_count > 0:
                        result = conn.execute(text("""
                            SELECT id, kind, created_at
                            FROM events
                            WHERE analysis_id = :aid
                            ORDER BY created_at ASC
                        """), {"aid": str(analysis_id)})
                        events = result.fetchall()
                        print(f"\n   Events:")
                        for event in events:
                            print(f"   - [{event[2]}] {event[1]}")
                    else:
                        print("\n   ❌ No events found!")
                        print("   This means the Celery worker hasn't created any events.")
                        print("\n   Possible reasons:")
                        print("   1. Celery worker is not running")
                        print("   2. Celery worker encountered an error")
                        print("   3. Celery worker is not connected to Redis")

                elif 'analysis_events' in tables:
                    result = conn.execute(text("""
                        SELECT COUNT(*) FROM analysis_events
                        WHERE analysis_id = :aid
                    """), {"aid": str(analysis_id)})
                    event_count = result.scalar()
                    print(f"\n📡 Analysis events for this analysis: {event_count}")

                    if event_count == 0:
                        print("   ❌ No events found!")
                        print("   This means the Celery worker hasn't created any events.")

            else:
                print("\n   No analyses found in database")

        print("\n" + "="*60)
        print("Diagnostic complete")
        print("="*60)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    diagnose()
