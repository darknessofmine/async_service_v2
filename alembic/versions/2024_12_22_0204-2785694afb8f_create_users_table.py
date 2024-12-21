"""create users table

Revision ID: 2785694afb8f
Revises:
Create Date: 2024-12-22 02:04:28.520005

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '2785694afb8f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('username', sa.String(length=32), nullable=False),
        sa.Column('password', sa.String(length=32), nullable=False),
        sa.Column('email', sa.String(length=256), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_superuser', sa.Boolean(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index(
        op.f('ix_users_username'),
        'users',
        ['username'],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_table('users')
