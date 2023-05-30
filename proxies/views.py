from flask import Blueprint, render_template

from proxies.core.database import db

bp = Blueprint("index", __name__, "templates/")


@bp.route("/", methods=["GET"])
def index():
    db.paginate()
    return render_template("index.html")
