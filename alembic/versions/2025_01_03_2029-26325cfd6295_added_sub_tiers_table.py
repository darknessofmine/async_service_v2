"""added sub_tiers table

Revision ID: 26325cfd6295
Revises: 0456d08682d7
Create Date: 2025-01-03 20:29:19.925164

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '26325cfd6295'
down_revision: Union[str, None] = '0456d08682d7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'sub_tiers',
        sa.Column('title', sa.String(length=64), nullable=False),
        sa.Column('text', sa.String(length=256), nullable=False),
        sa.Column('image_url', sa.String(), nullable=True),
        sa.Column('price', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint(
            'price', 'user_id',
            name='uq__tier__price__user_id',
        ),
        sa.UniqueConstraint(
            'title', 'user_id',
            name='uq__sub_tier__title__user_id',
        )
    )


def downgrade() -> None:
    op.drop_table('sub_tiers')
