"""users table: added is_admin column

Revision ID: 0456d08682d7
Revises: b1cf1d788274
Create Date: 2024-12-30 23:31:14.825350

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '0456d08682d7'
down_revision: Union[str, None] = 'b1cf1d788274'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), nullable=False))


def downgrade() -> None:
    op.drop_column('users', 'is_admin')
