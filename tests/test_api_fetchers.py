import pytest
from fastapi import HTTPException
from dopc.api_fetchers import fetchStaticData, fetchDynamicData

@pytest.mark.asyncio
async def test_fetchStaticData_success():
    # Using a valid venue slug to simulate a successful call
    venue_slug = "home-assignment-venue-helsinki"  

    # Test success scenario
    result = await fetchStaticData(venue_slug)
    
    # Check if the result is a list of 2 float coordinates
    assert isinstance(result, list)
    assert len(result) == 2
    assert isinstance(result[0], (int, float))
    assert isinstance(result[1], (int, float))

@pytest.mark.asyncio
async def test_fetchStaticData_invalidSlug():
    # Use an invalid slug to simulate a failure
    # Expecting 404 not found from Home Assignment API
    venue_slug = "home-assignment-venue-delhi"
    with pytest.raises(HTTPException) as exc_info:
        await fetchStaticData(venue_slug)
    assert exc_info.value.status_code == 404

@pytest.mark.asyncio
async def test_fetchDynamicData_success():
    # Using a valid venue slug to simulate a success
    venue_slug = "home-assignment-venue-berlin"
    result = await fetchDynamicData(venue_slug)
    
    # Check if the result is a tuple with three elements
    assert isinstance(result, tuple)
    assert len(result) == 3
    assert isinstance(result[0], (int, float))  # Minimum order value
    assert isinstance(result[1], (int, float))  # Base delivery price
    assert isinstance(result[2], list)  # Distance ranges should be a list

@pytest.mark.asyncio
async def test_fetchDynamicData_invalidSlug():
    # Using an invalid slug to simulate a failure
    # Expecting 404 Not found from Home Assignment API
    venue_slug = "home-assignment-venue-potato"
    with pytest.raises(HTTPException) as exc_info:
        await fetchDynamicData(venue_slug)
    assert exc_info.value.status_code == 404
