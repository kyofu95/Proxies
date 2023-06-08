from abc import ABC, abstractmethod

from proxies.service.address import Address
from proxies.service.proxy import Proxy


class IBaseGeolocation(ABC):
    """Abstract base class for geolocation implementations."""

    @abstractmethod
    def get_address(self, proxy: Proxy) -> Address:
        """Get the address details for a given proxy."""
        raise NotImplementedError
