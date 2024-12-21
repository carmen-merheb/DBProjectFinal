"""Initial migration

Revision ID: 1817487e61d8
Revises: 
Create Date: 2024-08-15 11:54:06.472338

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1817487e61d8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('role', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.drop_table('companycontacts')
    op.drop_table('location')
    op.drop_table('field')
    op.drop_table('education')
    op.drop_table('status')
    op.drop_table('university')
    op.drop_table('major')
    with op.batch_alter_table('application', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('cover_letter', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('resume', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('timestamp', sa.DateTime(), nullable=True))
        batch_op.drop_constraint('application_ibfk_2', type_='foreignkey')
        batch_op.drop_constraint('application_ibfk_1', type_='foreignkey')
        batch_op.drop_constraint('application_ibfk_3', type_='foreignkey')
        batch_op.create_foreign_key(None, 'internship', ['internship_id'], ['id'])
        batch_op.create_foreign_key(None, 'student', ['student_id'], ['id'])
        batch_op.drop_column('date')
        batch_op.drop_column('description')
        batch_op.drop_column('cv')
        batch_op.drop_column('application_id')
        batch_op.drop_column('status_id')

    with op.batch_alter_table('company', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('company_name', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('website', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'user', ['user_id'], ['id'])
        batch_op.drop_column('address')
        batch_op.drop_column('phone_number')
        batch_op.drop_column('name')
        batch_op.drop_column('industry')
        batch_op.drop_column('email')
        batch_op.drop_column('company_id')

    with op.batch_alter_table('internship', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('requirements', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('location', sa.String(length=100), nullable=True))
        batch_op.drop_constraint('internship_ibfk_2', type_='foreignkey')
        batch_op.drop_constraint('internship_ibfk_1', type_='foreignkey')
        batch_op.drop_constraint('internship_ibfk_3', type_='foreignkey')
        batch_op.create_foreign_key(None, 'company', ['company_id'], ['id'])
        batch_op.drop_column('field_id')
        batch_op.drop_column('tags')
        batch_op.drop_column('is_remote')
        batch_op.drop_column('end_date')
        batch_op.drop_column('location_id')
        batch_op.drop_column('internship_id')
        batch_op.drop_column('skills')
        batch_op.drop_column('start_date')
        batch_op.drop_column('deadline_date')
        batch_op.drop_column('salary')

    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=False))
        batch_op.alter_column('resume',
               existing_type=mysql.TEXT(),
               type_=sa.String(length=255),
               existing_nullable=True)
        batch_op.drop_index('email')
        batch_op.drop_index('idx_student_email')
        batch_op.create_foreign_key(None, 'user', ['user_id'], ['id'])
        batch_op.drop_column('email')
        batch_op.drop_column('student_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.add_column(sa.Column('student_id', mysql.INTEGER(), autoincrement=True, nullable=False))
        batch_op.add_column(sa.Column('email', mysql.VARCHAR(length=100), nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_index('idx_student_email', ['email'], unique=False)
        batch_op.create_index('email', ['email'], unique=True)
        batch_op.alter_column('resume',
               existing_type=sa.String(length=255),
               type_=mysql.TEXT(),
               existing_nullable=True)
        batch_op.drop_column('user_id')
        batch_op.drop_column('id')

    with op.batch_alter_table('internship', schema=None) as batch_op:
        batch_op.add_column(sa.Column('salary', mysql.DECIMAL(precision=10, scale=2), nullable=True))
        batch_op.add_column(sa.Column('deadline_date', sa.DATE(), nullable=True))
        batch_op.add_column(sa.Column('start_date', sa.DATE(), nullable=False))
        batch_op.add_column(sa.Column('skills', mysql.VARCHAR(length=255), nullable=True))
        batch_op.add_column(sa.Column('internship_id', mysql.INTEGER(), autoincrement=True, nullable=False))
        batch_op.add_column(sa.Column('location_id', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('end_date', sa.DATE(), nullable=True))
        batch_op.add_column(sa.Column('is_remote', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('tags', mysql.VARCHAR(length=255), nullable=True))
        batch_op.add_column(sa.Column('field_id', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('internship_ibfk_3', 'field', ['field_id'], ['field_id'])
        batch_op.create_foreign_key('internship_ibfk_1', 'company', ['company_id'], ['company_id'])
        batch_op.create_foreign_key('internship_ibfk_2', 'location', ['location_id'], ['location_id'])
        batch_op.drop_column('location')
        batch_op.drop_column('requirements')
        batch_op.drop_column('id')

    with op.batch_alter_table('company', schema=None) as batch_op:
        batch_op.add_column(sa.Column('company_id', mysql.INTEGER(), autoincrement=True, nullable=False))
        batch_op.add_column(sa.Column('email', mysql.VARCHAR(length=100), nullable=True))
        batch_op.add_column(sa.Column('industry', mysql.VARCHAR(length=100), nullable=True))
        batch_op.add_column(sa.Column('name', mysql.VARCHAR(length=100), nullable=False))
        batch_op.add_column(sa.Column('phone_number', mysql.VARCHAR(length=20), nullable=True))
        batch_op.add_column(sa.Column('address', mysql.VARCHAR(length=255), nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('user_id')
        batch_op.drop_column('website')
        batch_op.drop_column('company_name')
        batch_op.drop_column('id')

    with op.batch_alter_table('application', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status_id', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('application_id', mysql.INTEGER(), autoincrement=True, nullable=False))
        batch_op.add_column(sa.Column('cv', mysql.TEXT(), nullable=True))
        batch_op.add_column(sa.Column('description', mysql.TEXT(), nullable=True))
        batch_op.add_column(sa.Column('date', sa.DATE(), nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('application_ibfk_3', 'status', ['status_id'], ['status_id'])
        batch_op.create_foreign_key('application_ibfk_1', 'student', ['student_id'], ['student_id'])
        batch_op.create_foreign_key('application_ibfk_2', 'internship', ['internship_id'], ['internship_id'])
        batch_op.drop_column('timestamp')
        batch_op.drop_column('resume')
        batch_op.drop_column('cover_letter')
        batch_op.drop_column('id')

    op.create_table('major',
    sa.Column('major_id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=100), nullable=False),
    sa.PrimaryKeyConstraint('major_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('university',
    sa.Column('university_id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=100), nullable=False),
    sa.PrimaryKeyConstraint('university_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('status',
    sa.Column('status_id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=50), nullable=False),
    sa.PrimaryKeyConstraint('status_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('education',
    sa.Column('education_id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('student_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('university_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('major_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('year_of_study', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('gpa', mysql.DECIMAL(precision=3, scale=2), nullable=True),
    sa.Column('graduation_date', sa.DATE(), nullable=True),
    sa.Column('about', mysql.TEXT(), nullable=True),
    sa.ForeignKeyConstraint(['major_id'], ['major.major_id'], name='education_ibfk_3'),
    sa.ForeignKeyConstraint(['student_id'], ['student.student_id'], name='education_ibfk_1'),
    sa.ForeignKeyConstraint(['university_id'], ['university.university_id'], name='education_ibfk_2'),
    sa.PrimaryKeyConstraint('education_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('field',
    sa.Column('field_id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=100), nullable=False),
    sa.PrimaryKeyConstraint('field_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('location',
    sa.Column('location_id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('city', mysql.VARCHAR(length=100), nullable=False),
    sa.PrimaryKeyConstraint('location_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('companycontacts',
    sa.Column('contact_id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('company_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=100), nullable=False),
    sa.Column('email', mysql.VARCHAR(length=100), nullable=True),
    sa.Column('phone_number', mysql.VARCHAR(length=20), nullable=True),
    sa.Column('position', mysql.VARCHAR(length=100), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['company.company_id'], name='companycontacts_ibfk_1'),
    sa.PrimaryKeyConstraint('contact_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('user')
    # ### end Alembic commands ###