"""follows table added uq

Revision ID: 2325953a34f9
Revises: 5b84e4066dba
Create Date: 2025-02-04 21:09:31.293417

"""
from typing import Sequence, Union

from alembic import op


revision: str = '2325953a34f9'
down_revision: Union[str, None] = '5b84e4066dba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(
        'uq__follow__owner_id__client_id',
        'follows',
        ['owner_id', 'client_id'],
    )


def downgrade() -> None:
    op.drop_constraint(
        'uq__follow__owner_id__client_id',
        'follows',
        type_='unique',
    )
