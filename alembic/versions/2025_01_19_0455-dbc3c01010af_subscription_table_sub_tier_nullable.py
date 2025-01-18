"""subscription table sub_tier nullable

Revision ID: dbc3c01010af
Revises: d2b1cdb881f5
Create Date: 2025-01-19 04:55:17.646970

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'dbc3c01010af'
down_revision: Union[str, None] = 'd2b1cdb881f5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        'subscriptions',
        'sub_tier_id',
        existing_type=sa.INTEGER(),
        nullable=True,
    )


def downgrade() -> None:
    op.alter_column(
        'subscriptions',
        'sub_tier_id',
        existing_type=sa.INTEGER(),
        nullable=False,
    )
