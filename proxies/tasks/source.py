import concurrent.futures
from ipaddress import ip_address
import time
from typing import List

from proxies.core.database import db
from proxies.core.scheduler import scheduler

from proxies.models import Proxy as DB_Proxy, Address as DB_Address, Health as DB_Health

from proxies.service.source.manager import proxy_source_manager
from proxies.service.proxy import Proxy
from proxies.service.geoip.maxmind import MaxmindLiteDb2Geolocation

from proxies.tasks.netwok_utils import is_proxy_active

# This constant defines number of proxies per thread worker
CHUNK_SIZE = 10


def check_proxies(raw_proxies: List[Proxy]) -> List[Proxy]:
    """Check the connectivity of a proxies. This function is used in thread workers."""

    checked_proxies = []
    for raw_proxy in raw_proxies:
        proxy_scheme = {raw_proxy.protocol.name.lower(): raw_proxy.get_uri()}

        result = is_proxy_active("http://google.com", proxy_scheme, 5)
        if result.success:
            raw_proxy.latency = result.latency
            checked_proxies.append(raw_proxy)

    return checked_proxies


def store_proxies_in_db(cheched_proxies: List[Proxy]) -> None:
    """Store proxies in the database."""

    geodb = MaxmindLiteDb2Geolocation()

    for proxy in cheched_proxies:
        proxy_address = geodb.get_address(proxy.ip_address)

        db_proxy = DB_Proxy(
            ip_address=str(proxy.ip_address),
            ip_port=proxy.ip_port,
            protocol=proxy.protocol,
            latency=proxy.latency,
        )

        db_health = DB_Health(connections=1, failed_connections=0)

        db.session.add(db_proxy)
        db.session.add(db_health)
        db.session.commit()

        db_proxy.health_id = db_health.id

        db_address = DB_Address.get_address(proxy_address.country, proxy_address.region, proxy_address.city)

        if db_address:
            db_proxy.address_id = db_address.id
        else:
            db_address = DB_Address(country=proxy_address.country, region=proxy_address.region, city=proxy_address.city)

            db.session.add(db_address)
            db.session.commit()

        db_proxy.address_id = db_address.id
        db.session.commit()


def fetch_new_proxies() -> None:
    """Fetch new proxies from available sources and store them in the database."""

    with scheduler.app.app_context():
        raw_proxies = set()
        for source in proxy_source_manager.get_instances():
            proxies = source.get_proxies()
            raw_proxies.update(proxies)

        if not raw_proxies:
            return

        # Get a list of already stored proxies
        db_proxy_list = DB_Proxy.get_all_proxies_by_proxy_columns()

        # Prepare sets for O(n) filtering
        db_proxy_set = set(
            Proxy(ip_address=ip_address(proxy[0]), ip_port=proxy[1], protocol=proxy[2]) for proxy in db_proxy_list
        )

        raw_proxies = raw_proxies.difference(db_proxy_set)

        chunks = [list(raw_proxies)[i : i + CHUNK_SIZE] for i in range(0, len(raw_proxies), CHUNK_SIZE)]

        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            futures = [executor.submit(check_proxies, chunk) for chunk in chunks]

            for future in futures:
                if not future.done():
                    time.sleep(5)
                else:
                    store_proxies_in_db(future.result())
