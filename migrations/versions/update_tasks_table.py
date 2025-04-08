from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision = 'update_tasks_table'
down_revision = 'create_tasks_table'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('tasks', sa.Column('completed', sa.Boolean, nullable=False, server_default='false'))


def downgrade():
    op.drop_column('tasks', 'completed')
