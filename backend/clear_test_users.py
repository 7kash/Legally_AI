"""
Quick script to clear test users from the database
"""
import sys
sys.path.insert(0, '/home/user/Legally_AI/backend')

from app.database import SessionLocal
from app.models.user import User

def clear_test_users():
    """Delete all users with test emails"""
    db = SessionLocal()
    try:
        # Find all test users
        test_users = db.query(User).filter(
            User.email.like('test%@example.com')
        ).all()

        print(f"Found {len(test_users)} test users:")
        for user in test_users:
            print(f"  - {user.email} (created: {user.created_at})")

        if test_users:
            # Delete them
            deleted = db.query(User).filter(
                User.email.like('test%@example.com')
            ).delete(synchronize_session=False)

            db.commit()
            print(f"\n✅ Deleted {deleted} test users")
        else:
            print("\n✅ No test users to delete")

    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    clear_test_users()
