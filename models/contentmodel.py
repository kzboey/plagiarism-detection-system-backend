from extensions import db
from models.sourcemodel import Sources

class Contents(db.Model):
    __tablename__ = 'CONTENTS'

    content_type = db.Column(db.String(50), nullable=False)
    content_id = db.Column(db.String(20), primary_key=True)
    content_value = db.Column(db.Text, nullable=False)
    position_x1 = db.Column(db.Float, nullable=False)
    position_x2 = db.Column(db.Float, nullable=False)
    position_y1 = db.Column(db.Float, nullable=False)
    position_y2 = db.Column(db.Float, nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    page_id_FK = db.Column(db.String(20), db.ForeignKey('PAGES.page_id', ondelete="CASCADE"), nullable=False)

    sources = db.relationship('Sources', backref='document', cascade="all, delete", passive_deletes=True)

    @classmethod
    def get_content_by_pid(cls, pids):
        # lists = db.session.query(Contents).all()
        lists = [db.session.query(Contents.content_id, Contents.content_type, Contents.content_value, Contents.position_x1, Contents.position_x2, Contents.position_y1, Contents.position_y2, Contents.confidence, Contents.page_id_FK, Sources.sources_id, Sources.similarity, Sources.origin)\
            .filter(Contents.content_id==Sources.content_id_FK)\
            .filter(Contents.page_id_FK==pid).all() for pid in pids]
        return lists

    @classmethod
    def get_content_by_pid2(cls, pid):
        lists = db.session.query(Contents.content_id, Contents.content_type, Contents.content_value, Contents.position_x1, Contents.position_x2, Contents.position_y1, Contents.position_y2, Contents.confidence)\
            .filter(Contents.page_id_FK==pid, Contents.content_id==Sources.content_id_FK).all()
        return lists

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
