from flask import Flask
from flask_wtf.csrf import CSRFProtect

from proxies.core.config import settings
from proxies.core.database import init_database
from proxies.core.scheduler import init_scheduler

from proxies.views import bp as index_bp

from proxies.tasks.tasks import register_tasks


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.DATABASE_URI
    app.config["SECRET_KEY"] = settings.SECRET_KEY

    init_database(app)
    init_scheduler(app)
    csrf = CSRFProtect(app)

    app.register_blueprint(index_bp)

    app.app_context().push()

    register_tasks()

    return app
