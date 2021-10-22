from extensions import db

class Users(db.Model):
    __tablename__ = 'USERS'

    eid = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    tasks = db.relationship('TASKS', backref='user', lazy=True)