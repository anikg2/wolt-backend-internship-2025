"""
This file contains the code for the DOPC service
"""
from fastapi import FastAPI, HTTPException
import httpx
import uvicorn
from helpers import getServicePort, getStaticInformationURL, getDynamicInformationURL

dopc = FastAPI()


# Remember to handle edge case when one of these values are not specified
@dopc.get("/api/v1/delivery-order-price")
async def getDeliveryOrderPrice(venue_slug: str, cart_value: int, user_lat: float, user_lon: float):
    """
    This is the main endpoint of the DOPC service.
    """
    if not venue_slug or not cart_value or not user_lat or not user_lon:
        raise HTTPException(status_code=400, detail=f"Invalid request")
    
    # Get the static and dynamic URLs for the Home Assignment API based on the venue_slug
    staticInformationURL = getStaticInformationURL(venue_slug)
    dynamicInformationURL = getDynamicInformationURL(venue_slug)

    try:
        # Make an asynchronous GET request to the static URL
        async with httpx.AsyncClient() as client:
            response = await client.get(staticInformationURL)

        # If the GET request to the static API was successful, parse the JSON response
        if response.status_code == 200:
            static_data = response.json()
            return {"message": "Data from external API", "data": static_data["venue_raw"]["location"]["coordinates"]}
        else:
            raise HTTPException(status_code=response.status_code, detail="Error fetching data from external API")
    except httpx.RequestError as e:
        # Handle any HTTP request exceptions
        raise HTTPException(status_code=500, detail=f"Error during API request: {e}")

if __name__ == "__main__":
    port = getServicePort()
    print(f"Started DOPC Service on port {port}")
    uvicorn.run(dopc, host="127.0.0.1", port=port)