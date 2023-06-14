from datetime import datetime

from proxies.core.database import db


class Health(db.Model):
    """A class representing the health status of a proxy."""

    __tablename__ = "health"

    id = db.Column(db.Integer, primary_key=True)
    connections = db.Column(db.Integer, default=0, nullable=False)
    failed_connections = db.Column(db.Integer, default=0, nullable=False)

    last_tested = db.Column(db.DateTime, default=datetime.utcnow())
