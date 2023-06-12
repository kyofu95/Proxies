from datetime import datetime, timedelta

import pytest

from proxies.service.proxy import ProxyProtocol
from proxies.models import Proxy as DB_Proxy, Health as DB_Health, Address as DB_Address
from proxies.utils.format import proxy_format


def test_proxy_format():
    proxy = DB_Proxy(
        ip_address="192.168.0.1",
        ip_port=8080,
        protocol=ProxyProtocol.HTTP,
        latency=1000,
        health=DB_Health(last_tested=datetime.utcnow() - timedelta(hours=2)),
        address=DB_Address(country="United States"),
    )
    expected_output = {
        "address": "192.168.0.1",
        "port": 8080,
        "country": "United States",
        "protocol": "HTTP",
        "response": 1,
        "last_update": "2 hours",
    }
    assert proxy_format(proxy) == expected_output

def test_proxy_format_country_none():
    proxy = DB_Proxy(
        ip_address="192.168.0.1",
        ip_port=8080,
        protocol=ProxyProtocol.HTTP,
        latency=1000,
        health=DB_Health(last_tested=datetime.utcnow() - timedelta(minutes=2)),
        address=DB_Address(country=None),
    )
    expected_output = {
        "address": "192.168.0.1",
        "port": 8080,
        "country": "",
        "protocol": "HTTP",
        "response": 1,
        "last_update": "2 minutes",
    }
    assert proxy_format(proxy) == expected_output

def test_proxy_format_now():
    proxy = DB_Proxy(
        ip_address="192.168.0.1",
        ip_port=8080,
        protocol=ProxyProtocol.HTTP,
        latency=1000,
        health=DB_Health(last_tested=datetime.utcnow()),
        address=DB_Address(country="United Kingdom"),
    )
    expected_output = {
        "address": "192.168.0.1",
        "port": 8080,
        "country": "United Kingdom",
        "protocol": "HTTP",
        "response": 1,
        "last_update": "now",
    }
    assert proxy_format(proxy) == expected_output