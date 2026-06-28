from app.extention import db

class ResumeModel(db.Model):
    __tablename__ = "resumes"

    resume_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(255))
    file_path = db.Column(db.String(255))
    file_type = db.Column(db.String)
    file_size = db.Column(db.Integer)
    upload_time = db.Column(db.DateTime, default=db.func.current_timestamp())
    raw_text = db.Column(db.Text)
    parsed_json = db.Column(db.Text)

    user = db.relationship('User', back_populates='resumes')
