from ipaddress import IPv4Address, IPv6Address
from typing import List, Tuple

from proxies.core.database import db
from proxies.models.proxy import Proxy, ProxyProtocol
from proxies.models.health import Health
from proxies.models.address import Address


class ProxyRepository:
    """A class that provides methods to interact with the Proxy table in the database."""

    def create(self, ip_address, ip_port, protocol, latency, address_id, health_id) -> Proxy:
        """Create a new Proxy object in the database."""

        db_proxy = Proxy(
            ip_address=str(ip_address),
            ip_port=ip_port,
            protocol=protocol,
            latency=latency,
            address_id=address_id,
            health_id=health_id,
        )

        db.session.add(db_proxy)
        db.session.commit()

        return db_proxy

    def delete(self, proxy: Proxy) -> None:
        """Delete the given Proxy instance from the database."""

        db.session.delete(proxy)
        db.session.commit()

    def get_all_proxies_number(self) -> int:
        """Retrieve the total number of proxies in the database."""

        db_proxy_list = self.get_all_proxy_by_columns()
        return len(db_proxy_list)

    def get_all_proxy_by_columns(self) -> List[Tuple[IPv4Address | IPv6Address, int, ProxyProtocol]]:
        """Return a list of tuples based on fields 'ip_address', 'ip_port' and 'protocol'."""

        db_proxy_list = (
            db.session.execute(db.select(Proxy.ip_address, Proxy.ip_port, Proxy.protocol))
            .columns("ip_address", "ip_port", "protocol")
            .all()
        )
        return db_proxy_list

    def get_newest_proxies(self, limit: int = 500) -> List[Proxy]:
        """
        Retrieve the newest proxies from the database based on the last time they were tested and failed connections.
        """

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

    def get_oldest_proxies(self, limit: int = 500) -> List[Proxy]:
        """Retrieve the oldest proxies from the database based on the last time they were tested."""

        db_proxies = (
            db.session.execute(db.select(Proxy).join(Proxy.health).order_by(Health.last_tested.asc()).limit(limit))
            .scalars()
            .all()
        )
        return db_proxies

    def get_proxies_by_country_or_protocol(
        self, country: str | None, protocol: ProxyProtocol | None, limit: int = 50
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
