from typing import List

from proxies.service.source.base import IBaseProxySource
from proxies.service.source.github import JetkaiProxySource, TheSpeedXProxySource


class ProxySourceManager:
    """A class to manage instances of proxy sources."""

    def __init__(self) -> None:
        """Initialize the ProxySourceManager with an empty list of instances."""
        self.instances = []

    def add_instance(self, source: IBaseProxySource) -> None:
        """Add a proxy source instance to the list of instances."""
        self.instances.append(source)

    def get_instances(self) -> List[IBaseProxySource]:
        """Get the list of proxy source instances."""
        return self.instances


proxy_source_manager = ProxySourceManager()


proxy_source_manager.add_instance(TheSpeedXProxySource())
proxy_source_manager.add_instance(JetkaiProxySource())
