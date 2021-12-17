from extensions import db


class Users(db.Model):
    __tablename__ = 'USERS'

    eid = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    other_name = db.Column(db.String(50), default='')
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone = db.Column(db.String(30), default='')
    organization = db.Column(db.String(30), default='')
    right = db.Column(db.String(50), nullable=False)

    tasks = db.relationship('Tasks', backref='user', cascade="all, delete",  passive_deletes=True)

    @classmethod
    def get_by_eid(cls, eid):
        return cls.query.filter_by(eid=eid).first()

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
