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


@dataclass(init=True, unsafe_hash=True)
class Proxy:
    """A data class representing a proxy."""

    ip_address: IPAddress
    ip_port: int
    protocol: ProxyProtocol

    latency: Optional[int] = None

    def get_uri(self) -> str:
        """Returns a string representing a proxy URI."""

        protocol_name = self.protocol.name.lower()
        return f"{protocol_name}://{self.ip_address}:{self.ip_port}"
