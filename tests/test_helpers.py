import pytest
from dopc.helpers import (
    getStaticInformationURL,
    getDynamicInformationURL,
    computeDistance,
    computeDeliveryFeeAndSurcharge,
    getServicePort,
)
from dopc.config import HOME_API_BASE, DOPC_DEFAULT_PORT


def test_getStaticInformationURL():
    venue_slug = "home-assignment-venue-helsinki"
    expected_url = f"{HOME_API_BASE}/{venue_slug}/static"
    assert getStaticInformationURL(venue_slug) == expected_url

def test_getDynamicInformationURL():
    venue_slug = "home-assignment-venue-berlin"
    expected_url = f"{HOME_API_BASE}/{venue_slug}/dynamic"
    assert getDynamicInformationURL(venue_slug) == expected_url

def test_computeDistance():
    # All expected values and parameters taken from the specification document
    # And from the Home Assignment API Static URL for venue_slug helsinki
    expected_distance = 177 
    user_lat = 60.17094
    user_lon = 24.93087
    venue_lat = 60.17012143
    venue_lon = 24.92813512
    assert computeDistance(user_lat, user_lon, venue_lat, venue_lon) == expected_distance

# Test that the delivery fee and surcharge are computed as expected
def test_computeDeliveryFeeAndSurcharge():
    cart_value = 1000
    distance = 177
    minimum_order_value = 1000.0
    delivery_base_price = 190.0
    distance_ranges = [
        {"min": 0, "max": 500, "a": 0, "b": 0, "flag": None},
        {"min": 500, "max": 1000, "a": 100, "b": 0, "flag": None},
        {"min": 1000, "max": 1500, "a": 200, "b": 0, "flag": None},
        {"min": 1500, "max": 2000, "a": 200, "b": 1, "flag": None},
        {"min": 2000, "max": 0, "a": 0, "b": 0, "flag": None}
    ]

    expected_fee = 190  # Taken directly from the specification document
    expected_surcharge = 0  # Taken directly from the specification document

    delivery_fee, surcharge = computeDeliveryFeeAndSurcharge(
        cart_value, distance, minimum_order_value, delivery_base_price, distance_ranges
    )
    assert delivery_fee == expected_fee
    assert surcharge == expected_surcharge

# Test that a value error is raised when the delivery distance exceeds the limit
def test_computeDeliveryFeeAndSurcharge_exceeds_range():
    cart_value = 1200
    distance = 4000  # Exceeds the maximum range
    minimum_order_value = 1000.0
    delivery_base_price = 200.0
    distance_ranges = [
        {"min": 0, "max": 1000, "a": 50, "b": 12, "flag": None},
        {"min": 1000, "max": 2000, "a": 100, "b": 15, "flag": None},
        {"min": 2000, "max": 0, "a": 0, "b": 0, "flag": None},
    ]

    with pytest.raises(ValueError, match="The delivery distance is too large! Delivery not possible!"):
        computeDeliveryFeeAndSurcharge(
            cart_value, distance, minimum_order_value, delivery_base_price, distance_ranges
        )

# Test that the function in fact returns the correct value from the configuration file
def test_getServicePort():
    assert getServicePort() == DOPC_DEFAULT_PORT

if __name__ == "__main__":
    pytest.main()
