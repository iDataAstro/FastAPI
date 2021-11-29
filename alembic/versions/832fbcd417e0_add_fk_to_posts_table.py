"""add fk to posts table

Revision ID: 832fbcd417e0
Revises: dc6b5b4ef4da
Create Date: 2021-11-19 16:23:19.359711

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '832fbcd417e0'
down_revision = 'dc6b5b4ef4da'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.column('owner_id'), sa.Integer(), nullable=False)
    op.add_foreign_key('posts_users_fk', source_table="posts", referent_table="users", local_cols=['id'],
                       remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
