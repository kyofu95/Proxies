from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def init_database(app: Flask):
    """Initialize database and migrations."""

    db.init_app(app)
    migrate.init_app(app, db)
