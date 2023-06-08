from flask import Flask

from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()


def init_scheduler(app: Flask):
    """Initialize APScheduler."""

    scheduler.app = app
    scheduler.start()
