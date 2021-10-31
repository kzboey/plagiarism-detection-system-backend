from extensions import db

class Contents(db.Model):
    __tablename__ = 'CONTENTS'

    content_type = db.Column(db.String(50), nullable=False)
    content_id = db.Column(db.String(20), primary_key=True)
    content_value = db.Column(db.Text, nullable=False)
    position_x1 = db.Column(db.Float, nullable=False)
    position_x2 = db.Column(db.Float, nullable=False)
    position_y1 = db.Column(db.Float, nullable=False)
    position_y1 = db.Column(db.Float, nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    page_id_FK = db.Column(db.String(20), db.ForeignKey('PAGES.page_id', ondelete="CASCADE"), nullable=False)

    sources = db.relationship('Sources', backref='document', cascade="all, delete", passive_deletes=True)