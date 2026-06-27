import os
from app.extention import db
from app.services.upload_service import validate_resume_upload
from app.services.upload_service import save_resume
from app.services.upload_service import get_user_resumes
from app.services.upload_service import delete_resume

from flask import Blueprint, request, redirect, url_for, flash, current_app
from flask_login import login_required

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload', methods=['POST'])
@login_required
def upload_resume():
    try:
        if 'resume' not in request.files:
            flash('No file part', 'error')
            return redirect(url_for('dashboard.dashboard'))

        file = request.files['resume']
        is_valid, message = validate_resume_upload(file)

        if not is_valid:
            flash(message, 'error')
            return redirect(url_for('dashboard.dashboard'))

        upload_folder = current_app.config['UPLOAD_FOLDER']
        resume = save_resume(file, upload_folder)
        flash('Resume uploaded successfully!', 'success')

        from app.integration.file_extractor import Extractor
        text = None
        if resume.file_type == 'application/pdf':
            extractor = Extractor(resume.file_path)
            text = extractor.extract_pdf()
        elif resume.file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            extractor = Extractor(resume.file_path)
            text = extractor.extract_docx()

        if text:
            resume.raw_text = text
        
        from app.utils.text_cleaner import text_cleaner
        cleaned_text = text_cleaner(resume.raw_text)

        from app.services.parser_service import ParserService
        parser = ParserService(cleaned_text)
        resume.parsed_json = parser.parse_resume()
        db.session.commit() 
        
    except Exception as e:
        flash('An error occurred while uploading the resume.', 'error')
    return redirect(url_for('dashboard.dashboard'))
