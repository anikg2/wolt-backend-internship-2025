"""
This file contains helper functions for the DOPC module. Separating these helper functions ensures modularity and assists with maintaibility.
"""
from config import HOME_API_BASE, DOPC_PORT

def getStaticInformationURL(venue_slug: str) -> str:
    """
    Remember to fill this out.
    """
    return f"{HOME_API_BASE}/{venue_slug}/static"

def getDynamicInformationURL(venue_slug: str) -> str:
    """
    Remember to fill this out
    """
    return f"{HOME_API_BASE}/{venue_slug}/dynamic"
def computeDistance(userLat: float, userLon: float, venueLat: float, venueLon: float) -> float:
    pass

def getServicePort() -> int:
    return DOPC_PORT

if __name__ == "__main__":
    print(f"DOPC is currently set to run on port: {getServicePort()}")
    print(f"Example Static URL: {getStaticInformationURL("home-assignment-venue-berlin")}")
    print(f"Example Dynamic URL: {getDynamicInformationURL("home-assignment-venue-berlin")}")