"""add unique key to users table

Revision ID: 893f58e5abc0
Revises: 832fbcd417e0
Create Date: 2021-11-29 16:35:12.892308

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '893f58e5abc0'
down_revision = '832fbcd417e0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint('uq_users_email', 'users', ['email'])


def downgrade():
    op.drop_constraint('uq_users_email', 'users')
