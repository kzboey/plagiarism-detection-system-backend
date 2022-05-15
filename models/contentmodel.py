from extensions import db
from models.sourcemodel import Sources
from models.pagemodel import Pages
from models.submissionmodel import Submissions
from sqlalchemy import or_, and_

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
    def get_content_by_pid(cls, pids, eqnValue, sentenceValue):
        lists = [db.session.query(Contents.content_id, Contents.content_type, Contents.content_value, Contents.position_x1, Contents.position_x2, Contents.position_y1, Contents.position_y2, Contents.confidence, Contents.page_id_FK, Sources.sources_id, Sources.similarity, Sources.origin)\
            .filter(Contents.content_id==Sources.content_id_FK, Contents.page_id_FK==pid) \
            .filter(or_(and_(Contents.content_type == "equation", Sources.similarity >= eqnValue), and_(Contents.content_type == "sentence", Sources.similarity >= sentenceValue)))
            .order_by(Contents.position_y1.asc()).all() for pid in pids]
        return lists

    @classmethod
    def get_content_by_cids(cls, cids):
        lists = [db.session.query(Contents.content_id, Contents.content_type, Contents.content_value, Contents.position_x1,
                Contents.position_x2, Contents.position_y1, Contents.position_y2, Contents.confidence,
                Contents.page_id_FK, Pages.page_name).filter(Contents.content_id == cid, Contents.page_id_FK == Pages.page_id).all() for cid in cids]
        return lists

    @classmethod
    def get_content_by_task_and_name(cls, task_id, name):
        return db.session.query(Contents).filter(Contents.page_id_FK.in_(db.session.query(Pages.page_id).filter(Pages.submission_id_FK.in_(db.session.query(Submissions.submission_id).filter(Submissions.author_name == name, Submissions.task_id_FK == task_id))))).count()

    @classmethod
    def get_matched_content(cls, task_id, name):
        return db.session.query(Contents).filter(Contents.page_id_FK.in_(db.session.query(Pages.page_id).filter(
            Pages.submission_id_FK.in_(
                db.session.query(Submissions.submission_id).filter(Submissions.author_name == name,
                                                                   Submissions.task_id_FK == task_id)))), Contents.content_id == Sources.content_id_FK, Contents.confidence > 0.6).count()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
