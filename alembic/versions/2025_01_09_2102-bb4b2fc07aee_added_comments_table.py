"""added comments table

Revision ID: bb4b2fc07aee
Revises: a9e496d1e948
Create Date: 2025-01-09 21:02:43.309433

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'bb4b2fc07aee'
down_revision: Union[str, None] = 'a9e496d1e948'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'comments',
        sa.Column('text', sa.String(length=500), nullable=False),
        sa.Column('created', sa.DateTime(), nullable=False),
        sa.Column('updated', sa.DateTime(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('post_id', sa.Integer(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['post_id'], ['posts.id'],
            ondelete='CASCADE',
        ),
        sa.ForeignKeyConstraint(
            ['user_id'], ['users.id'],
            ondelete='SET NULL',
        ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('comments')
