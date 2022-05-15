from extensions import db

class Submissions(db.Model):
    __tablename__ = 'SUBMISSIONS'

    submission_id = db.Column(db.String(20), primary_key=True)  #uuid
    author_name = db.Column(db.String(255), nullable=False)
    page = db.Column(db.Integer, nullable=False,default=0)
    # pages = db.column_property(db.query(Pages.page_id).count().where(submission_id == Pages.submission_id_FK))
    overall_similarity = db.Column(db.Numeric(3, 2),default=0)
    modified_date = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())
    task_id_FK = db.Column(db.Integer, db.ForeignKey('TASKS.task_id', ondelete="CASCADE"), nullable=False)

    documents = db.relationship('Documents', backref='submission', cascade="all, delete",  passive_deletes=True)
    pages = db.relationship('Pages', backref='submission', cascade="all, delete",  passive_deletes=True)

    @classmethod
    def get_task_submissions(cls, task_id):
        return cls.query.filter_by(task_id_FK=task_id).order_by(Submissions.modified_date.desc()).all()

    @classmethod
    def get_submission_by_author(cls, author, task_id):
        return cls.query.filter_by(author_name=author, task_id_FK=task_id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
