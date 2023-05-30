from flask import Flask, Blueprint, render_template, flash

from proxies.core.database import init_database
from proxies.core.config import settings

from proxies.views import bp as index_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.DATABASE_URI
    app.config["SECRET_KEY"] = settings.SECRET_KEY

    init_database(app)

    app.register_blueprint(index_bp)

    return app

