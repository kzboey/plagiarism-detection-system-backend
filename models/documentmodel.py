from extensions import db

class Documents(db.Model):
    __tablename__ = 'DOCUMENTS'

    document_id = db.Column(db.String(20), primary_key=True)
    document_name = db.Column(db.String(255), nullable=False)
    document_path = db.Column(db.String(255), nullable=False)
    submission_id_FK = db.Column(db.String(20), db.ForeignKey('SUBMISSIONS.submission_id', ondelete="CASCADE"), nullable=False)

    @classmethod
    def get_documents_by_subid(cls, sub_id):
        # assume only one document, further document uploaded are merged into one
        return cls.query.filter_by(submission_id_FK=sub_id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

