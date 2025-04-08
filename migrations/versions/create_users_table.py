from alembic import op
import sqlalchemy as sa
import uuid

# Revision identifiers, used by Alembic.
revision = 'create_users_table'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('email', sa.String, nullable=False, unique=True),
        sa.Column('hashed_password', sa.String, nullable=False),
    )


def downgrade():
    op.drop_table('users')
