
import click
from flask import current_app, g
from flask.cli import with_appcontext
from .models import *


def get_db():
    if 'db' not in g:
        g.db = db
        current_app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:C0d3rSkad@localhost/vision'
        current_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.session.close()

def init_db():
    db = get_db()
    db.init_app(current_app)
    db.create_all()

@click.command('init-db')
@with_appcontext
def init_db_command():
    "Clear the existing data and create new tables"
    init_db()
    click.echo('initialized the datatbase.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)