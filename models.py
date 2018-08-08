from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    First_name = db.Column(db.String(20), nullable=False)
    Last_name = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(60), nullable=False)
    posts =  db.relationship('POST', backref='users', lazy='dynamic')

class POST(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

