from typing import Dict
from collections import namedtuple
import logging

import requests

RequestResult = namedtuple("RequestResult", ["success", "latency"])


def make_request(uri: str) -> str | None:
    """Send an HTTP GET request to the specified URI and return the response text."""

    try:
        response = requests.get(uri, timeout=10)
    except (requests.exceptions.Timeout, requests.exceptions.RequestException) as exc:
        logging.error("Http request failed", exc_info=exc)
        return None

    if not response.ok:
        logging.error("Http request returned HTTP %s, {%s}", response.status_code, response)
        return None

    return response.text


def is_proxy_active(uri: str, proxy_dict: Dict[str, str], timeout: int) -> RequestResult:
    """Check if the proxy is active by attempting a connection."""

    try:
        response = requests.get(uri, proxies=proxy_dict, timeout=timeout)
    except (requests.exceptions.Timeout, requests.exceptions.ProxyError, requests.exceptions.ConnectionError):
        return RequestResult(False, 0)
    except requests.exceptions.RequestException as exc:
        logging.debug("proxy checking exception", exc_info=exc)
        return RequestResult(False, 0)

    if response.status_code not in [200, 429]:
        return RequestResult(False, 0)

    return RequestResult(True, response.elapsed.microseconds)
