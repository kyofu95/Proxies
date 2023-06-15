from ipaddress import IPv4Address, IPv6Address

from flask_restx import fields, Namespace, Resource, reqparse

from proxies.models.repositories.proxy_repository import ProxyRepository, ProxyProtocol

ns = Namespace(
    "api",
    path="/",
)

proxy_rep = ProxyRepository()


class IpAddressField(fields.Raw):
    """Custom flask-restx Field for ipaddress package types."""

    def format(self, value: str | IPv4Address | IPv6Address) -> str:
        """Convert value into string."""

        return str(value)


proxy_scheme = ns.model(
    "Proxy",
    {
        "address": IpAddressField(attribute="ip_address"),
        "port": fields.Integer(attribute="ip_port"),
        "protocol": fields.String(attribute="protocol.name", enum=[p.name for p in ProxyProtocol]),
        "country": fields.String(attribute="address.country"),
        "last_checked": fields.DateTime(attribute="health.last_tested"),
    },
)


parser = reqparse.RequestParser()
parser.add_argument("country", type=str, location="args", help="Country of proxy")
parser.add_argument(
    "protocol", type=str, choices=[p.name for p in ProxyProtocol], location="args", help="Proxy protocol"
)
parser.add_argument("limit", type=int, default=20, location="args", help="Limit list")


@ns.route("/proxies")
class Proxy(Resource):
    """Router class for Proxy."""

    @ns.expect(parser)
    @ns.doc(responses={400: "Bad request"})
    @ns.marshal_list_with(proxy_scheme, code=200)
    def get(self):
        """Returns list of proxies."""

        args = parser.parse_args()

        country = args["country"]

        protocol = None
        if args["protocol"]:
            protocol = ProxyProtocol[args["protocol"]]

        limit = args["limit"]

        proxies = proxy_rep.get_proxies_by_country_or_protocol(country, protocol, limit)
        return proxies
