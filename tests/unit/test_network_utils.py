from datetime import timedelta

import requests
import pytest


from proxies.utils.network import make_request, is_proxy_active


def test_make_request_ok(monkeypatch):
    def fake_get(*args, **kwargs):
        class FakeResponse:
            def __init__(self) -> None:
                self.text = "1"
                self.ok = True
                self.status_code = 200

        return FakeResponse()

    monkeypatch.setattr("requests.get", fake_get)

    response_text = make_request("https://www.google.com/")
    assert response_text == "1"


def test_make_request_not_ok(monkeypatch):
    def fake_get(*args, **kwargs):
        class FakeResponse:
            def __init__(self) -> None:
                self.text = ""
                self.ok = False
                self.status_code = 500

        return FakeResponse()

    monkeypatch.setattr("requests.get", fake_get)

    response_text = make_request("https://www.google.com/")
    assert response_text is None


def test_make_request_raise(monkeypatch):
    def fake_get(*args, **kwargs):
        class FakeResponse:
            def __init__(self) -> None:
                self.text = "1"
                self.ok = True
                self.status_code = 200

        raise requests.exceptions.RequestException()
        return FakeResponse()

    monkeypatch.setattr("requests.get", fake_get)

    response_text = make_request("https://www.google.com/")
    assert response_text is None


def test_is_proxy_active_ok(monkeypatch):
    def fake_get(*args, **kwargs):
        class FakeResponse:
            def __init__(self) -> None:
                self.text = ""
                self.status_code = 200
                self.elapsed = timedelta(seconds=4)

        return FakeResponse()

    monkeypatch.setattr("requests.get", fake_get)

    result = is_proxy_active("https://www.google.com/", {"a": "b"}, 5)
    assert result.success
    assert result.latency == timedelta(seconds=4).microseconds


def test_is_proxy_active_not_ok(monkeypatch):
    def fake_get(*args, **kwargs):
        class FakeResponse:
            def __init__(self) -> None:
                self.text = ""
                self.status_code = 500
                self.elapsed = timedelta(seconds=4)

        return FakeResponse()

    monkeypatch.setattr("requests.get", fake_get)

    result = is_proxy_active("https://www.google.com/", {"a": "b"}, 5)
    assert result.success is False
    assert result.latency == 0


def test_is_proxy_active_raise(monkeypatch):
    def fake_get(*args, **kwargs):
        class FakeResponse:
            def __init__(self) -> None:
                self.text = ""
                self.status_code = 500
                self.elapsed = timedelta(seconds=4)

        raise requests.exceptions.ProxyError()
        return FakeResponse()

    monkeypatch.setattr("requests.get", fake_get)

    result = is_proxy_active("https://www.google.com/", {"a": "b"}, 5)
    assert result.success is False
    assert result.latency == 0
