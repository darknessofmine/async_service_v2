"""users table: added is_author column

Revision ID: 964a1a06b5e6
Revises: aad5b21bea4a
Create Date: 2024-12-29 21:45:51.957278

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '964a1a06b5e6'
down_revision: Union[str, None] = 'aad5b21bea4a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        'profiles',
        'image_url',
        existing_type=sa.VARCHAR(),
        nullable=True,
    )
    op.add_column(
        'users',
        sa.Column('is_author', sa.Boolean(), nullable=False),
    )


def downgrade() -> None:
    op.drop_column('users', 'is_author')
    op.alter_column(
        'profiles',
        'image_url',
        existing_type=sa.VARCHAR(),
        nullable=False,
    )
