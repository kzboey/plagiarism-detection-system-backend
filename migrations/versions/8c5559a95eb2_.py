"""empty message

Revision ID: 8c5559a95eb2
Revises: d93656ff3e89
Create Date: 2021-10-29 16:18:06.583655

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c5559a95eb2'
down_revision = 'd93656ff3e89'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('USERS',
    sa.Column('eid', sa.String(length=20), nullable=False),
    sa.Column('password', sa.String(length=20), nullable=False),
    sa.Column('last_name', sa.String(length=30), nullable=False),
    sa.Column('first_name', sa.String(length=30), nullable=False),
    sa.Column('other_name', sa.String(length=30), nullable=True),
    sa.Column('email', sa.String(length=20), nullable=False),
    sa.Column('phone', sa.String(length=30), nullable=True),
    sa.Column('organization', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('eid'),
    sa.UniqueConstraint('email')
    )
    op.create_table('TASKS',
    sa.Column('task_id', sa.Integer(), nullable=False),
    sa.Column('course_id', sa.String(length=20), nullable=False),
    sa.Column('course_title', sa.String(length=50), nullable=False),
    sa.Column('task_name', sa.String(length=100), nullable=False),
    sa.Column('start_date', sa.DateTime(), nullable=False),
    sa.Column('due_date', sa.DateTime(), nullable=False),
    sa.Column('modified_date', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('eid_fk', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['eid_fk'], ['USERS.eid'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('task_id')
    )
    op.create_table('SUBMISSIONS',
    sa.Column('submission_id', sa.Integer(), nullable=False),
    sa.Column('author_name', sa.String(length=255), nullable=False),
    sa.Column('overall_similarity', sa.Numeric(precision=3, scale=2), nullable=True),
    sa.Column('modified_date', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('task_id_FK', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['task_id_FK'], ['TASKS.task_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('submission_id')
    )
    op.create_table('DOCUMENTS',
    sa.Column('document_id', sa.Integer(), nullable=False),
    sa.Column('document_name', sa.String(length=255), nullable=False),
    sa.Column('document_path', sa.String(length=255), nullable=False),
    sa.Column('submission_id_FK', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['submission_id_FK'], ['SUBMISSIONS.submission_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('document_id')
    )
    op.create_table('PAGES',
    sa.Column('page_id', sa.Integer(), nullable=False),
    sa.Column('page_name', sa.String(length=255), nullable=False),
    sa.Column('page_path', sa.String(length=255), nullable=False),
    sa.Column('submission_id_FK', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['submission_id_FK'], ['SUBMISSIONS.submission_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('page_id')
    )
    op.create_table('CONTENTS',
    sa.Column('content_type', sa.String(length=50), nullable=False),
    sa.Column('content_id', sa.Integer(), nullable=False),
    sa.Column('content_value', sa.Text(), nullable=False),
    sa.Column('position_x1', sa.SmallInteger(), nullable=False),
    sa.Column('position_x2', sa.SmallInteger(), nullable=False),
    sa.Column('position_y1', sa.SmallInteger(), nullable=False),
    sa.Column('confidence', sa.SmallInteger(), nullable=False),
    sa.Column('page_id_FK', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['page_id_FK'], ['PAGES.page_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('content_id')
    )
    op.create_table('SOURCES',
    sa.Column('sources_id', sa.Integer(), nullable=False),
    sa.Column('content_id_FK', sa.Integer(), nullable=False),
    sa.Column('origin', sa.String(length=255), nullable=False),
    sa.Column('similarity', sa.Numeric(precision=3, scale=2), nullable=False),
    sa.ForeignKeyConstraint(['content_id_FK'], ['CONTENTS.content_id'], ),
    sa.PrimaryKeyConstraint('sources_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('SOURCES')
    op.drop_table('CONTENTS')
    op.drop_table('PAGES')
    op.drop_table('DOCUMENTS')
    op.drop_table('SUBMISSIONS')
    op.drop_table('TASKS')
    op.drop_table('USERS')
    # ### end Alembic commands ###
