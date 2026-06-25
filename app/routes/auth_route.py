from flask import render_template, Blueprint, request
from app.services.register_service import register_user


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def home():
    return render_template('home.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        success = register_user(username, email, password)
        
        if success:
            return "User registered successfully!"
        else:
            return "Username or email already exists."