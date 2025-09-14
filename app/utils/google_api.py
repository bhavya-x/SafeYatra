# Helper functions to call Google APIs (e.g., directions)
# Helper functions to interact with Google Maps API
import requests
import httpx
import json
from app.config import GOOGLE_MAPS_API_KEY

async def get_directions(start: str, end: str, mode=str, alternatives=True):
    """
    Call the Google Directions API to get route information.
    Returns the JSON response from the API.
    """
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": start,
        "destination": end,
        "mode": mode,
        "alternatives": alternatives,
        "key": GOOGLE_MAPS_API_KEY  # Make sure this is set correctly
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            if data["status"] != "OK":
                return {"error": data["status"]}

            result = []
            for i, route in enumerate(data.get("routes", [])):
                route_details = {
                    "route_number": i + 1,
                    "summary": route.get("summary", "No summary"),
                    "legs": []
                }

                for j, leg in enumerate(route.get("legs", [])):
                    leg_details = {
                        "leg_number": j + 1,
                        "start_address": leg["start_address"],
                        "end_address": leg["end_address"],
                        "distance": leg["distance"]["text"],
                        "duration": leg["duration"]["text"],
                        "steps": []
                    }

                    for step in leg.get("steps", []):
                        instruction = step["html_instructions"]
                        instruction = instruction.replace("<b>", "").replace("</b>", "").replace("<wbr/>", "")
                        instruction = instruction.replace('<div style="font-size:0.9em">', " ").replace('</div>', "")

                        step_data = {
                            "instruction": instruction,
                            "distance": step["distance"]["text"],
                            "duration": step["duration"]["text"],
                            "start_location": step["start_location"],
                            "end_location": step["end_location"]
                        }
                        
                        leg_details["steps"].append(step_data)

                    route_details["legs"].append(leg_details)

                result.append(route_details)

            return result  # Return the structured result

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
