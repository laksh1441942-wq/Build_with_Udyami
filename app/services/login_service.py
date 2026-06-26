from app.models.user_model import User
from app.extention import bcrypt

def authenticate_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return None
    if user and bcrypt.check_password_hash(user.password, password):
        return user

    return False