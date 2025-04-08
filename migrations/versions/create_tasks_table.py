from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision = 'create_tasks_table'
down_revision = 'create_users_table'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'tasks',
        sa.Column('id', sa.String, primary_key=True, index=True),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('description', sa.String, nullable=True),
        sa.Column('due_date', sa.DateTime, nullable=False),
    )


def downgrade():
    op.drop_table('tasks')
