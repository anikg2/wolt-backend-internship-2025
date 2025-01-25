"""
This file contains functions that fetch data from the static and dynamic Home Assignment API endpoints.
Modularizing the application by separating these functions helps to test and maintain the application better.
"""
import httpx
from fastapi import HTTPException
from dopc.helpers import getStaticInformationURL, getDynamicInformationURL

# For logging requests and error messages
import os
if not os.path.exists('logs'):
    os.mkdir('logs')
import logging
from dopc.config import DEFAULT_LOG_DIRECTORY
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler(f'{DEFAULT_LOG_DIRECTORY}/home_api.log')])  # Log file will be created in 'logs' directory


async def fetchStaticData(venue_slug: str):
    """
    This function makes a GET request to the Home Assignment API Static URL and
    fetches the venue's coordinates. It is capable of handling exceptions due to
    invalid requests to the API, as well as server errors.
    
    Parameters:
        venue_slug: A string that uniquely identifies a venue
    Returns:
        venue_coordinates: A list containing two floats venue_lon and venue_lat
    """
    staticInformationURL = getStaticInformationURL(venue_slug)
    try:
        # Make an asynchronous GET request to the static URL
        async with httpx.AsyncClient() as client:
            response = await client.get(staticInformationURL)
        # If the GET request to the returns 200, get the venue's longitude and latitude values
        if response.status_code == 200:
            logging.info(f"Static URL returned 200 for slug: {venue_slug}")
            static_data = response.json()
            venue_coordinates = static_data["venue_raw"]["location"]["coordinates"]
            return venue_coordinates
        # Otherwise, raise an exception because the value of venue_slug is incorrect
        else:
            logging.error(f"Static URL returned {response.status_code} for slug: {venue_slug}")
            raise HTTPException(status_code=response.status_code, detail=f"Error fetching data from Home Assignment API static URL. Please check the value of venue_slug.")
    except httpx.RequestError as e:
        # Handle any errors of Home Assignment API
        logging.error(f"Static URL returned 500 code for slug: {venue_slug}")
        raise HTTPException(status_code=500, detail=f"Error during request to Home Assignment Static API. Server returned: {e}")
    
async def fetchDynamicData(venue_slug: str):
    """
    This function makes a GET request to the Home Assignment API Dynamic URL and
    fetches the minimum order value, delivery base price, and list of distance ranges. 
    It is capable of handling exceptions due to invalid requests to the API, as well as server errors.

    Parameters:
        venue_slug: A string that uniquely identifies a venue
    Returns:
        minimum_order_value: The minimum cart_value required to avoid a surcharge fee
        delivery_base_price: The base fee for a delivery
        distance_ranges: A list containing distance ranges to compute delivery fee
    """
    dynamicInformationURL = getDynamicInformationURL(venue_slug)
    try:
        # Make an asynchronous GET request to the dynamic URL
        async with httpx.AsyncClient() as client:
            response = await client.get(dynamicInformationURL)
        # If the GET request returns 200, get the venue's three dynamic params
        if response.status_code == 200:
            logging.info(f"Dynamic URL returned 200 for slug: {venue_slug}")
            dynamic_data = response.json()
            minimum_order_value = dynamic_data["venue_raw"]["delivery_specs"]["order_minimum_no_surcharge"]
            delivery_base_price = dynamic_data["venue_raw"]["delivery_specs"]["delivery_pricing"]["base_price"]
            distance_ranges = dynamic_data["venue_raw"]["delivery_specs"]["delivery_pricing"]["distance_ranges"]
            return minimum_order_value, delivery_base_price, distance_ranges
        # Otherwise, raise an exception because the value of venue_slug is incorrect
        else:
            logging.error(f"Dynamic URL returned {response.status_code} for slug: {venue_slug}")
            raise HTTPException(status_code=response.status_code, detail="Error fetching data from Home Assignment API dynamic URL. Please check the value of venue_slug.")
    except httpx.RequestError as e:
        # Handle any errors of Home Assignment API
        logging.error(f"Dynamic URL returned 500 code for slug: {venue_slug}")
        raise HTTPException(status_code=500, detail=f"Error during request to Home Assignment Dynamic API. Server returned: {e}")