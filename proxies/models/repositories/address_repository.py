from typing import List

from proxies.core.database import db
from proxies.models.address import Address


class AddressRepository:
    """A class that provides methods to interact with the Address table in the database."""

    def create(self, country: str | None, region: str | None, city: str | None) -> Address:
        """Create a new Address object in the database."""

        db_address = Address(country=country, region=region, city=city)

        db.session.add(db_address)
        db.session.commit()

        return db_address

    def get(self, country: str | None, region: str | None, city: str | None) -> Address | None:
        """Retrieve an Address object from the database."""

        db_address = db.session.execute(
            db.select(Address).filter_by(country=country, region=region, city=city)
        ).scalar()
        return db_address

    def get_countries(self) -> List[str]:
        """Retrieve a list of unique countries from the Address table in the database."""

        db_countries = (
            db.session.execute(
                db.select(Address.country).where(Address.country.isnot(None)).distinct().order_by(Address.country.asc())
            )
            .columns("country")
            .all()
        )
        # List of tuples to a list of strings
        return [country[0] for country in db_countries]
