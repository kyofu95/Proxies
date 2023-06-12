import logging

import geoip2.database

from proxies.service.address import Address
from proxies.service.proxy import Proxy
from proxies.service.geoip.base import IBaseGeolocation

from proxies.core.config import settings


class MaxmindLiteDb2Geolocation(IBaseGeolocation):
    """
    Geolocation implementation using the MaxMind GeoLite2 City database.

    This class provides a concrete implementation of the IBaseGeolocation
    interface, using the MaxMind GeoLite2 City database to store geolocation
    information.
    """

    # The path to the GeoLite2-City.mmdb file.
    litedb2_path = settings.MAXDBLITE_PATH

    def __init__(self) -> None:
        try:
            self.db_reader = geoip2.database.Reader(self.litedb2_path)
        except FileNotFoundError as exc:
            logging.exception("litedb2 was not found with path %s", self.litedb2_path, exc_info=exc)
            raise exc
        except Exception as exc:
            logging.exception("geoip2 reader failed", exc_info=exc)
            raise exc


    def get_address(self, proxy: Proxy) -> Address:
        """Get the geolocation information for the given IP address using the MaxMind GeoLite2 City database."""

        try:
            response = self.db_reader.city(proxy.ip_address)
        except geoip2.errors.AddressNotFoundError:
            return Address()

        return Address(
            city=response.city.name, region=response.subdivisions.most_specific.name, country=response.country.name
        )
