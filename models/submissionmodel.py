from extensions import db
from models.pagemodel import Pages


class Submissions(db.Model):
    __tablename__ = 'SUBMISSIONS'

    submission_id = db.Column(db.String(20), primary_key=True)  #uuid
    author_name = db.Column(db.String(255), nullable=False)
    pages = db.Column(db.Integer, nullable=False,default=0)
    # pages = db.column_property(db.query(Pages.page_id).count().where(submission_id == Pages.submission_id_FK))
    overall_similarity = db.Column(db.Numeric(3, 2))
    modified_date = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())
    task_id_FK = db.Column(db.Integer, db.ForeignKey('TASKS.task_id', ondelete="CASCADE"), nullable=False)

    documents = db.relationship('Documents', backref='submission', cascade="all, delete",  passive_deletes=True)
    pages = db.relationship('Pages', backref='submission', cascade="all, delete",  passive_deletes=True)
