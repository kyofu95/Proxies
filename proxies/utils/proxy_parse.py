from ipaddress import ip_address
from proxies.service.source.base import UncheckedProxyTuple

from proxies.models.proxy import ProxyProtocol


def parse_proxy(ip_adress: str, ip_port: str, protocol: ProxyProtocol | str) -> UncheckedProxyTuple | None:
    """Parse and validate a proxy address."""

    # Convert and (partially) validate address and port
    try:
        address = ip_address(ip_adress)
        port = int(ip_port)
    except ValueError:
        return None

    # skip reserved adresses
    if address.is_reserved or address.is_private:
        return None

    # check ip port
    if not (1 <= port <= 65535):
        return None

    if isinstance(protocol, str):
        protocol = protocol.upper()

        if protocol not in [p.name for p in ProxyProtocol]:
            return None

        protocol = ProxyProtocol[protocol]
    elif isinstance(protocol, ProxyProtocol):
        pass
    else:
        return None

    return UncheckedProxyTuple(address, port, protocol)
