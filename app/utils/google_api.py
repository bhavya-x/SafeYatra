# Helper functions to call Google APIs (e.g., directions)
# Helper functions to interact with Google Maps API
import requests
import httpx
import json
from app.config import GOOGLE_MAPS_API_KEY
from app.models.route import RouteRequest

async def get_directions(start: str, end: str, mode: str = "driving", alternatives: bool = True):

    """
    Call the Google Directions API to get route information.
    Returns a list of dictionaries containing the top routes with their polyline strings, ranks, times, and distances.


    """
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params: dict = {

        "origin": start,
        "destination": end,
        "mode": mode,
        "alternatives": alternatives,
        "key": "AIzaSyDf34ue6DB4ukLmPqY09YJsZ4FXW_vs98Y"

    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            if data["status"] != "OK":
                return {"error": data["status"]}

            # Extract polylines from the routes

            if data.get("routes"):
                top_routes = []
                for route in data["routes"]:  # Get all routes

                    polyline = route.get("overview_polyline", {}).get("points", "")
                    rank = route.get("rank", None)
                    duration = route.get("legs", [{}])[0].get("duration", {}).get("text", "")
                    distance = route.get("legs", [{}])[0].get("distance", {}).get("text", "")
                    top_routes.append({
                        "polyline": polyline,
                        "rank": rank,
                        "duration": duration,
                        "distance": distance
                    })
                return top_routes  # Return the list of top 3 routes


            return ""  # Return empty if no routes found

        else:
            return {"error": "Failed to fetch directions"}

    except httpx.RequestError as exc:
        return {"error": f"An error occurred while requesting directions: {str(exc)}"}

async def get_directions_for_Krish(request: RouteRequest):
    """
    Call Google Directions API to fetch routes, then return the results in a structured format.
    """
    try:
        # Construct the API request URL
        api_key = "AIzaSyDf34ue6DB4ukLmPqY09YJsZ4FXW_vs98Y"  # Replace with your actual API key
        url = (
            f"https://maps.googleapis.com/maps/api/directions/json"
            f"?origin={request.start}&destination={request.end}"
            f"&mode={request.mode}&alternatives=true&key={api_key}"
        )
        
        # Make the API request
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        # Parse the JSON response
        directions = response.json()

        # Debugging: Print the raw response from the API
        # print("Raw directions response:", directions)

        # Initialize the final response
        routes_response = []

        # Check if routes are present in the API response
        if "routes" in directions and directions["routes"]:
            for i, route in enumerate(directions["routes"], start=1):
                # Initialize a dictionary for the route
                route_details = {
                    "route_number": i,
                    "legs": []
                }

                # Process each leg in the route
                for leg in route["legs"]:
                    leg_details = {
                        "start_location": {
                            "address": leg["start_address"],
                            "lat": leg["start_location"]["lat"],
                            "lng": leg["start_location"]["lng"]
                        },
                        "end_location": {
                            "address": leg["end_address"],
                            "lat": leg["end_location"]["lat"],
                            "lng": leg["end_location"]["lng"]
                        },
                        "steps_count": len(leg["steps"]),
                        "steps": []
                    }

                    # Process each step in the leg
                    for step in leg["steps"]:
                        step_details = {
                            "instruction": step["html_instructions"],
                            "distance": step["distance"]["text"],
                            "duration": step["duration"]["text"],
                            "start_location": {
                                "lat": step["start_location"]["lat"],
                                "lng": step["start_location"]["lng"]
                            },
                            "end_location": {
                                "lat": step["end_location"]["lat"],
                                "lng": step["end_location"]["lng"]
                            }
                        }
                        leg_details["steps"].append(step_details)

                    # Add the leg details to the route
                    route_details["legs"].append(leg_details)

                # Add the route details to the response
                routes_response.append(route_details)
        # print(routes_response)
        return routes_response

    except Exception as e:
        print(f"Error getting directions: {str(e)}")
        return {"error": "Failed to fetch directions", "details": str(e)}

def decode_polyline(encoded):
    """
    Decodes a Google Maps encoded polyline into a list of (latitude, longitude) tuples.
    This method handles decoding correctly, keeping more detailed points.
    """
    polyline = []
    index = 0
    lat = 0
    lng = 0
    length = len(encoded)
    
    while index < length:
        # Decode latitude
        shift = 0
        result = 0
        while True:
            byte = ord(encoded[index]) - 63
            index += 1
            result |= (byte & 0x1f) << shift
            shift += 5
            if byte < 0x20:
                break
        delta_lat = (result & 1) != 0 and ~(result >> 1) or (result >> 1)
        lat += delta_lat

        # Decode longitude
        shift = 0
        result = 0
        while True:
            byte = ord(encoded[index]) - 63
            index += 1
            result |= (byte & 0x1f) << shift
            shift += 5
            if byte < 0x20:
                break
        delta_lng = (result & 1) != 0 and ~(result >> 1) or (result >> 1)
        lng += delta_lng
        
        # Append the decoded lat/lng as a tuple
        polyline.append((lat / 1E5, lng / 1E5))

    return polyline

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