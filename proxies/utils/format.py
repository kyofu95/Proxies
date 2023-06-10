from datetime import datetime, timedelta
from typing import Any, Dict

from proxies.models import Proxy as DB_Proxy


def timedelta_format(td_object: timedelta) -> str:
    """
    Convert a timedelta object to a string representing the duration
    in years, months, days, hours, minutes, and seconds.
    """

    seconds = int(td_object.total_seconds())
    periods = [
        ("year", 60 * 60 * 24 * 365),
        ("month", 60 * 60 * 24 * 30),
        ("day", 60 * 60 * 24),
        ("hour", 60 * 60),
        ("minute", 60),
        ("second", 1),
    ]

    strings = []
    for period_name, period_seconds in periods:
        if seconds >= period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            has_s = "s" if period_value > 1 else ""
            strings.append(f"{period_value} {period_name}{has_s}")

    return ", ".join(strings)


def proxy_format(proxy: DB_Proxy) -> Dict[str, Any]:
    """Format the given proxy object into a dictionary."""

    return {
        "address": str(proxy.ip_address),
        "port": proxy.ip_port,
        "country": proxy.address.country,
        "protocol": proxy.protocol.name,
        "response": proxy.latency // 1000,
        "last_update": timedelta_format(datetime.utcnow() - proxy.health.last_tested),
    }
