import os
from flask import Flask
from app.extention import db, bcrypt, login_manager
from app.config import Config
from app.models.user_model import User
from app.models.resume_model import ResumeModel

def create_app():
    app = Flask(__name__,
                template_folder='templates',
                static_folder='static'
            )
    
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    login_manager.login_view = 'auth.login'

    @login_manager.user_loader

    def load_user(user_id):

        return User.query.get(int(user_id))

    from app.routes.auth_route import auth_bp

    app.register_blueprint(auth_bp)

    from app.routes.dashboard import dashboard_bp

    app.register_blueprint(dashboard_bp)

    from app.routes.upload import upload_bp

    app.register_blueprint(upload_bp)

    with app.app_context():
        db.create_all()
    return app
