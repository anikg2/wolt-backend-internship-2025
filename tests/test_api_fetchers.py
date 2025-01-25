import pytest
import respx
from fastapi import HTTPException
from httpx import Response
from dopc.api_fetchers import fetchStaticData, fetchDynamicData
from dopc.helpers import getStaticInformationURL, getDynamicInformationURL

# Test cases for fetchStaticData
@pytest.mark.asyncio
@respx.mock
async def test_fetchStaticData_success():
    venue_slug = "home-assignment-venue-helsinki"
    mock_url = getStaticInformationURL(venue_slug)
    mock_coordinates = [10.0, 20.0]

    # Mocking the HTTP GET request
    respx.get(mock_url).mock(
        return_value=Response(200, json={"venue_raw": {"location": {"coordinates": mock_coordinates}}})
    )

    # Test success scenario
    result = await fetchStaticData(venue_slug)
    assert result == mock_coordinates

@pytest.mark.asyncio
@respx.mock
async def test_fetchStaticData_invalid_slug():
    venue_slug = "invalid-venue"
    mock_url = getStaticInformationURL(venue_slug)

    # Mocking the HTTP GET request with a 400 error
    respx.get(mock_url).mock(return_value=Response(400))

    # Test invalid slug scenario
    with pytest.raises(HTTPException) as exc_info:
        await fetchStaticData(venue_slug)
    assert exc_info.value.status_code == 400

@pytest.mark.asyncio
@respx.mock
async def test_fetchStaticData_server_error():
    venue_slug = "server-error-venue"
    mock_url = getStaticInformationURL(venue_slug)

    # Mocking the HTTP GET request with a server error
    respx.get(mock_url).mock(return_value=Response(500))

    # Test server error scenario
    with pytest.raises(HTTPException) as exc_info:
        await fetchStaticData(venue_slug)
    assert exc_info.value.status_code == 500

# Test cases for fetchDynamicData
@pytest.mark.asyncio
@respx.mock
async def test_fetchDynamicData_success():
    venue_slug = "test-venue"
    mock_url = getDynamicInformationURL(venue_slug)
    mock_data = {
        "venue_raw": {
            "delivery_specs": {
                "order_minimum_no_surcharge": 1000,
                "delivery_pricing": {
                    "base_price": 500,
                    "distance_ranges": [{"min": 0, "max": 1000, "price": 300}]
                }
            }
        }
    }

    # Mocking the HTTP GET request
    respx.get(mock_url).mock(return_value=Response(200, json=mock_data))

    # Test success scenario
    result = await fetchDynamicData(venue_slug)
    assert result == (
        mock_data["venue_raw"]["delivery_specs"]["order_minimum_no_surcharge"],
        mock_data["venue_raw"]["delivery_specs"]["delivery_pricing"]["base_price"],
        mock_data["venue_raw"]["delivery_specs"]["delivery_pricing"]["distance_ranges"]
    )

@pytest.mark.asyncio
@respx.mock
async def test_fetchDynamicData_invalid_slug():
    venue_slug = "invalid-venue"
    mock_url = getDynamicInformationURL(venue_slug)

    # Mocking the HTTP GET request with a 400 error
    respx.get(mock_url).mock(return_value=Response(400))

    # Test invalid slug scenario
    with pytest.raises(HTTPException) as exc_info:
        await fetchDynamicData(venue_slug)
    assert exc_info.value.status_code == 400

@pytest.mark.asyncio
@respx.mock
async def test_fetchDynamicData_server_error():
    venue_slug = "server-error-venue"
    mock_url = getDynamicInformationURL(venue_slug)

    # Mocking the HTTP GET request with a server error
    respx.get(mock_url).mock(return_value=Response(500))

    # Test server error scenario
    with pytest.raises(HTTPException) as exc_info:
        await fetchDynamicData(venue_slug)
    assert exc_info.value.status_code == 500
