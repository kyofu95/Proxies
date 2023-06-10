from typing import List
import json

from proxies.service.proxy import Proxy, ProxyProtocol
from proxies.service.source.base import IBaseProxySource
from proxies.service.source.utils import parse_proxy
from proxies.utils.network import make_request


class TheSpeedXProxySource(IBaseProxySource):
    """
    A class representing TheSpeedX proxy source,
    which fetches proxies from https://github.com/TheSpeedX/PROXY-List.
    """

    base_url = "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/"

    PROTOCOL_LIST = [
        (ProxyProtocol.SOCKS4, "socks4.txt"),
        (ProxyProtocol.SOCKS5, "socks5.txt"),
    ]

    def get_proxies(self) -> List[Proxy] | None:
        """Get a list of proxies from the source."""

        proxies = []

        for proxy_type in self.PROTOCOL_LIST:
            proxies_url = self.base_url + proxy_type[1]

            text_response = make_request(proxies_url)
            if not text_response:
                continue

            # Parse text contents
            for line in text_response.split("\n"):
                address, port = line.split(":")

                proxy = parse_proxy(address, port, proxy_type[0])
                if proxy:
                    proxies.append(proxy)

        return proxies


class JetkaiProxySource(IBaseProxySource):
    """
    A class representing jetkai proxy source,
    which fetches proxies from https://github.com/jetkai/proxy-list.
    """

    base_url = "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/json/proxies-basic.json"

    def get_proxies(self) -> List[Proxy] | None:
        """Get a list of proxies from the source."""

        proxies = []

        text_response = make_request(self.base_url)
        if not text_response:
            return None

        raw_proxy_list = json.loads(text_response)
        for raw_proxy in raw_proxy_list:
            raw_address = raw_proxy["ip"]
            for raw_protocol in raw_proxy["protocols"]:
                raw_port = raw_protocol["port"]
                raw_type = raw_protocol["type"]

                # convert proxy protocol
                proxy_protocol = ProxyProtocol[raw_type.upper()]

                proxy = parse_proxy(raw_address, raw_port, proxy_protocol)
                if proxy:
                    proxies.append(proxy)

        return proxies
