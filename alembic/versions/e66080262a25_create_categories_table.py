"""create categories table

Revision ID: e66080262a25
Revises: 955e1c75458f
Create Date: 2023-10-23 08:22:17.300038

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e66080262a25'
down_revision: Union[str, None] = '955e1c75458f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'categories',
        sa.Column('id', sa.INTEGER, primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.BIGINT, nullable=False),
        sa.Column('description', sa.String, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=True),
        sa.Column('updated_at', sa.DateTime, nullable=True),
    )


def downgrade() -> None:
    op.drop_table('categories')
