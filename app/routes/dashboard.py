from flask import render_template, Blueprint

from app.services.upload_service import get_user_resumes

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    resumes = get_user_resumes()
    print(resumes)  # Debugging line to check the resumes fetched
    return render_template('dashboard.html', resumes=resumes, )   