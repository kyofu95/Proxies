from proxies.core.database import db


class Address(db.Model):
    """Address database model represents a location with its associated country, region, and city."""

    __tablename__ = "address"
    __table_args__ = (db.UniqueConstraint("country", "region", "city"),)

    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(100))
    region = db.Column(db.String(100))
    city = db.Column(db.String(100))
