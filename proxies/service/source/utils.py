from ipaddress import ip_address

from proxies.service.proxy import Proxy, ProxyProtocol


def parse_proxy(ip_adress: str, ip_port: str, protocol: ProxyProtocol) -> Proxy | None:
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

    return Proxy(address, port, protocol)
