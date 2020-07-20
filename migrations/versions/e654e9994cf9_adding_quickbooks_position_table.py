"""adding quickbooks_position table

Revision ID: e654e9994cf9
Revises: 28ddd530807e
Create Date: 2020-07-08 13:42:55.826469

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e654e9994cf9'
down_revision = None
branch_labels = None
depends_on = None

SCHEMA = 'ns_sync'

def upgrade():
    op.create_table(
        'quickbooks_position',
        sa.Column('id', sa.INTEGER, primary_key=True),
        sa.Column('submitter', sa.VARCHAR, nullable=False),
        sa.Column('as_of_date', sa.DateTime,nullable=False),
        sa.Column('period',sa.Date,nullable=False),
        sa.Column('wisetack_junior_position',sa.Numeric(14,2),nullable=False),
        sa.Column('lighter_junior_position', sa.Numeric(14,2),nullable=False),
        schema=SCHEMA
    )


def downgrade():
    op.drop_table('quickbooks_position', schema=SCHEMA)
