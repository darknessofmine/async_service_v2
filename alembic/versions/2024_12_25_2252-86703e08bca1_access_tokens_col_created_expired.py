"""access_tokens: col created->expired

Revision ID: 86703e08bca1
Revises: 15c887ab9452
Create Date: 2024-12-25 22:52:37.914302

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '86703e08bca1'
down_revision: Union[str, None] = '15c887ab9452'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'access_tokens',
        sa.Column('expired', sa.DateTime(), nullable=False),
    )
    op.alter_column(
        'access_tokens',
        'token',
        existing_type=sa.VARCHAR(length=128),
        type_=sa.String(length=512),
        existing_nullable=False
    )
    op.drop_index('ix_access_tokens_created', table_name='access_tokens')
    op.create_index(
        op.f('ix_access_tokens_expired'),
        'access_tokens',
        ['expired'],
        unique=False,
    )
    op.drop_column('access_tokens', 'created')


def downgrade() -> None:
    op.add_column(
        'access_tokens',
        sa.Column(
            'created',
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.drop_index(op.f('ix_access_tokens_expired'), table_name='access_tokens')
    op.create_index(
        'ix_access_tokens_created',
        'access_tokens',
        ['created'],
        unique=False,
    )
    op.alter_column(
        'access_tokens',
        'token',
        existing_type=sa.String(length=512),
        type_=sa.VARCHAR(length=128),
        existing_nullable=False,
    )
    op.drop_column('access_tokens', 'expired')
