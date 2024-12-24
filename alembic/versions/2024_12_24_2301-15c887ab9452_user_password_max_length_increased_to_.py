"""user_password_max_length_increased_to_256

Revision ID: 15c887ab9452
Revises: 8098fad120b7
Create Date: 2024-12-24 23:01:09.937707

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '15c887ab9452'
down_revision: Union[str, None] = '8098fad120b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        'users',
        'password',
        existing_type=sa.VARCHAR(length=32),
        type_=sa.String(length=256),
        existing_nullable=False)


def downgrade() -> None:
    op.alter_column(
        'users',
        'password',
        existing_type=sa.String(length=256),
        type_=sa.VARCHAR(length=32),
        existing_nullable=False)
