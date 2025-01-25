"""
This file contains helper functions for the DOPC module. Separating these helper functions ensures modularity and assists with maintaibility.
"""
import math
from dopc.config import HOME_API_BASE, DOPC_DEFAULT_PORT

def getStaticInformationURL(venue_slug: str) -> str:
    """
    This function takes a venue slug and generates the static information URL for the Home Assignment API

    Parameters:
        venue_slug: A string that uniquely identifies a venue
    Returns:
        static_url: A URL for the Home Assignment API static information, parameterized with the venue_slug
    """
    return f"{HOME_API_BASE}/{venue_slug}/static"

def getDynamicInformationURL(venue_slug: str) -> str:
    """
    This function takes a venue slug and generates the dynamic information URL for the Home Assignment API

    Parameters:
        venue_slug: A string that uniquely identifies a venue
    Returns:
        dynamic_url: A URL for the Home Assignment API dynamic information, parameterized with the venue_slug
    """
    return f"{HOME_API_BASE}/{venue_slug}/dynamic"

def computeDistance(userLat: float, userLon: float, venueLat: float, venueLon: float) -> int:
    """
    This function takes the latitude and longitude coordinate values of a user and a venue.
    Using Haversine Distance to compute the straight-line distance between two points.
    Please refer to the provided documentation for a more detailed explanation of formulas.

    Parameters:
        userLat: A float value of the user's latitude coordinate in degrees
        userLon: A float value of the user's longitude coordinate in degrees
        venueLat: A float value of the venue's latitude coordinate in degrees
        venueLon: A float value of the venue's longitude coordinate in degrees
    Returns:
        distance: An integer value of the straight line distance between the user and venue
    """
    # Earth's radius is approximately 6371 kilometres
    earth_radius = 6371000 # In metres
    
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [userLat, userLon, venueLat, venueLon])
    
    # Compute difference in coordinates
    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1
    
    # Haversine formula - Compute a and c terms
    a = math.sin(delta_lat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # Multiply c by earth's radius to get the distance
    distance = earth_radius * c

    # Return rounded distance
    return round(distance)

def computeDeliveryFeeAndSurcharge(cart_value: int, distance: int, minimum_order_value: float, delivery_base_price: float, distance_ranges: list):
    """
    A function that computes the delivery fee and surcharge for a given cart_value and distance,
    based on the information returned by the Home Assignment API dynamic URL.
    If the delivery is outside the range of available values, an exception is thrown which is handled by DOPC.

    Parameters:
        cart_value: An integer representing the input cart_value passed to DOPC
        distance: An integer, denoting the straight line distance between user and venue
        minimum_order_value: Provided by Home Assignment API dyamic URL. No details were specified, so assuming float
        delivery_base_value: Provided by Home Assignment API dyamic URL. No details were specified, so assuming float
        distance_ranges: A range of distance values provided by the Home Assignment API dynamic URL
    Returns:
        delivery_fee: An integer, computed based on the given formula in the document
        surcharge: An integer computed based on the given instructions
    """
    # The given formula is delivery_fee = base_price + a + b * distance / 10
    # First, find the appropriate range
    exceeded_delivery_range_flag = True
    for idx in range(len(distance_ranges)-1):
        distance_range = distance_ranges[idx]
        if distance >= distance_range["min"] and distance < distance_range["max"]:
            delivery_fee = round(delivery_base_price + distance_range["a"] + distance_range["b"] * distance / 10)
            exceeded_delivery_range_flag = False
            break
    
    # Also get the surcharge
    surcharge = round(minimum_order_value - cart_value) if minimum_order_value > cart_value else 0

    # Handle situation if delivery distance is exceeded
    if exceeded_delivery_range_flag:
        raise ValueError("The delivery distance is too large! Delivery not possible!")

    return delivery_fee, surcharge


def getServicePort() -> int:
    """
    A helper function to fetch the default port configuration from the config file.
    """
    return DOPC_DEFAULT_PORT

if __name__ == "__main__":
    print(f"DOPC is currently set to run on port {getServicePort()} by default")
    print(f"Example Static URL: {getStaticInformationURL("home-assignment-venue-berlin")}")
    print(f"Example Dynamic URL: {getDynamicInformationURL("home-assignment-venue-berlin")}")