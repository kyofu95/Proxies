from datetime import datetime, timedelta

from flask import Blueprint, render_template

from proxies.models import Proxy as DB_Proxy, Health as DB_Health
from proxies.core.database import db

bp = Blueprint("index", __name__, "templates/")


def td_format(td_object: timedelta) -> str:
    """
    Convert a timedelta object to a string representing the duration
    in years, months, days, hours, minutes, and seconds.
    """

    seconds = int(td_object.total_seconds())
    periods = [
        ("year", 60 * 60 * 24 * 365),
        ("month", 60 * 60 * 24 * 30),
        ("day", 60 * 60 * 24),
        ("hour", 60 * 60),
        ("minute", 60),
        ("second", 1),
    ]

    strings = []
    for period_name, period_seconds in periods:
        if seconds >= period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            has_s = "s" if period_value > 1 else ""
            strings.append(f"{period_value} {period_name}{has_s}")

    return ", ".join(strings)


@bp.route("/", methods=["GET"])
def index():
    """Renders the index.html template with a list of proxy servers."""

    db_proxies = (
        db.session.execute(db.select(DB_Proxy).join(DB_Proxy.health).order_by(DB_Health.last_tested.desc()).limit(20))
        .scalars()
        .all()
    )

    items = []
    for proxy in db_proxies:
        proxy_dict = {
            "address": str(proxy.ip_address),
            "port": proxy.ip_port,
            "country": proxy.address.country,
            "protocol": proxy.protocol.name.lower(),
            "response": proxy.latency,
            "last_update": td_format(datetime.utcnow() - proxy.health.last_tested),
        }
        items.append(proxy_dict)

    return render_template("index.html", items=items)
