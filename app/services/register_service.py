from app.models.user import User
from app.extention import db

def register_user(username, email, password):
    # Check if the username or email already exists
    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        return False  

    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return True  
