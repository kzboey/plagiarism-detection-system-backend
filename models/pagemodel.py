from extensions import db

class Pages(db.Model):
    __tablename__ = 'PAGES'

    page_id = db.Column(db.String(20), primary_key=True)
    page_name = db.Column(db.String(255), nullable=False)
    page_path = db.Column(db.String(255), nullable=False)
    submission_id_FK = db.Column(db.String(20), db.ForeignKey('SUBMISSIONS.submission_id', ondelete="CASCADE"), nullable=False)

    contents = db.relationship('Contents', backref='pages', cascade="all, delete", passive_deletes=True)

    @classmethod
    def get_pages_by_subid(cls, sub_id):
        return cls.query.filter_by(submission_id_FK=sub_id).all()

    @classmethod
    def get_pages_by_pid(cls, pid):
        return cls.query.filter_by(page_id=pid).first()

    @classmethod
    def get_pages_list_by_pid(cls, pids):
        lists = []
        for pid in pids:
            lists.append( cls.query.filter_by(page_id=pid).first())
        return lists

    @classmethod
    def delete_list(cls, sub_id_fk):
        cls.query.filter_by(submission_id_FK=sub_id_fk).delete()
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
