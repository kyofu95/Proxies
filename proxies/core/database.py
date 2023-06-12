import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.exc import SQLAlchemyError

db = SQLAlchemy()
migrate = Migrate()


def init_database(app: Flask):
    """Initialize database and migrations."""

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        with db.engine.begin() as conn:
            try:
                result = conn.exec_driver_sql("select 1;")
                result.one()
            except SQLAlchemyError as exc:
                logging.exception("Database is not connected", exc_info=exc)
