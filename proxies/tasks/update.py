from datetime import datetime
from typing import List, Tuple
import concurrent.futures

from proxies.core.database import db
from proxies.core.scheduler import scheduler

from proxies.models import Proxy as DB_Proxy

from proxies.utils.network import is_proxy_active

# This constant defines number of proxies per thread worker
CHUNK_SIZE = 10


def check_proxies(proxies: List[DB_Proxy]) -> Tuple[DB_Proxy, bool]:
    """Check if the given proxies are working or not. This function is used in thread workers."""

    checked_proxies = []
    for proxy in proxies:
        proxy_scheme = {proxy.protocol.name.lower(): proxy.get_uri()}

        result = is_proxy_active("http://google.com", proxy_scheme, 5)

        checked_proxies.append((proxy, result.success))
    return checked_proxies


def update_oldest_proxies() -> None:
    """Update the health status of the oldest proxies and delete the ones that have failed a certain number of times."""

    with scheduler.app.app_context():
        # Get proxies with last checked date
        db_proxies = DB_Proxy.get_oldest_proxies(500)

        if not db_proxies:
            return

        chunks = [db_proxies[i : i + CHUNK_SIZE] for i in range(0, len(db_proxies), CHUNK_SIZE)]

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
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
                db.session.delete(proxy.health)
                db.session.delete(proxy)
                db.session.commit()
                continue

            # update proxy database record
            db.session.commit()
