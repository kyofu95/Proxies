import geoip2.database

from proxies.service.address import Address
from proxies.service.proxy import Proxy
from proxies.service.geoip.base import IBaseGeolocation


class MaxmindLiteDb2Geolocation(IBaseGeolocation):
    litedb2_path = "C:/GeoLite2-City.mmdb"

    def get_address(self, proxy: Proxy) -> Address:
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
