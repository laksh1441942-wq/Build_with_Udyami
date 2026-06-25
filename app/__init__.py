from flask import Flask
from app.extention import db
from app.config import Config

def create_app():
    app = Flask(__name__,
                template_folder='templates',
                static_folder='static'
            )
    app.config.from_object(Config)
    db.init_app(app)
    
    from app.routes.auth_route import auth_bp
    app.register_blueprint(auth_bp)
    return app