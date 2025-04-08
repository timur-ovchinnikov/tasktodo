from alembic import op
import sqlalchemy as sa
import uuid

# revision identifiers, used by Alembic.
revision = '<timestamp>'
down_revision = 'update_tasks_table_with_executor'
branch_labels = None
depends_on = None

def upgrade():
    op.alter_column('tasks', 'id', type_=sa.dialects.postgresql.UUID(as_uuid=True), postgresql_using='id::uuid')

def downgrade():
    op.alter_column('tasks', 'id', type_=sa.String, postgresql_using='id::text')
