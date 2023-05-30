from flask import Flask

from proxies.core.database import init_database
from proxies.core.config import settings


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.DATABASE_URI
    print(app.config["SQLALCHEMY_DATABASE_URI"])

    init_database(app)

    return app
