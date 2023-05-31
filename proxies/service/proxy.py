from dataclasses import dataclass
from enum import Enum
from ipaddress import IPv4Address, IPv6Address
from typing import Optional

IPAddress = IPv4Address | IPv6Address


class ProxyProtocol(Enum):
    """
    Enum representing different proxy protocols:
    SOCKS4, SOCKS5, HTTP, and HTTPS (also known as SSL).
    """

    SOCKS4 = 1
    SOCKS5 = 2
    HTTP = 3
    HTTPS = 4


@dataclass
class Proxy:
    """A data class representing a proxy."""

    ip_address: IPAddress
    ip_port: int
    protocol: ProxyProtocol
    login: Optional[str] = None
    password: Optional[str] = None
