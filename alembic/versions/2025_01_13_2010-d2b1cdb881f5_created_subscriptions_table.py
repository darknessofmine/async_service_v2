"""created subscriptions table

Revision ID: d2b1cdb881f5
Revises: bb4b2fc07aee
Create Date: 2025-01-13 20:10:06.050531

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'd2b1cdb881f5'
down_revision: Union[str, None] = 'bb4b2fc07aee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'subscriptions',
        sa.Column('owner_id', sa.Integer(), nullable=False),
        sa.Column('sub_id', sa.Integer(), nullable=False),
        sa.Column('sub_tier_id', sa.Integer(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['owner_id'], ['users.id'],
            ondelete='CASCADE',
        ),
        sa.ForeignKeyConstraint(
            ['sub_id'], ['users.id'],
            ondelete='CASCADE',
        ),
        sa.ForeignKeyConstraint(
            ['sub_tier_id'], ['sub_tiers.id'],
            ondelete='SET NULL',
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint(
            'owner_id', 'sub_id',
            name='uq__subscription__owner_id__sub_id',
        )
    )


def downgrade() -> None:
    op.drop_table('subscriptions')
