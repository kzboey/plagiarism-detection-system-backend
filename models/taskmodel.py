from extensions import db

class Tasks(db.Model):
    __tablename__ = 'TASKS'

    task_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.String(20), nullable=False)
    course_title = db.Column(db.String(50), nullable=False)
    task_name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.DateTime(), nullable=False)
    due_date = db.Column(db.DateTime(), nullable=False)
    modified_date = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())
    eid_fk	= db.Column(db.String(20), db.ForeignKey('USERS.eid'), nullable=False)