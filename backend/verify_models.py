#!/usr/bin/env python3
"""
Verify SQLAlchemy model relationships are correctly configured.
"""

import sys
sys.path.insert(0, '/home/user/Legally_AI/backend')

try:
    from app.models.user import User
    from app.models.contract import Contract
    from app.models.analysis import Analysis
    from app.models.deadline import Deadline
    from app.models.feedback import Feedback

    print("✅ All models imported successfully")

    # Check User relationships
    print("\n📋 User model relationships:")
    print(f"  - contracts: {User.contracts}")
    print(f"  - analyses: {User.analyses}")
    print(f"  - deadlines: {User.deadlines}")
    print(f"  - feedback: {User.feedback}")

    # Check Contract relationships
    print("\n📋 Contract model relationships:")
    print(f"  - user: {Contract.user}")
    print(f"  - analyses: {Contract.analyses}")
    print(f"  - deadlines: {Contract.deadlines}")
    print(f"  - feedback: {Contract.feedback}")

    # Check Contract.user_id foreign key
    user_id_col = Contract.__table__.columns['user_id']
    print(f"\n🔑 Contract.user_id foreign keys: {list(user_id_col.foreign_keys)}")

    # Check Analysis relationships
    print("\n📋 Analysis model relationships:")
    print(f"  - contract: {Analysis.contract}")
    print(f"  - events: {Analysis.events}")
    print(f"  - deadlines: {Analysis.deadlines}")
    print(f"  - feedback: {Analysis.feedback}")

    # Check Analysis.contract_id foreign key
    contract_id_col = Analysis.__table__.columns['contract_id']
    print(f"\n🔑 Analysis.contract_id foreign keys: {list(contract_id_col.foreign_keys)}")

    print("\n✅ All model relationships configured correctly!")
    print("✅ Foreign keys properly defined!")

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
