from extensions import db

class Sources(db.Model):
    __tablename__ = 'SOURCES'

    sources_id = db.Column(db.String(20), primary_key=True)
    origin = db.Column(db.String(255), nullable=False)
    similarity = db.Column(db.Numeric(3,2), nullable=False)
    content_id_FK = db.Column(db.String(20), db.ForeignKey('CONTENTS.content_id'), nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
