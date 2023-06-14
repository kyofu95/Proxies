from datetime import datetime
from typing import List, Tuple
import concurrent.futures

from proxies.core.scheduler import scheduler

from proxies.models.repositories.proxy_repository import ProxyRepository, Proxy as DB_Proxy
from proxies.models.repositories.health_repository import HealthRepository

from proxies.utils.network import is_proxy_active

# This constant defines number of proxies per thread worker
CHUNK_SIZE = 10

proxy_rep = ProxyRepository()
health_rep = HealthRepository()


def check_proxies(proxies: List[DB_Proxy]) -> Tuple[DB_Proxy, bool]:
    """Check if the given proxies are working or not. This function is used in thread workers."""

    checked_proxies = []
    for proxy in proxies:
        protocol_name = proxy.protocol.name.lower()
        proxy_scheme = {protocol_name: f"{protocol_name}://{proxy.ip_address}:{proxy.ip_port}"}

        result = is_proxy_active("http://google.com", proxy_scheme, 5)

        checked_proxies.append((proxy, result.success))
    return checked_proxies


def update_oldest_proxies() -> None:
    """Update the health status of the oldest proxies and delete the ones that have failed a certain number of times."""

    with scheduler.app.app_context():
        # Get proxies with last checked date
        db_proxies = proxy_rep.get_oldest_proxies(1000)

        if not db_proxies:
            return

        chunks = [db_proxies[i : i + CHUNK_SIZE] for i in range(0, len(db_proxies), CHUNK_SIZE)]

        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            futures = [executor.submit(check_proxies, chunk) for chunk in chunks]

        checked_proxies = [proxy for future in futures for proxy in future.result()]

        for proxy, success in checked_proxies:
            proxy.health.connections += 1

            if not success:
                proxy.health.failed_connections += 1

            proxy.health.last_tested = datetime.utcnow()

            if proxy.health.failed_connections > 10 or (
                proxy.health.failed_connections == proxy.health.connections and proxy.health.failed_connections > 5
            ):
                # delete proxy record
                health_rep.delete(proxy.health)
                proxy_rep.delete(proxy)
                continue

            # update proxy database record
            health_rep.update(proxy.health)
