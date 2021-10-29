from extensions import db

class Users(db.Model):
    __tablename__ = 'USERS'

    eid = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    other_name = db.Column(db.String(30))
    email = db.Column(db.String(20), nullable=False, unique=True)
    phone = db.Column(db.String(30))
    organization = db.Column(db.String(30))

    tasks = db.relationship('TASKS', backref='user', cascade="all, delete",  passive_deletes=True)

    @classmethod
    def get_by_eid(cls, eid):
        return cls.query.filter_by(eid=eid).first()

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
