from typing import Dict
from collections import namedtuple

import requests

RequestResult = namedtuple("RequestResult", ["success", "latency"])


def is_proxy_active(uri: str, proxy_dict: Dict[str, str], timeout: int) -> RequestResult:
    """Check if the proxy is active by attempting a connection."""

    try:
        response = requests.get(uri, proxies=proxy_dict, timeout=timeout)
    except (
        requests.exceptions.ProxyError,
        requests.exceptions.Timeout,
        requests.exceptions.ChunkedEncodingError,
    ):
        return RequestResult(False, 0)

    if response.status_code not in [200, 429]:
        return RequestResult(False, 0)

    return RequestResult(True, response.elapsed.microseconds)
