from app.models.user import User

def authenticate_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        return True
    return False