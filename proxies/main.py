import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, Blueprint
from flask_wtf.csrf import CSRFProtect
from flask_restx import Api

from proxies.core.config import settings
from proxies.core.database import init_database
from proxies.core.scheduler import init_scheduler

from proxies.views.index import bp as index_bp

from proxies.api.proxies import ns

from proxies.service.tasks.tasks import register_tasks


def setup_logging(app: Flask):
    if settings.GUNICORN:
        gunicorn_logger = logging.getLogger("gunicorn.error")
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)
    else:
        logging.basicConfig(
            handlers=[RotatingFileHandler("flask.log", maxBytes=100000, backupCount=10)],
            level=logging.DEBUG,
            format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S",
        )

    # this line removes logging about EVERY proxy check
    logging.getLogger("urllib3").setLevel(logging.WARNING)


def create_app() -> Flask:
    """Application factory."""

    app = Flask(__name__)
    root_blueprint = Blueprint("api", __name__, url_prefix="/api")
    api = Api(root_blueprint, doc="/docs/")

    setup_logging(app)

    app.register_blueprint(root_blueprint)

    app.logger.info("App start")

    app.config["SQLALCHEMY_DATABASE_URI"] = settings.DATABASE_URI
    app.config["SECRET_KEY"] = settings.SECRET_KEY

    init_database(app)
    init_scheduler(app)
    csrf = CSRFProtect(app)

    app.register_blueprint(index_bp)

    api.add_namespace(ns)

    app.app_context().push()

    if settings.ENVIRONMENT != "testing":
        register_tasks()

    return app
