from flask import Blueprint, json, render_template, request, redirect, url_for, flash
from app.extention import db
from app.models.resume_model import ResumeModel


resume_bp = Blueprint('resume', __name__)

@resume_bp.route("/resume/<int:id>")
def view_resume(id):
    resume = ResumeModel.query.get_or_404(id)

    return render_template(
        "resume/view.html",
        raw_text=resume.raw_text,
        parsed_json=json.dumps(
            json.loads(resume.parsed_json),
            indent=4
        )
    )