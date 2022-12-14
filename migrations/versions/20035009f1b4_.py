"""empty message

Revision ID: 20035009f1b4
Revises: 
Create Date: 2022-10-11 11:31:25.465972

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20035009f1b4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.Column('token', sa.String(length=64), nullable=True),
    sa.Column('token_expiration', sa.DateTime(), nullable=True),
    sa.Column('cash', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_user_token'), 'user', ['token'], unique=True)
    op.create_table('stock',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ticker', sa.String(length=8), nullable=False),
    sa.Column('new_price', sa.Float(), nullable=False),
    sa.Column('new_shares', sa.Integer(), nullable=False),
    sa.Column('create_date', sa.DateTime(), nullable=False),
    sa.Column('total_shares', sa.Integer(), nullable=True),
    sa.Column('total_invested', sa.Float(), nullable=True),
    sa.Column('total_divested', sa.Float(), nullable=True),
    sa.Column('avg_price', sa.Float(), nullable=True),
    sa.Column('real_value', sa.Float(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('stock')
    op.drop_index(op.f('ix_user_token'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
