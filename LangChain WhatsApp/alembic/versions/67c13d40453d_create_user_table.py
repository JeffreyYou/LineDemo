"""create_user_table

Revision ID: 67c13d40453d
Revises: 3b2e26d7395f
Create Date: 2023-12-29 02:51:37.102132

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67c13d40453d'
down_revision = '3b2e26d7395f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('user',
                    sa.Column('id', sa.Integer(),primary_key=True, index=True),
                    sa.Column('user_id', sa.String(100), nullable=True),
                    sa.Column('user_name', sa.String(100), nullable=True),
                    sa.Column('user_gender', sa.String(100), nullable=True),
                    sa.Column('is_in_group', sa.Boolean, nullable=True),
                    sa.Column('is_open_account', sa.Boolean, nullable=True),
                    sa.Column('investment_knowledge', sa.String(100), nullable=True),
                    sa.Column('account_agency', sa.String(100), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    )



def downgrade() -> None:
    op.drop_table('user')

