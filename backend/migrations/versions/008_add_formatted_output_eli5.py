"""Add formatted_output_eli5 field to analyses table

Revision ID: 008_add_eli5
Revises: 007_add_feedback
Create Date: 2025-11-17

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '008_add_eli5'
down_revision = '007_add_feedback'
branch_labels = None
depends_on = None


def upgrade():
    # Add formatted_output_eli5 column to analyses table
    op.add_column(
        'analyses',
        sa.Column('formatted_output_eli5', postgresql.JSON(astext_type=sa.Text()), nullable=True)
    )


def downgrade():
    # Remove formatted_output_eli5 column from analyses table
    op.drop_column('analyses', 'formatted_output_eli5')
