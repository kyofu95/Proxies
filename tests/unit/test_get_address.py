import pytest
from proxies.service.geoip.maxmind import MaxmindLiteDb2Geolocation


# Fixture for initializing the object with the litedb2_path
@pytest.fixture(scope="module")
def db2_instance():
    your_instance = MaxmindLiteDb2Geolocation()
    return your_instance


# Test function for a successful get_address call
def test_get_address_success(db2_instance):
    address = db2_instance.get_address("8.8.8.8")

    # Assertions for the expected values
    assert address.city is None
    assert address.region is None
    assert address.country is not None


# Test function for AddressNotFoundError in get_address
def test_get_address_address_not_found_error(db2_instance):
    # Example invalid IP address

    address = db2_instance.get_address("0.0.0.0")
    # Assertions for the expected values
    assert address.city is None
    assert address.region is None
    assert address.country is None
