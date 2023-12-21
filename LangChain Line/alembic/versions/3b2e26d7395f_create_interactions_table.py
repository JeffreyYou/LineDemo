"""create interactions table

Revision ID: 3b2e26d7395f
Revises: 
Create Date: 2023-12-15 07:05:29.998075

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b2e26d7395f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('interactions',
                    sa.Column('id', sa.Integer(),primary_key=True, index=True),
                    sa.Column('client_message_unicode', sa.Unicode(65535)),
                    sa.Column('server_message_unicode', sa.Unicode(65535)),
                    sa.Column('session_id', sa.String(100), nullable=True),
                    sa.Column('character_name', sa.String(100), nullable=True),
                    sa.Column('timestamp', sa.DateTime(), nullable=True),
                    sa.Column('character_id', sa.String(100), nullable=True),
                    sa.Column('client_id', sa.Integer(), nullable=True),
                    sa.Column('message_id', sa.String(64), nullable=True),
                    sa.Column('platform', sa.String(50), nullable=True),
                    sa.Column('user_id', sa.String(100), nullable=True),
                    sa.Column('action_type', sa.String(50), nullable=True),
                    sa.Column('tools', sa.String(100), nullable=True),
                    sa.Column('llm_config', sa.JSON(), nullable=True),
                    sa.Column('language', sa.String(10), nullable=True),
                    sa.Column('client_message', sa.String(), nullable=True),
                    sa.Column('server_message', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),

                    )


def downgrade() -> None:
    op.drop_table('interactions')

