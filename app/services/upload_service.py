import os
import datetime

from flask import json
from app.models.resume_model import ResumeModel
from flask_login import current_user
from app.extention import db
from app.config import Config
from app.extention import ALLOWED_EXTENSIONS
from werkzeug.utils import secure_filename

MAX_CONTENT_LENGTH = Config.MAX_CONTENT_LENGTH

def validate_resume_upload(file):

    if not file or file.filename == '':
        return False, "No file selected for upload."
    
    if not file.filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS:
        return False, "Invalid file type. Only PDF and DOCX files are allowed."
    
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)

    if file_size > MAX_CONTENT_LENGTH:
        return False, "File size exceeds the maximum limit of 16MB."
    
    if file_size == 0:
        return False, "File is empty."
    return True, "File is valid for upload."

def save_resume_file(file, upload_folder):
    filename = secure_filename(file.filename)
    file_path = os.path.join(upload_folder, f"{current_user.id}_{filename}")
    os.makedirs(upload_folder, exist_ok=True)
    file.save(file_path)

def save_resume(file, upload_folder, raw_text, parsed_json):
    filename = secure_filename(file.filename)
    file_path = os.path.join(upload_folder, f"{current_user.id}_{filename}")

    resume = ResumeModel(
        user_id=current_user.id,
        filename=filename,
        file_path=file_path,
        file_type=file.content_type,
        file_size=len(file.read()),
        upload_time=datetime.datetime.now(),
        raw_text=str(raw_text),
        parsed_json=str(parsed_json)
    )
    db.session.add(resume)
    db.session.commit()
    return resume

def get_user_resumes():
    return ResumeModel.query.filter_by(user_id=current_user.id).all()

def delete_resume(resume_id):
    resume = ResumeModel.query.get(resume_id)
    if resume:
        if os.path.exists(resume.file_path):
            os.remove(resume.file_path)
        db.session.delete(resume)
        db.session.commit()
        return True
    return False