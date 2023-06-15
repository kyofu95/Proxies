import os
import pytest
from proxies.main import create_app
from proxies.core.database import db

from proxies.models.proxy import Proxy, ProxyProtocol
from proxies.models.address import Address
from proxies.models.health import Health


@pytest.fixture(scope="session")
def setup_flask():
    os.environ["SQLALCHEMY_DATABASE_URI"] = "testing"
    app = create_app()
    db.create_all()

    a1 = Address(country="United States", region=None, city=None)
    a2 = Address(country="Japan", region=None, city=None)

    db.session.add(a1)
    db.session.add(a2)

    h1 = Health(connections=1, failed_connections=0)
    h2 = Health(connections=1, failed_connections=0)
    h3 = Health(connections=1, failed_connections=0)

    db.session.add(h1)
    db.session.add(h2)
    db.session.add(h3)

    db.session.commit()

    p1 = Proxy(
        ip_address="30.0.0.1", ip_port=8080, protocol=ProxyProtocol.SOCKS4, latency=0, address_id=a1.id, health_id=h1.id
    )
    p2 = Proxy(
        ip_address="30.0.0.2", ip_port=80, protocol=ProxyProtocol.SOCKS5, latency=0, address_id=a1.id, health_id=h2.id
    )
    p3 = Proxy(
        ip_address="30.0.0.3", ip_port=5050, protocol=ProxyProtocol.SOCKS4, latency=0, address_id=a2.id, health_id=h3.id
    )

    db.session.add(p1)
    db.session.add(p2)
    db.session.add(p3)

    db.session.commit()

    yield app
    # Explicitly close DB connection
    db.session.close()
    db.drop_all()
