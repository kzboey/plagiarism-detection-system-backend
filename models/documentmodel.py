from extensions import db

class Documents(db.Model):
    __tablename__ = 'DOCUMENTS'

    document_id = db.Column(db.Integer, primary_key=True)
    document_name = db.Column(db.String(255), nullable=False)
    document_path = db.Column(db.String(255), nullable=False)
    submission_id_FK = db.Column(db.Integer, db.ForeignKey('SUBMISSIONS.submission_id', ondelete="CASCADE"), nullable=False)



