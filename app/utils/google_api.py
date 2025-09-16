# Helper functions to call Google APIs (e.g., directions)
# Helper functions to interact with Google Maps API
import requests
import httpx
import json
from app.config import GOOGLE_MAPS_API_KEY

async def get_directions(start: str, end: str, mode=str, alternatives=True):
    """
    Call the Google Directions API to get route information.
    Returns the polyline string of the top route.
    """
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": start,
        "destination": end,
        "mode": mode,
        "alternatives": alternatives,
        "key": GOOGLE_MAPS_API_KEY
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            if data["status"] != "OK":
                return {"error": data["status"]}

            # Extract polyline from the first route
            if data.get("routes"):
                top_route = data["routes"][0]
                polyline = top_route.get("overview_polyline", {}).get("points", "")
                return polyline  # Return the polyline string

            return ""  # Return empty if no routes found

        else:
            return {"error": "Failed to fetch directions"}

    except httpx.RequestError as exc:
        return {"error": f"An error occurred while requesting directions: {str(exc)}"}

def get_current_location():
    """
    Fetch the user's current location using Google Maps Geolocation API.
    Returns a tuple of (latitude, longitude).
    """
    url = "https://www.googleapis.com/geolocation/v1/geolocate?key=" + GOOGLE_MAPS_API_KEY
    response = requests.post(url)
    
    if response.status_code == 200:
        location = response.json().get('location', {})
        lat = location.get('lat')
        lng = location.get('lng')
        return lat, lng
    else:
        return None, None  # Return None if location cannot be fetched
