from extensions import db

class Pages(db.Model):
    __tablename__ = 'PAGES'

    page_id = db.Column(db.String(20), primary_key=True)
    page_name = db.Column(db.String(255), nullable=False)
    page_path = db.Column(db.String(255), nullable=False)
    submission_id_FK = db.Column(db.String(20), db.ForeignKey('SUBMISSIONS.submission_id', ondelete="CASCADE"), nullable=False)

    contents = db.relationship('Contents', backref='pages', cascade="all, delete", passive_deletes=True)