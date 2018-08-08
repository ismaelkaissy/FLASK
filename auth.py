import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db

from .models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        First_name = request.form['firstname']
        Last_name = request.form['lastname']
        username = First_name + Last_name
        password = request.form['password']
        email = request.form['email']
        db = get_db()
        error = None
        
        if not First_name:
            error = 'First name is required'
        elif not Last_name:
            error = 'Last name is required'
        elif not password:
            error = 'Password is required'
        elif User.query.filter_by(username=username).first() is not None:
            error = 'User {} is already registered.'.format(username)
        
        if error is None:
            user = User(First_name=First_name, Last_name=Last_name, username=username, password=generate_password_hash(password), email=email)
            db.session.add(user)
            db.session.commit()
            redirect(url_for('index'))
        else:
            flash(error)
    
    return render_template('signup.html') 

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        
        user_by_username =  User.query.filter_by(username=username).first()
        user_by_email = User.query.filter_by(email=username).first()

        if user_by_username is None and user_by_email is None:
            error = 'Incorrect username'
        else:
            user = user_by_username if user_by_username else user_by_email
            if not check_password_hash(user.password, password):
                error = 'Invalid password'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            flash(error)    
    return render_template('login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

