"""create Records table

Revision ID: 955e1c75458f
Revises: 08634a84a8e8
Create Date: 2023-10-23 06:21:29.701959

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '955e1c75458f'
down_revision: Union[str, None] = '08634a84a8e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'records',
        sa.Column('id', sa.INTEGER, primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.BIGINT, nullable=False),
        sa.Column('category_id', sa.String, nullable=False),
        sa.Column('amount', sa.Float, nullable=False),
        sa.Column('note', sa.String, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=True),
        sa.Column('updated_at', sa.DateTime, nullable=True)
    )


def downgrade() -> None:
    op.drop_table('records')
