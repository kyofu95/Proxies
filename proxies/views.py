from datetime import datetime, timedelta
from typing import Any, Dict

from flask import Blueprint, render_template, request, jsonify
from flask_wtf.csrf import validate_csrf, generate_csrf
from wtforms.validators import ValidationError

from proxies.models import Proxy as DB_Proxy, Address as DB_Address
from proxies.service.proxy import ProxyProtocol
from proxies.forms import FilterForm

bp = Blueprint("index", __name__, "templates/")


def timedelta_format(td_object: timedelta) -> str:
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


def proxy_format(proxy: DB_Proxy) -> Dict[str, Any]:
    """Format the given proxy object into a dictionary."""

    return {
        "address": str(proxy.ip_address),
        "port": proxy.ip_port,
        "country": proxy.address.country,
        "protocol": proxy.protocol.name,
        "response": proxy.latency // 1000,
        "last_update": timedelta_format(datetime.utcnow() - proxy.health.last_tested),
    }


@bp.route("/filtered_data", methods=["POST"])
def filtered_data():
    """Route to filter ProxyDB table based on country and protocol, if provided."""

    # Get CSRF token from the form data and try to validate it
    csrf_token = request.form.get("csrf_token")
    try:
        validate_csrf(csrf_token)
    except ValidationError:
        return jsonify({"error": "Invalid CSRF token"}), 400

    # Create a FilterForm instance with the form data and validate it
    form = FilterForm(request.form)
    if form.validate():
        country = request.form.get("country")
        protocol = request.form.get("protocol")

        if protocol:
            protocol = ProxyProtocol(int(protocol))

        db_proxies = DB_Proxy.get_proxies_by_country_or_protocol(country, protocol, 50)

        # Convert the filtered results into a list of dictionaries
        items = [proxy_format(proxy) for proxy in db_proxies]

        return jsonify(items)
    return jsonify({"error": "Invalid input data"}), 400


@bp.route("/", methods=["GET"])
def index():
    """Renders the index.html template with a list of proxy servers."""

    form = FilterForm()
    token = generate_csrf()

    db_proxies = DB_Proxy.get_newest_proxies(50)

    db_coutries = DB_Address.get_countries()

    countries = [country[0] for country in db_coutries]

    items = [proxy_format(proxy) for proxy in db_proxies]

    return render_template("index.html", countries=countries, items=items, form=form, csrf_token=token)
