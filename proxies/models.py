from datetime import datetime
import enum

from sqlalchemy.dialects.postgresql import INET

from proxies.core.database import db


class SQLProxyProtocol(enum.Enum):
    """
    Represents different proxy protocols.

    This enumeration defines the supported proxy protocols:
    - UNKNOWN: Unknown proxy protocol
    - SOCKS4: SOCKS version 4
    - SOCKS5: SOCKS version 5
    - HTTP: HTTP proxy
    - HTTPS: HTTPS proxy
    """

    UNKNOWN = 0
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
        db.Enum(SQLProxyProtocol, values_callable=lambda obj: [e.name for e in obj]),
        default=SQLProxyProtocol.UNKNOWN,
        nullable=False,
    )
    login = db.Column(db.String(100))
    password = db.Column(db.String(100))

    anonymity_level = db.Column(db.Integer)
    latency = db.Column(db.Integer)

    added = db.Column(db.DateTime, default=datetime.utcnow)

    address_id = db.Column(db.ForeignKey("address.id"))
    health_id = db.Column(db.ForeignKey("health.id"))

    address = db.relationship("Address", uselist=False)
    health = db.relationship("Health", uselist=False)


class Address(db.Model):
    """Address database model represents a location with its associated country, region, and city."""

    __tablename__ = "address"

    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(100))
    region = db.Column(db.String(100))
    city = db.Column(db.String(100))


class Health(db.Model):
    """A class representing the health status of a proxy."""

    __tablename__ = "health"

    id = db.Column(db.Integer, primary_key=True)
    connections = db.Column(db.Integer, default=0)
    failed_connections = db.Column(db.Integer, default=0)

    last_tested = db.Column(db.DateTime, default=datetime.utcnow)
