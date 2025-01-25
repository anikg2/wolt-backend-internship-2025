"""
This file contains helper functions for the DOPC module. Separating these helper functions ensures modularity and assists with maintaibility.
"""
import math
from config import HOME_API_BASE, DOPC_DEFAULT_PORT

def getStaticInformationURL(venue_slug: str) -> str:
    """
    This function takes a venue slug and generates the static information URL for the Home Assignment API
    """
    return f"{HOME_API_BASE}/{venue_slug}/static"

def getDynamicInformationURL(venue_slug: str) -> str:
    """
    This function takes a venue slug and generates the dynamic information URL for the Home Assignment API
    """
    return f"{HOME_API_BASE}/{venue_slug}/dynamic"

def computeDistance(userLat: float, userLon: float, venueLat: float, venueLon: float) -> int:
    """
    This function takes the latitude and longitude coordinate values of a user and a venue.
    Using Haversine Distance to compute the straight-line distance between two points.

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
    return DOPC_DEFAULT_PORT

if __name__ == "__main__":
    print(f"DOPC is currently set to run on port {getServicePort()} by default")
    print(f"Example Static URL: {getStaticInformationURL("home-assignment-venue-berlin")}")
    print(f"Example Dynamic URL: {getDynamicInformationURL("home-assignment-venue-berlin")}")