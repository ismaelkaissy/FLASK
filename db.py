
import click
from flask import current_app, g
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy



def get_db():
    if 'db' not in g:
        g.db = SQLAlchemy()
        current_app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:C0d3rSkad@localhost/vision'
        current_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
