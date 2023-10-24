"""create user table

Revision ID: 08634a84a8e8
Revises: 
Create Date: 2023-10-22 23:26:43.416114

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '08634a84a8e8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column('platform_type', sa.String, nullable=False),
        sa.Column('platform_user_id', sa.String, nullable=False),
        sa.Column('user_name', sa.String, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
    )
    op.create_index(
        index_name='index_uniq_user_in_platform',
        table_name='users',
        columns=['platform_user_id', 'platform_type'],
        unique=True
    )


def downgrade() -> None:
    op.drop_table('users')
