from app.extention import bcrypt
from flask import redirect, render_template, Blueprint, request, url_for
from flask_login import login_user
from app.services.login_service import authenticate_user
from app.services.register_service import register_user
from app.forms.auth_form import AuthForm, LoginForm


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def home():
    return render_template('home.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    try:
        user = None
        if form.validate_on_submit():
            user = authenticate_user(form.username.data, form.password.data)
            if user:
                login_user(user)
                return redirect(url_for('dashboard.dashboard')) 
    except Exception as e:
        print(e)  # Print any exceptions for debugging
    print(user)  # Print form errors for debugging
    return render_template('login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = AuthForm()
    try:
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data)
            register_user(form.username.data, form.email.data, hashed_password)
            return redirect(url_for('auth.login'))
    except Exception as e:
        print(e)  # Print any exceptions for debugging
    print(form.errors)  # Print form errors for debugging
    return render_template('register.html', form=form)

@auth_bp.route('/logout')
def logout():
    from flask_login import logout_user
    logout_user()
    return redirect(url_for('auth.login'))