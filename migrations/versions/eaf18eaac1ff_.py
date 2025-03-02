"""empty message

Revision ID: eaf18eaac1ff
Revises: 8f930c6345ff
Create Date: 2024-08-28 10:26:12.678507

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'eaf18eaac1ff'
down_revision = '8f930c6345ff'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('article', schema=None) as batch_op:
        batch_op.add_column(sa.Column('thumbnail', sa.String(length=500).with_variant(mysql.NVARCHAR(national=True, length=500), 'mariadb').with_variant(mysql.NVARCHAR(national=True, length=500), 'mysql'), nullable=True))
        batch_op.alter_column('title',
               existing_type=mysql.VARCHAR(charset='utf8mb3', collation='utf8mb3_general_ci', length=500),
               type_=sa.String(length=500).with_variant(mysql.NVARCHAR(national=True, length=500), 'mariadb').with_variant(mysql.NVARCHAR(national=True, length=500), 'mysql'),
               existing_nullable=True)
        batch_op.alter_column('content',
               existing_type=mysql.VARCHAR(charset='utf8mb3', collation='utf8mb3_general_ci', length=15000),
               type_=sa.String(length=15000).with_variant(mysql.NVARCHAR(national=True, length=15000), 'mariadb').with_variant(mysql.NVARCHAR(national=True, length=15000), 'mysql'),
               existing_nullable=True)
        batch_op.alter_column('category',
               existing_type=mysql.VARCHAR(charset='utf8mb3', collation='utf8mb3_general_ci', length=500),
               type_=sa.String(length=500).with_variant(mysql.NVARCHAR(national=True, length=500), 'mariadb').with_variant(mysql.NVARCHAR(national=True, length=500), 'mysql'),
               existing_nullable=True)
        batch_op.alter_column('note',
               existing_type=mysql.VARCHAR(charset='utf8mb3', collation='utf8mb3_general_ci', length=500),
               type_=sa.String(length=500).with_variant(mysql.NVARCHAR(national=True, length=500), 'mariadb').with_variant(mysql.NVARCHAR(national=True, length=500), 'mysql'),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('article', schema=None) as batch_op:
        batch_op.alter_column('note',
               existing_type=sa.String(length=500).with_variant(mysql.NVARCHAR(national=True, length=500), 'mariadb').with_variant(mysql.NVARCHAR(national=True, length=500), 'mysql'),
               type_=mysql.VARCHAR(charset='utf8mb3', collation='utf8mb3_general_ci', length=500),
               existing_nullable=True)
        batch_op.alter_column('category',
               existing_type=sa.String(length=500).with_variant(mysql.NVARCHAR(national=True, length=500), 'mariadb').with_variant(mysql.NVARCHAR(national=True, length=500), 'mysql'),
               type_=mysql.VARCHAR(charset='utf8mb3', collation='utf8mb3_general_ci', length=500),
               existing_nullable=True)
        batch_op.alter_column('content',
               existing_type=sa.String(length=15000).with_variant(mysql.NVARCHAR(national=True, length=15000), 'mariadb').with_variant(mysql.NVARCHAR(national=True, length=15000), 'mysql'),
               type_=mysql.VARCHAR(charset='utf8mb3', collation='utf8mb3_general_ci', length=15000),
               existing_nullable=True)
        batch_op.alter_column('title',
               existing_type=sa.String(length=500).with_variant(mysql.NVARCHAR(national=True, length=500), 'mariadb').with_variant(mysql.NVARCHAR(national=True, length=500), 'mysql'),
               type_=mysql.VARCHAR(charset='utf8mb3', collation='utf8mb3_general_ci', length=500),
               existing_nullable=True)
        batch_op.drop_column('thumbnail')

    # ### end Alembic commands ###
