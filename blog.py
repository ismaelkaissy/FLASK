from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.exceptions import abort

from .db import get_db

from .models import User, POST

from .auth import login_required

from datetime import datetime

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    posts = POST.query.order_by('date').all()
    return render_template('index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        db = get_db()
        title = request.form['title']
        content = request.form['content']
        date = datetime.now()
        user_id = g.user.id
        post = POST(user_id=user_id, title=title, content=content, date=date)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html')

def get_post(id, check_author=True):
    post = POST.query.filter_by(id=id).first_or_404()
    if post.user_id != g.user.id:
        abort(403)
    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        date = datetime.now()
        error = None

        if not title:
            error = 'Title is required'
        elif not content:
            error = 'Content is required'
        
        if error:
            flash(error)
        else:
            post.title = title
            post.content = content
            post.date = date
            db = get_db()
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    post = get_post(id)
    db = get_db()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('index'))

@bp.route('/profile', methods=('GET',))
@login_required
def profile():
    user = g.user
    firstname = user.First_name
    lastname = user.Last_name
    email = user.email
    posts = user.posts
    return render_template('profile.html', firstname=firstname, lastname=lastname, email=email, posts=posts)