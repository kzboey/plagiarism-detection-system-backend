from extensions import db
from pagemodel import Pages


class Submissions(db.Model):
    __tablename__ = 'SUBMISSIONS'

    submission_id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String(255), nullable=False)
    # pages = db.Column(db.Integer, nullable=False)
    pages = db.column_property(db.query(Pages.page_id).count().where(submission_id == Pages.submission_id_FK))
    overall_similarity = db.Column(db.Numeric(3, 2))
    modified_date = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())
    task_id_FK = db.Column(db.Integer, db.ForeignKey('TASKS.task_id'), nullable=False)

    documents = db.relationship('DOCUMENTS', backref='submission')
    pages = db.relationship('PAGES', backref='submission')
