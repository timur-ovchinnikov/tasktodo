from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# Revision identifiers, used by Alembic.
revision = 'update_tasks_table_with_executor'
down_revision = 'update_tasks_table'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('tasks', sa.Column('executor_id', UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False))


def downgrade():
    op.drop_column('tasks', 'executor_id')
