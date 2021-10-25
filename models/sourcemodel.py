from extensions import db

class Documents(db.Model):
    __tablename__ = 'SOURCES'

    sources_id = db.Column(db.Integer, primary_key=True)
    content_id_FK = db.Column(db.Integer, db.ForeignKey('CONTENTS.content_id'), nullable=False)
    origin = db.Column(db.String(255), nullable=False)
    similarity = db.Column(db.Numeric(3,2), nullable=False)