"""Add user_id to analyses table

Revision ID: 008_add_user_id_analyses
Revises: 007_add_feedback
Create Date: 2025-11-16

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '008_add_user_id_analyses'
down_revision = '007_add_feedback'
branch_labels = None
depends_on = None


def upgrade():
    # Step 1: Add user_id column as nullable first
    op.add_column('analyses',
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True)
    )

    # Step 2: Populate user_id from contract.user_id for existing records
    # This ensures all existing analyses get the correct user_id
    op.execute("""
        UPDATE analyses
        SET user_id = contracts.user_id
        FROM contracts
        WHERE analyses.contract_id = contracts.id
    """)

    # Step 3: Make user_id NOT NULL now that it's populated
    op.alter_column('analyses', 'user_id',
        existing_type=postgresql.UUID(as_uuid=True),
        nullable=False
    )

    # Step 4: Add foreign key constraint
    op.create_foreign_key(
        'fk_analyses_user_id_users',
        'analyses', 'users',
        ['user_id'], ['id'],
        ondelete='CASCADE'
    )

    # Step 5: Add index for better query performance
    op.create_index('ix_analyses_user_id', 'analyses', ['user_id'])


def downgrade():
    # Remove in reverse order
    op.drop_index('ix_analyses_user_id', table_name='analyses')
    op.drop_constraint('fk_analyses_user_id_users', 'analyses', type_='foreignkey')
    op.drop_column('analyses', 'user_id')
