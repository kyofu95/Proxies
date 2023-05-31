from typing import List
import requests

from proxies.service.proxy import Proxy, ProxyProtocol
from proxies.service.source.base import IBaseProxySource, ProxySourceError
from proxies.service.source.utils import parse_proxy


class BaseGithubProxySource(IBaseProxySource):
    def make_request(self, uri: str) -> requests.Response:
        try:
            response = requests.get(uri, timeout=10)
        except requests.exceptions.Timeout as exc:
            raise ProxySourceError("Timeout!") from exc
        except requests.exceptions.RequestException as exc:
            raise ProxySourceError(str(exc)) from exc

        if not response.ok:
            raise ProxySourceError(f"Response status is {response.status_code}")

        return response


class TheSpeedXProxySource(BaseGithubProxySource):
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

        proxies = [Proxy]

        for proxy_type in self.PROTOCOL_LIST:
            proxies_url = self.base_url + proxy_type[1]

            response = self.make_request(proxies_url)

            # Parse text contents
            for line in response.text.split("\n"):
                address, port = line.split(":")

                proxy = parse_proxy(address, port, proxy_type[0])
                if proxy:
                    proxies.append(proxy)

        return proxies


class JetkaiProxySource(BaseGithubProxySource):
    """
    A class representing jetkai proxy source,
    which fetches proxies from https://github.com/jetkai/proxy-list.
    """

    base_url = "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/json/proxies-basic.json"

    def get_proxies(self) -> List[Proxy] | None:
        """Get a list of proxies from the source."""

        proxies = [Proxy]

        response = self.make_request(self.base_url)

        raw_proxy_list = response.json()
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
