"""Add feedback table

Revision ID: 007_add_feedback
Revises: 006_add_deadlines
Create Date: 2025-11-15

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '007_add_feedback'
down_revision = '006_add_deadlines'
branch_labels = None
depends_on = None


def upgrade():
    # Create enum types for feedback
    feedback_type_enum = postgresql.ENUM(
        'accuracy', 'quality', 'missing', 'incorrect', 'other',
        name='feedbacktype'
    )
    feedback_type_enum.create(op.get_bind())

    feedback_section_enum = postgresql.ENUM(
        'obligations', 'rights', 'risks', 'payment_terms',
        'calendar', 'mitigations', 'suggestions', 'screening', 'overall',
        name='feedbacksection'
    )
    feedback_section_enum.create(op.get_bind())

    # Create feedback table
    op.create_table(
        'feedback',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('analysis_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('contract_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('feedback_type', sa.Enum('accuracy', 'quality', 'missing', 'incorrect', 'other', name='feedbacktype'), nullable=False),
        sa.Column('section', sa.Enum('obligations', 'rights', 'risks', 'payment_terms', 'calendar', 'mitigations', 'suggestions', 'screening', 'overall', name='feedbacksection'), nullable=False),
        sa.Column('item_index', sa.Integer(), nullable=True),
        sa.Column('is_accurate', sa.Boolean(), nullable=True),
        sa.Column('quality_rating', sa.Integer(), nullable=True),
        sa.Column('comment', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['analysis_id'], ['analyses.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['contract_id'], ['contracts.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes for better query performance
    op.create_index('ix_feedback_user_id', 'feedback', ['user_id'])
    op.create_index('ix_feedback_analysis_id', 'feedback', ['analysis_id'])
    op.create_index('ix_feedback_contract_id', 'feedback', ['contract_id'])


def downgrade():
    op.drop_index('ix_feedback_contract_id', table_name='feedback')
    op.drop_index('ix_feedback_analysis_id', table_name='feedback')
    op.drop_index('ix_feedback_user_id', table_name='feedback')
    op.drop_table('feedback')

    # Drop enum types
    sa.Enum(name='feedbacksection').drop(op.get_bind())
    sa.Enum(name='feedbacktype').drop(op.get_bind())
