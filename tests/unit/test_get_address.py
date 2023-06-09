import pytest
import geoip2.database
import geoip2.errors
from proxies.service.geoip.maxmind import MaxmindLiteDb2Geolocation, Proxy, Address
from proxies.service.proxy import ProxyProtocol


# Fixture for initializing the object with the litedb2_path
@pytest.fixture(scope="module")
def your_class_instance():
    your_instance = MaxmindLiteDb2Geolocation()
    return your_instance


# Fixture for the Proxy object
@pytest.fixture(scope="module")
def proxy_instance():
    proxy = Proxy("8.8.8.8", 80, ProxyProtocol.SOCKS4)
    return proxy


# Test function for a successful get_address call
def test_get_address_success(your_class_instance, proxy_instance):
    address = your_class_instance.get_address(proxy_instance)

    # Assertions for the expected values
    assert address.city is None
    assert address.region is None
    assert address.country is not None


# Test function for AddressNotFoundError in get_address
def test_get_address_address_not_found_error(your_class_instance):
        # Example invalid IP address
        proxy = Proxy("0.0.0.0", 80, ProxyProtocol.SOCKS4)
        address = your_class_instance.get_address(proxy)
        # Assertions for the expected values
        assert address.city is None
        assert address.region is None
        assert address.country is None
