import pytest

from proxies.service.source.github import JetkaiProxySource, TheSpeedXProxySource, ProxyProtocol


def test_speedx_get_proxies(monkeypatch):
    source = TheSpeedXProxySource()

    def fake_make_request(*args, **kwargs):
        class MockResponce:
            def __init__(self, text) -> None:
                self.text = text

        return MockResponce("34.0.0.1:8080\n209.97.150.1:8080\n20.111.54.1:8080\n192.168.1.1:80")

    monkeypatch.setattr(TheSpeedXProxySource, "make_request", fake_make_request)
    monkeypatch.setattr(TheSpeedXProxySource, "PROTOCOL_LIST", [(ProxyProtocol.HTTP, "http.txt")])

    proxies = source.get_proxies()
    assert len(proxies) == 3
    assert str(proxies[0].ip_address) == "34.0.0.1"
    assert str(proxies[0].ip_port) == "8080"
    assert str(proxies[2].ip_address) == "20.111.54.1"
    assert str(proxies[2].ip_port) == "8080"


raw_proxy_list = [
    {"ip": "34.0.0.1", "protocols": [{"port": 80, "type": "http"}, {"port": 443, "type": "https"}]},
    {"ip": "34.0.0.2", "protocols": [{"port": 8080, "type": "socks5"}]},
]


def test_jetkai_get_proxies(monkeypatch):
    source = JetkaiProxySource()

    def fake_make_request(*args, **kwargs):
        class MockResponce:
            def json(self):
                return raw_proxy_list

        return MockResponce()
    
    monkeypatch.setattr(JetkaiProxySource, "make_request", fake_make_request)

    proxies = source.get_proxies()
    assert len(proxies) == 3
    assert str(proxies[0].ip_address) == "34.0.0.1"
    assert str(proxies[0].ip_port) == "80"
    assert str(proxies[2].ip_address) == "34.0.0.2"
    assert str(proxies[2].ip_port) == "8080"
