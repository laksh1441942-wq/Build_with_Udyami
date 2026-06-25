from flask import Flask

def create_app():
    app = Flask(__name__,
                template_folder='templates',
                static_folder='static'
            )
    from app.routes.auth_route import auth_bp
    app.register_blueprint(auth_bp)
    return app