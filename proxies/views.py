from flask import Blueprint, render_template, request, jsonify
from flask_wtf.csrf import validate_csrf, generate_csrf
from wtforms.validators import ValidationError

from proxies.models import Proxy as DB_Proxy, Address as DB_Address
from proxies.service.proxy import ProxyProtocol
from proxies.forms import FilterForm
from proxies.utils.format import proxy_format

bp = Blueprint("index", __name__, "templates/")


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

    num_proxies = DB_Proxy.get_all_proxies_number()

    db_proxies = DB_Proxy.get_newest_proxies(50)

    db_countries = DB_Address.get_countries()

    items = [proxy_format(proxy) for proxy in db_proxies]

    return render_template(
        "index.html", num_proxies=num_proxies, countries=db_countries, items=items, form=form, csrf_token=token
    )
