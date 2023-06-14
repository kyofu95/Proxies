from datetime import datetime
from enum import Enum

from sqlalchemy.dialects.postgresql import INET

from proxies.core.database import db


class ProxyProtocol(Enum):
    """
    Enum representing different proxy protocols:
    SOCKS4, SOCKS5, HTTP, and HTTPS (also known as SSL).
    """

    SOCKS4 = 1
    SOCKS5 = 2
    HTTP = 3
    HTTPS = 4


class Proxy(db.Model):
    """A database model representing a proxy server."""

    __tablename__ = "proxy"
    __table_args__ = (db.UniqueConstraint("ip_address", "ip_port", "protocol"),)

    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(INET, nullable=False)
    ip_port = db.Column(db.Integer, nullable=False)
    protocol = db.Column(
        db.Enum(ProxyProtocol, values_callable=lambda obj: [e.name for e in obj]),
        nullable=False,
    )

    latency = db.Column(db.Integer)

    added = db.Column(db.DateTime, default=datetime.utcnow)

    address_id = db.Column(db.ForeignKey("address.id"))
    health_id = db.Column(db.ForeignKey("health.id"))

    address = db.relationship("Address", uselist=False)
    health = db.relationship("Health", uselist=False)
