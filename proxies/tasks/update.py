from datetime import datetime
from typing import List, Tuple
import concurrent.futures

import requests

from proxies.core.database import db
from proxies.core.scheduler import scheduler

from proxies.models import Proxy as DB_Proxy

# This constant defines number of proxies per thread worker
CHUNK_SIZE = 10


def check_proxies(proxies: List[DB_Proxy]) -> Tuple[DB_Proxy, bool]:
    """Check if the given proxies are working or not. This function is used in thread workers."""

    checked_proxies = []
    for proxy in proxies:
        failed = False

        proxies = {proxy.protocol.name.lower(): proxy.get_uri()}

        try:
            response = requests.get("http://google.com", proxies=proxies, timeout=5)
        except (
            requests.exceptions.ProxyError,
            requests.exceptions.Timeout,
            requests.exceptions.ChunkedEncodingError,
            requests.exceptions.ConnectionError,
        ):
            failed = True

        if not failed and response.status_code not in [200, 429]:
            failed = True

        checked_proxies.append((proxy, failed))
    return checked_proxies


def update_oldest_proxies() -> None:
    """Update the health status of the oldest proxies and delete the ones that have failed a certain number of times."""

    with scheduler.app.app_context():
        # Get proxies with last checked date
        db_proxies = DB_Proxy.get_oldest_proxies(500)

        if not db_proxies:
            return

        chunks = [db_proxies[i : i + CHUNK_SIZE] for i in range(0, len(db_proxies), CHUNK_SIZE)]

        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            futures = [executor.submit(check_proxies, chunk) for chunk in chunks]

        checked_proxies = [proxy for future in futures for proxy in future.result()]

        for proxy, failed in checked_proxies:
            proxy.health.connections += 1

            if failed:
                proxy.health.failed_connections += 1

            proxy.health.last_tested = datetime.utcnow()

            if proxy.health.failed_connections == 10 and proxy.health.failed_connections == proxy.health.connections:
                # delete proxy record
                db.session.delete(proxy.health)
                db.session.delete(proxy)
                db.session.commit()
                continue

            # update proxy database record
            db.session.commit()
