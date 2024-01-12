"""empty message

Revision ID: 5bce28283e35
Revises: 286b3c589a32
Create Date: 2024-01-12 08:29:12.166234

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5bce28283e35'
down_revision = '286b3c589a32'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('enquiryactivity',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('enuiry_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['enuiry_id'], ['enquiry.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('enquiryactivity')
    # ### end Alembic commands ###