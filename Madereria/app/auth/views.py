from app.models import UserData
from app.forms import LoginForm
from flask import render_template, redirect, flash, url_for, session
from flask_login import login_user, login_required, logout_user, current_user
from . import auth
from app.firestore_service import get_user, user_put
from app.models import UserModel, UserData
from werkzeug.security import generate_password_hash, check_password_hash
from flask import abort
from functools import wraps

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    login_form = LoginForm()
    context = {
        'login_form': LoginForm()
    }

    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data

        user_document = get_user(username)

        if user_document.to_dict() is not None:
            #password_from_db = user_document.to_dict()['password']
            if check_password_hash(user_document.to_dict()['password'], password):
                is_admin = user_document.to_dict()['admin']
                user_data = UserData(username, password, is_admin)
                user = UserModel(user_data)

                login_user(user)
                flash(f'Bienvenido de nuevo {current_user.id}')
                redirect(url_for('hello'))

            else:
                flash('La informacion no coincide')

        else:
            flash('El usuario no existe')

        return redirect(url_for('index'))

    return render_template('login.html', **context)

@auth.route('logout')
@login_required
def logout ():
    logout_user()
    flash('Vuelve pronto...')

    return redirect(url_for('auth.login'))

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        is_admin = getattr(current_user, 'is_admin', False)
        if not is_admin:
            abort(401)
        return f(*args, **kws)
    return decorated_function
