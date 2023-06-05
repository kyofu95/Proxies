from datetime import datetime, timedelta

from flask import Blueprint, render_template, request, jsonify

from proxies.models import Proxy as DB_Proxy, Health as DB_Health, Address as DB_Address
from proxies.core.database import db
from proxies.service.proxy import ProxyProtocol

bp = Blueprint("index", __name__, "templates/")


def td_format(td_object: timedelta) -> str:
    """
    Convert a timedelta object to a string representing the duration
    in years, months, days, hours, minutes, and seconds.
    """

    seconds = int(td_object.total_seconds())
    PERIODS = [
        ("year", 60 * 60 * 24 * 365),
        ("month", 60 * 60 * 24 * 30),
        ("day", 60 * 60 * 24),
        ("hour", 60 * 60),
        ("minute", 60),
        ("second", 1),
    ]

    strings = []
    for period_name, period_seconds in PERIODS:
        if seconds >= period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            has_s = "s" if period_value > 1 else ""
            strings.append(f"{period_value} {period_name}{has_s}")

    return ", ".join(strings)


@bp.route("/filtered_data", methods=["POST"])
def filtered_data():
    country = request.form.get("country")
    protocol = request.form.get("protocol")

    statement = db.select(DB_Proxy).join(DB_Proxy.address).join(DB_Proxy.health)
    if country:
        statement = statement.filter(DB_Address.country == country)
    if protocol:
        protocol = ProxyProtocol(int(protocol))
        statement = statement.filter(DB_Proxy.protocol == protocol)

    statement = statement.order_by(DB_Health.last_tested.desc()).limit(50)

    db_proxies = db.session.execute(statement).scalars().all()

    items = []
    for proxy in db_proxies:
        proxy_dict = {
            "address": str(proxy.ip_address),
            "port": proxy.ip_port,
            "country": proxy.address.country,
            "protocol": proxy.protocol.name,
            "response": proxy.latency,
            "last_update": td_format(datetime.utcnow() - proxy.health.last_tested),
        }
        items.append(proxy_dict)

    return jsonify(items)


@bp.route("/", methods=["GET", "POST"])
def index():
    """Renders the index.html template with a list of proxy servers."""

    db_proxies = (
        db.session.execute(db.select(DB_Proxy).join(DB_Proxy.health).order_by(DB_Health.last_tested.desc()).limit(50))
        .scalars()
        .all()
    )

    db_coutries = (
        db.session.execute(db.select(DB_Address.country).distinct().order_by(DB_Address.country.asc()))
        .columns("country")
        .all()
    )

    countries = []
    for country in db_coutries:
        country_name = country[0]
        countries.append(country_name)

    items = []
    for proxy in db_proxies:
        proxy_dict = {
            "address": str(proxy.ip_address),
            "port": proxy.ip_port,
            "country": proxy.address.country,
            "protocol": proxy.protocol.name,
            "response": proxy.latency,
            "last_update": td_format(datetime.utcnow() - proxy.health.last_tested),
        }
        items.append(proxy_dict)

    return render_template("index.html", countries=countries, items=items)
