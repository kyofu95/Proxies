from abc import ABC, abstractmethod

from proxies.service.address import Address
from proxies.service.proxy import Proxy


class IBaseGeolocation(ABC):
    @abstractmethod
    def get_address(self, proxy: Proxy) -> Address:
        raise NotImplementedError
