import concurrent.futures
from ipaddress import ip_address
from collections import namedtuple
import time
import logging
from typing import List, Set


from sqlalchemy.exc import SQLAlchemyError

from proxies.core.scheduler import scheduler

from proxies.models.repositories.proxy_repository import ProxyRepository
from proxies.models.repositories.address_repository import AddressRepository
from proxies.models.repositories.health_repository import HealthRepository

from proxies.service.source.base import UncheckedProxyTuple
from proxies.service.source.manager import proxy_source_manager
from proxies.service.geoip.maxmind import MaxmindLiteDb2Geolocation

from proxies.utils.network import is_proxy_active

CheckedProxyTuple = namedtuple("CheckedProxy", ["address", "port", "protocol", "latency"])

# This constant defines number of proxies per thread worker
CHUNK_SIZE = 10

proxy_rep = ProxyRepository()
address_rep = AddressRepository()
health_rep = HealthRepository()


def check_proxies(raw_proxies: List[UncheckedProxyTuple]) -> List[CheckedProxyTuple]:
    """Check the connectivity of a proxies. This function is used in thread workers."""

    checked_proxies = []
    for raw_proxy in raw_proxies:
        protocol_name = raw_proxy.protocol.name.lower()
        proxy_scheme = {protocol_name: f"{protocol_name}://{raw_proxy.address}:{raw_proxy.port}"}

        result = is_proxy_active("http://google.com", proxy_scheme, 5)
        if result.success:
            checked_proxies.append(CheckedProxyTuple(*raw_proxy, result.latency))

    return checked_proxies


def store_proxies_in_db(cheched_proxies: List[CheckedProxyTuple]) -> None:
    """Store proxies in the database."""

    geodb = MaxmindLiteDb2Geolocation()

    for proxy in cheched_proxies:
        try:
            proxy_address = geodb.get_address(proxy[0])

            db_address = address_rep.get(proxy_address.country, proxy_address.region, proxy_address.city)
            if not db_address:
                db_address = address_rep.create(proxy_address.country, proxy_address.region, proxy_address.city)

            db_health = health_rep.create(1, 0)

            db_proxy = proxy_rep.create(
                proxy.address, proxy.port, proxy.protocol, proxy.latency, db_address.id, db_health.id
            )
        except SQLAlchemyError as exc:
            logging.exception("Db exception", exc_info=exc)


def fetch_from_all_sources() -> Set[UncheckedProxyTuple]:
    """Iterates over all sources and collects fresh proxies."""

    raw_proxies = set()
    for source in proxy_source_manager.get_instances():
        raw_proxies.update(source.get_proxies())
    return raw_proxies


def fetch_new_proxies() -> None:
    """Fetch new proxies from available sources and store them in the database."""

    with scheduler.app.app_context():
        raw_proxies = fetch_from_all_sources()
        if not raw_proxies:
            return

        # Get a list of already stored proxies
        db_proxy_list = proxy_rep.get_all_proxy_by_columns()

        # Prepare sets for O(n) filtering
        db_proxy_set = set(UncheckedProxyTuple(ip_address(proxy[0]), proxy[1], proxy[2]) for proxy in db_proxy_list)

        raw_proxies = raw_proxies.difference(db_proxy_set)

        chunks = [list(raw_proxies)[i : i + CHUNK_SIZE] for i in range(0, len(raw_proxies), CHUNK_SIZE)]

        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            futures = [executor.submit(check_proxies, chunk) for chunk in chunks]

            for future in futures:
                if not future.done():
                    time.sleep(2)
                else:
                    store_proxies_in_db(future.result())
