from extensions import db

class Documents(db.Model):
    __tablename__ = 'CONTENTS'

    content_type = db.Column(db.String(50), nullable=False)
    content_id = db.Column(db.Integer, primary_key=True)
    content_value = db.Column(db.Text, nullable=False)
    position_x1 = db.Column(db.SmallInteger, nullable=False)
    position_x2 = db.Column(db.SmallInteger, nullable=False)
    position_y1 = db.Column(db.SmallInteger, nullable=False)
    position_y1 = db.Column(db.SmallInteger, nullable=False)
    confidence = db.Column(db.SmallInteger, nullable=False)
    page_id_FK = db.Column(db.Integer, db.ForeignKey('SOURCES.sources_id'), nullable=False)

    sources = db.relationship('SOURCES', backref='document')