"""created follows table

Revision ID: 5b84e4066dba
Revises: dbc3c01010af
Create Date: 2025-02-04 19:15:14.728185

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '5b84e4066dba'
down_revision: Union[str, None] = 'dbc3c01010af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'follows',
        sa.Column('owner_id', sa.Integer(), nullable=False),
        sa.Column('client_id', sa.Integer(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['client_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('follows')
