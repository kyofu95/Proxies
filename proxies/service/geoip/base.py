from abc import ABC, abstractmethod
from ipaddress import IPv4Address, IPv6Address
from collections import namedtuple

from proxies.service.proxy import Proxy

Address = namedtuple("Address", ["country", "region", "city"])

class IBaseGeolocation(ABC):
    """Abstract base class for geolocation implementations."""

    @abstractmethod
    def get_address(self, ip_address: str | IPv4Address | IPv6Address) -> Address:
        """Get the address details for a given proxy."""
        raise NotImplementedError
