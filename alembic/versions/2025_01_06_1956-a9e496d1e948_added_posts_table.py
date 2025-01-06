"""added posts table

Revision ID: a9e496d1e948
Revises: 26325cfd6295
Create Date: 2025-01-06 19:56:58.799648

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'a9e496d1e948'
down_revision: Union[str, None] = '26325cfd6295'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'posts',
        sa.Column('title', sa.String(length=128), nullable=False),
        sa.Column('text', sa.Text(), nullable=True),
        sa.Column('file_url', sa.String(), nullable=True),
        sa.Column('created', sa.DateTime(), nullable=False),
        sa.Column('updated', sa.DateTime(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('sub_tier_id', sa.Integer(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['sub_tier_id'],
            ['sub_tiers.id'],
            ondelete='SET NULL',
        ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('posts')
