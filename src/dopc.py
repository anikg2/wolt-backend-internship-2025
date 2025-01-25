"""
This file contains the code for the DOPC service
"""
from fastapi import FastAPI, HTTPException, Query

import uvicorn
from helpers import getServicePort, computeDistance, computeDeliveryFeeAndSurcharge
from api_fetchers import fetchStaticData, fetchDynamicData

# For logging requests and error messages
import os
if not os.path.exists('logs'):
    os.mkdir('logs')
import logging
from config import DEFAULT_LOG_DIRECTORY
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler(f'{DEFAULT_LOG_DIRECTORY}/dopc.log')]) 

dopc = FastAPI()

@dopc.get("/api/v1/delivery-order-price")
async def getDeliveryOrderPrice(
    venue_slug: str = Query("", description = "The venue slug"), 
    cart_value: int = Query(-9000, description = "The cart value"), 
    user_lat: float = Query(None, description = "The user's latitude"), 
    user_lon: float = Query(None, description = "The user's longitude")
):
    """
    This is the main endpoint of the DOPC service.
    """
    # Handling of invalid or missing parameters
    invalid_params = {}
    
    if not venue_slug:
        invalid_params["venue_slug"] = ""
    if cart_value < 0:
        invalid_params["cart_value"] = cart_value
    if user_lat is None:
        invalid_params["user_lat"] = user_lat
    if user_lon is None:
        invalid_params["user_lon"] = user_lon

    if invalid_params:
        logging.error("Received invalid request")
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Invalid request. One or more parameters are missing or invalid.",
                "missing/invalid": invalid_params,
                "hint": "Please ensure to use correct parameter values",
            }
        )
    
    # Fetch the necessary parameters from the two endpoints
    # First from the Home Assignment API static URL
    venue_lon, venue_lat = await fetchStaticData(venue_slug)
    
    # Then from the Home Assignment API dynamic URL
    minimum_order_value, delivery_base_price, distance_ranges = await fetchDynamicData(venue_slug)

    # Compute the distance using the coordinates of the user and venue
    distance = computeDistance(user_lat, user_lon, venue_lat, venue_lon)

    # Finally calculate the delivery fee and return a response based on the specified format
    # If the delivery distance is too large, it has to be handled accordingly
    try:
        delivery_fee, surcharge = computeDeliveryFeeAndSurcharge(cart_value, distance, minimum_order_value, delivery_base_price, distance_ranges)
    except ValueError as e:
        logging.error(f"Delivery distance is too large. computeDeliveryFeeAndSurcharge() threw exception {e}")
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Invalid request! Delivery distance is too large! Delivery not possible!",
            }
        )
    total_delivery_price = cart_value + surcharge + delivery_fee
    return {
        "total_price": total_delivery_price,
        "small_order_surcharge": surcharge,
        "cart_value": cart_value,
        "delivery": {
            "fee": delivery_fee,
            "distance": distance
        }        
    }

if __name__ == "__main__":
    port = getServicePort()
    print(f"Started DOPC Service on port {port}")
    uvicorn.run(dopc, host="127.0.0.1", port=port)