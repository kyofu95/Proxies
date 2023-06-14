from datetime import datetime

from proxies.core.database import db
from proxies.models.health import Health


class HealthRepository:
    """A class that provides methods to interact with the Health table in the database."""

    def create(self, connections: int = 1, failed_connections: int = 0) -> Health:
        """Create a new Health object in the database."""

        db_health = Health(
            connections=connections, failed_connections=failed_connections, last_tested=datetime.utcnow()
        )

        db.session.add(db_health)
        db.session.commit()

        return db_health

    def update(self, health: Health) -> None:
        """Update the given Health instance in the database."""

        db.session.commit()

    def delete(self, health: Health) -> None:
        """Delete the given Health instance from the database."""

        db.session.delete(health)
        db.session.commit()
