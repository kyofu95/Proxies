from abc import ABC, abstractmethod
from collections import namedtuple
from ipaddress import IPv4Address, IPv6Address
from typing import List, Tuple

from proxies.models.proxy import ProxyProtocol

UncheckedProxyTuple = namedtuple("UncheckedProxy", ["address", "port", "protocol"])


class IBaseProxySource(ABC):
    """An abstract base class for proxy sources, providing a get_proxies method to retrieve proxies."""

    @abstractmethod
    def get_proxies(self) -> List[UncheckedProxyTuple] | None:
        """Get a list of proxies from the source."""
        raise NotImplementedError
