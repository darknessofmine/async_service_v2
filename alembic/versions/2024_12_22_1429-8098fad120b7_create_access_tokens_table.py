"""create access_tokens table

Revision ID: 8098fad120b7
Revises: 2785694afb8f
Create Date: 2024-12-22 14:29:45.772442

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '8098fad120b7'
down_revision: Union[str, None] = '2785694afb8f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'access_tokens',
        sa.Column('token', sa.String(length=128), nullable=False),
        sa.Column('created', sa.DateTime(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('token')
    )
    op.create_index(
        op.f('ix_access_tokens_created'),
        'access_tokens',
        ['created'],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f('ix_access_tokens_created'), table_name='access_tokens')
    op.drop_table('access_tokens')
