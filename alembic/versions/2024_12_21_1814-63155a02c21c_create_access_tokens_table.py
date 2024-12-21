"""create access_tokens table

Revision ID: 63155a02c21c
Revises: a145ac685e4e
Create Date: 2024-12-21 18:14:03.123652

"""
from typing import Sequence, Union

from alembic import op
import fastapi_users_db_sqlalchemy
import sqlalchemy as sa


revision: str = '63155a02c21c'
down_revision: Union[str, None] = 'a145ac685e4e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'access_tokens',
        sa.Column('token', sa.String(length=43), nullable=False),
        sa.Column(
            'created_at',
            fastapi_users_db_sqlalchemy.generics.TIMESTAMPAware(timezone=True),
            nullable=False
        ),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('token')
    )
    op.create_index(
        op.f('ix_access_tokens_created_at'),
        'access_tokens',
        ['created_at'],
        unique=False
    )


def downgrade() -> None:
    op.drop_index(
        op.f('ix_access_tokens_created_at'),
        table_name='access_tokens'
    )
    op.drop_table('access_tokens')
