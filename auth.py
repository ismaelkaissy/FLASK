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
        First_name = request.form['Firstname']
        Last_name = request.form['Lastname']
        username = First_name + Last_name
        password = request.form['Password']
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
            redirect(url_for('auth.login'))
        else:
            flash(error)
    else:
        return render_template('auth/signup.html') 

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        
        user =  User.query.filter_by(username=username).first()
        if user is None:
            error = 'Incorrect username'
        elif not check_password_hash(user['password'], password):
            error = 'Invalid password'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        else:
            flash(error)
    else:
        return render_template('auth/login.html')

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


