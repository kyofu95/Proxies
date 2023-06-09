from ipaddress import ip_address
import pytest
from proxies.service.source.utils import parse_proxy, Proxy, ProxyProtocol


@pytest.mark.parametrize(
    "ip_adress, ip_port, protocol, expected_output",
    [
        ("34.0.0.1", "8080", ProxyProtocol.HTTP, Proxy(ip_address("34.0.0.1"), 8080, ProxyProtocol.HTTP)),
        ("34.0.0.1", "80000", ProxyProtocol.HTTP, None),
        (
            "2a01:8640:2:11::674b:ad6d",
            "8080",
            ProxyProtocol.SOCKS5,
            Proxy(ip_address("2a01:8640:2:11::674b:ad6d"), 8080, ProxyProtocol.SOCKS5),
        ),
        ("192.168.1.1", "0", ProxyProtocol.HTTP, None),
        ("192.168.1.1", "65536", ProxyProtocol.HTTP, None),
        ("0.0.0.0", "8080", ProxyProtocol.HTTP, None),
    ],
)
def test_parse_proxy(ip_adress, ip_port, protocol, expected_output):
    result = parse_proxy(ip_adress, ip_port, protocol)
    assert result == expected_output
