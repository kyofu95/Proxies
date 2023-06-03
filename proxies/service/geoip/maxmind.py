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

    def get_address(self, proxy: Proxy) -> Address:
        """Get the geolocation information for the given IP address using the MaxMind GeoLite2 City database."""

        with geoip2.database.Reader(self.litedb2_path) as reader:
            address = Address()

            try:
                response = reader.city(proxy.ip_address)
            except geoip2.errors.AddressNotFoundError:
                return address

            address.city = response.city.name
            address.region = response.subdivisions.most_specific.name
            address.country = response.country.name

            return address