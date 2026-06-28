from flask import Blueprint, json, jsonify, render_template
from app.extention import db
from app.models.resume_model import ResumeModel
from flask_login import current_user, login_required


resume_bp = Blueprint('resume', __name__)

@resume_bp.route("/api/resume/<int:resume_id>")

@login_required

def get_resume(resume_id):

    resume = ResumeModel.query.filter_by(

        resume_id=resume_id,

        user_id=current_user.id

    ).first_or_404()

    return jsonify({

        "raw_text": resume.raw_text,

        "parsed_json": json.loads(resume.parsed_json)

        if resume.parsed_json else None

    })

@resume_bp.route("/resume/<int:resume_id>")
@login_required
def view_resume(resume_id):
    return render_template("view.html", resume_id=resume_id)