import logging

from flask import Flask

from apscheduler.events import EVENT_JOB_ERROR
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()


def listener(event):
    """APScheduler listener."""

    scheduler.app.logger.exception(
        "Job %i raised %s", event.job_id, event.exception.__class__.__name__, exc_info=event.exception
    )


def init_scheduler(app: Flask):
    """Initialize APScheduler."""

    scheduler.app = app
    scheduler.start()

    scheduler.add_listener(listener, EVENT_JOB_ERROR)
