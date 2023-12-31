import pytest
from flask import Flask

from proxies.core.database import db

from proxies.service.tasks.source import fetch_new_proxies, CheckedProxyTuple
from proxies.utils.proxy_parse import parse_proxy, ProxyProtocol


class MockResult:
    def __init__(self) -> None:
        self.success = True
        self.latency = 10


fake_proxies = {
    parse_proxy("40.0.0.1", 8080, ProxyProtocol.HTTP),
    parse_proxy("40.0.0.2", 8080, ProxyProtocol.HTTP),
    parse_proxy("40.0.0.3", 8080, ProxyProtocol.HTTP),
}


def test_source_task(setup_flask: Flask, monkeypatch):
    def fake_is_proxy_active(*args, **kwargs):
        return MockResult()

    def fake_fetch_from_all_sources(*args, **kwargs):
        return fake_proxies

    def fake_store_proxies_in_db(proxies):
        global cheched_proxies
        cheched_proxies = len(proxies)

        for fake_proxy in fake_proxies:
            assert CheckedProxyTuple(*fake_proxy, 10) in proxies

    monkeypatch.setattr("proxies.service.tasks.source.is_proxy_active", fake_is_proxy_active)
    monkeypatch.setattr("proxies.service.tasks.source.fetch_from_all_sources", fake_fetch_from_all_sources)
    monkeypatch.setattr("proxies.service.tasks.source.store_proxies_in_db", fake_store_proxies_in_db)

    fetch_new_proxies()

    assert cheched_proxies == len(fake_proxies)
