"""Add deadlines table

Revision ID: 006_add_deadlines
Revises: 005_add_audit_log
Create Date: 2025-11-15

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '006_add_deadlines'
down_revision = '005_add_audit_log'
branch_labels = None
depends_on = None


def upgrade():
    # Create enum type for deadline types
    deadline_type_enum = postgresql.ENUM(
        'payment', 'renewal', 'notice', 'termination',
        'option_exercise', 'obligation', 'other',
        name='deadlinetype'
    )
    deadline_type_enum.create(op.get_bind())

    # Create deadlines table
    op.create_table(
        'deadlines',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('contract_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('analysis_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('deadline_type', sa.Enum('payment', 'renewal', 'notice', 'termination', 'option_exercise', 'obligation', 'other', name='deadlinetype'), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('date', sa.DateTime(), nullable=True),
        sa.Column('date_formula', sa.String(length=200), nullable=True),
        sa.Column('is_recurring', sa.Boolean(), nullable=True),
        sa.Column('is_completed', sa.Boolean(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('source_section', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['analysis_id'], ['analyses.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['contract_id'], ['contracts.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes for better query performance
    op.create_index('ix_deadlines_contract_id', 'deadlines', ['contract_id'])
    op.create_index('ix_deadlines_analysis_id', 'deadlines', ['analysis_id'])
    op.create_index('ix_deadlines_user_id', 'deadlines', ['user_id'])
    op.create_index('ix_deadlines_date', 'deadlines', ['date'])
    op.create_index('ix_deadlines_is_completed', 'deadlines', ['is_completed'])


def downgrade():
    op.drop_index('ix_deadlines_is_completed', table_name='deadlines')
    op.drop_index('ix_deadlines_date', table_name='deadlines')
    op.drop_index('ix_deadlines_user_id', table_name='deadlines')
    op.drop_index('ix_deadlines_analysis_id', table_name='deadlines')
    op.drop_index('ix_deadlines_contract_id', table_name='deadlines')
    op.drop_table('deadlines')

    # Drop enum type
    sa.Enum(name='deadlinetype').drop(op.get_bind())
