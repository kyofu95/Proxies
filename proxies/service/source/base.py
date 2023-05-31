from abc import ABC, abstractmethod
from typing import List

from proxies.service.proxy import Proxy


class ProxySourceError(Exception):
    pass


class IBaseProxySource(ABC):
    """An abstract base class for proxy sources, providing a get_proxies method to retrieve proxies."""

    @abstractmethod
    def get_proxies(self) -> List[Proxy] | None:
        """Get a list of proxies from the source."""
        raise NotImplementedError
