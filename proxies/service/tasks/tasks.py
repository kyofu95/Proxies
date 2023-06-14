from datetime import datetime, timedelta

from proxies.core.scheduler import scheduler
from proxies.service.tasks.source import fetch_new_proxies
from proxies.service.tasks.update import update_oldest_proxies


def register_tasks() -> None:
    """Register apscheduler tasks."""

    scheduler.add_job(
        fetch_new_proxies, "interval", hours=12, id="fetch_job_1", next_run_time=datetime.now() + timedelta(seconds=1)
    )

    scheduler.add_job(update_oldest_proxies, "interval", minutes=30, id="update_job_1")
