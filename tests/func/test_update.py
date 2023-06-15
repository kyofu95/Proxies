import pytest
from flask import Flask

from proxies.models.proxy import Proxy, ProxyProtocol
from proxies.models.address import Address
from proxies.models.health import Health

from proxies.core.database import db

from proxies.service.tasks.update import update_oldest_proxies


@pytest.fixture(scope="module")
def setup_db(setup_flask: Flask):
    a1 = Address(country="China", region=None, city=None)
    h1 = Health(connections=10, failed_connections=10)

    db.session.add(a1)
    db.session.add(h1)

    db.session.commit()

    p1 = Proxy(
        ip_address="30.0.0.10",
        ip_port=8080,
        protocol=ProxyProtocol.SOCKS4,
        latency=0,
        address_id=a1.id,
        health_id=h1.id,
    )

    db.session.add(p1)
    db.session.commit()


class MockResult:
    def __init__(self) -> None:
        self.success = True
        self.latency = 10


def test_update_task(setup_db, monkeypatch):
    def fake_is_proxy_active(*args, **kwargs):
        return MockResult()

    monkeypatch.setattr("proxies.service.tasks.update.is_proxy_active", fake_is_proxy_active)

    update_oldest_proxies()

    db_proxies = (db.session.execute(db.select(Proxy))).scalars().all()

    assert len(db_proxies) == 3

    db_proxies = (
        (
            db.session.execute(
                db.select(Proxy).filter(
                    (Proxy.ip_address == "30.0.0.10"), (Proxy.ip_port == 8080), (Proxy.protocol == ProxyProtocol.SOCKS4)
                )
            )
        )
        .scalars()
        .all()
    )

    assert len(db_proxies) == 0
