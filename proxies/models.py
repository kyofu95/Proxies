from __future__ import annotations
from datetime import datetime
from typing import List, Tuple

from sqlalchemy.dialects.postgresql import INET

from proxies.core.database import db
from proxies.service.proxy import ProxyProtocol, IPAddress


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

    @staticmethod
    def get_all_proxies_number() -> int:
        """Retrieve the total number of proxies in the database."""
        db_proxy_list = (
            db.session.execute(db.select(Proxy.ip_address, Proxy.ip_port, Proxy.protocol))
            .columns("ip_address", "ip_port", "protocol")
            .all()
        )
        return len(db_proxy_list)

    @staticmethod
    def get_all_proxies_by_proxy_columns() -> List[Tuple[IPAddress, int, ProxyProtocol]]:
        """Return a list of tuples based on fields 'ip_address', 'ip_port' and 'protocol'."""

        db_proxy_list = (
            db.session.execute(db.select(Proxy.ip_address, Proxy.ip_port, Proxy.protocol))
            .columns("ip_address", "ip_port", "protocol")
            .all()
        )
        return db_proxy_list

    @staticmethod
    def get_newest_proxies(limit: int = 500) -> List[Proxy]:
        """Retrieve the newest proxies from the database based on the last time they were tested and failed connections."""

        db_proxies = (
            db.session.execute(
                db.select(Proxy)
                .join(Proxy.health)
                .order_by(Health.last_tested.desc(), Health.failed_connections.asc())
                .limit(limit)
            )
            .scalars()
            .all()
        )
        return db_proxies

    @staticmethod
    def get_oldest_proxies(limit: int = 500) -> List[Proxy]:
        """Retrieve the oldest proxies from the database based on the last time they were tested."""

        db_proxies = (
            db.session.execute(db.select(Proxy).join(Proxy.health).order_by(Health.last_tested.asc()).limit(limit))
            .scalars()
            .all()
        )
        return db_proxies

    @staticmethod
    def get_proxies_by_country_or_protocol(
        country: str | None, protocol: ProxyProtocol | None, limit: int = 50
    ) -> List[Proxy]:
        """
        Retrieve a list of proxies that match the specified country and protocol
        ordered by nearest time they were tested and failed connections.
        """

        filters = []
        if country:
            filters.append(Address.country == country)
        if protocol:
            filters.append(Proxy.protocol == protocol)

        statement = (
            db.select(Proxy)
            .join(Proxy.address)
            .join(Proxy.health)
            .filter(*filters)
            .order_by(Health.last_tested.desc(), Health.failed_connections.asc())
            .limit(limit)
        )
        return db.session.execute(statement).scalars().all()

    def get_uri(self) -> str:
        """Returns a string representing a proxy URI."""

        protocol_name = self.protocol.name.lower()
        return f"{protocol_name}://{self.ip_address}:{self.ip_port}"


class Address(db.Model):
    """Address database model represents a location with its associated country, region, and city."""

    __tablename__ = "address"
    __table_args__ = (db.UniqueConstraint("country", "region", "city"),)

    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(100))
    region = db.Column(db.String(100))
    city = db.Column(db.String(100))

    @staticmethod
    def get_address(country: str | None, region: str | None, city: str | None) -> Address | None:
        """
        This function returns an instance of the Address class if a matching record exists in the database,
        otherwise it returns None.
        """

        db_address = db.session.execute(
            db.select(Address).filter_by(country=country, region=region, city=city)
        ).scalar()
        return db_address

    @staticmethod
    def get_countries() -> List[str]:
        """Return a list of distinct countries from the Address table."""

        db_countries = (
            db.session.execute(
                db.select(Address.country).where(Address.country.isnot(None)).distinct().order_by(Address.country.asc())
            )
            .columns("country")
            .all()
        )
        return [country[0] for country in db_countries]


class Health(db.Model):
    """A class representing the health status of a proxy."""

    __tablename__ = "health"

    id = db.Column(db.Integer, primary_key=True)
    connections = db.Column(db.Integer, default=0, nullable=False)
    failed_connections = db.Column(db.Integer, default=0, nullable=False)

    last_tested = db.Column(db.DateTime, default=datetime.utcnow())
