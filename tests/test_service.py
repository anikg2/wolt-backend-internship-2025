import pytest
from fastapi.testclient import TestClient
from dopc.service import dopc

client = TestClient(dopc)

@pytest.mark.asyncio
async def test_getDeliveryOrderPrice_success():
    # Test a valid request with all parameters correct
    # Using the example provided in the specification document
    response = client.get("/api/v1/delivery-order-price", params={
        "venue_slug": "home-assignment-venue-helsinki",
        "cart_value": 1000,
        "user_lat": 60.17094,
        "user_lon": 24.93087
    })
    assert response.status_code == 200
    data = response.json()
    
    # Check that the response fields are integers
    assert isinstance(data["total_price"], int)
    assert isinstance(data["small_order_surcharge"], int)
    assert isinstance(data["cart_value"], int)
    assert isinstance(data["delivery"]["fee"], int)
    assert isinstance(data["delivery"]["distance"], int)

@pytest.mark.asyncio
async def test_getDeliveryOrderPrice_invalidVenueSlug():
    # Test an invalid venue_slug to get 404 from the home assignment API
    response = client.get("/api/v1/delivery-order-price", params={
        "venue_slug": "home-assignment-venue-kolkata", # This is the city that I am from and we don't have wolt there yet
        "cart_value": 1000000,
        "user_lat": 22.498820,
        "user_lon": 88.317073
    })
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_getDeliveryOrderPrice_invalidCartValue():
    # Test with a negative cart value to return 400 error at the initial check
    response = client.get("/api/v1/delivery-order-price", params={
        "venue_slug": "home-assignment-venue-berlin",
        "cart_value": -100,
        "user_lat": 60.0,
        "user_lon": 30.0
    })
    assert response.status_code == 400
    data = response.json()
    assert "invalid_parameters" in data["detail"]
    assert "cart_value" in data["detail"]["invalid_parameters"]

@pytest.mark.asyncio
async def test_getDeliveryOrderPrice_invalidLatitude():
    # Testing with invalid latitude (out of valid range)
    response = client.get("/api/v1/delivery-order-price", params={
        "venue_slug": "home-assignment-venue-helsinki",
        "cart_value": 100,
        "user_lat": 200.0,  # Invalid latitude, has to be within [-90, 90]
        "user_lon": 30.0
    })
    assert response.status_code == 400
    data = response.json()
    assert "invalid_parameters" in data["detail"]
    assert "user_lat" in data["detail"]["invalid_parameters"]

@pytest.mark.asyncio
async def test_getDeliveryOrderPrice_deliveryDistanceLimitExceeded():
    # Test case where delivery is not possible due to distance being too large
    response = client.get("/api/v1/delivery-order-price", params={
        "venue_slug": "home-assignment-venue-helsinki",
        "cart_value": 100,
        "user_lat": 22.498820, # Once again using coordinates from my hometown in India
        "user_lon": 88.317073
    })
    assert response.status_code == 400
    data = response.json()
    assert data["detail"]["message"] == "Invalid request! Delivery distance is too large! Delivery not possible!"
