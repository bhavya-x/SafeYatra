# Business logic for route ranking using ML and external API calls
# Handles safe route recommendation and emergency/SOS features
from app.models.route import RouteRequest
from app.utils.google_api import get_directions, decode_polyline, get_directions_for_Krish
import os
from twilio.rest import Client  # Import Twilio client
from app.services.user_service import get_user_by_id
from app.services.model_service import calculate_route_safety
import json

import json

async def get_safe_routes(request: RouteRequest):
    # Fetch directions for the requested start and end points
    directions = await get_directions(request.start, request.end, request.mode)
    
    # Decode the polylines from the directions into coordinates
    decoded_coordinates = [decode_polyline(route["polyline"]) for route in directions]

    # Fetch Krish's specific location directions
    krish_ke_location = await get_directions_for_Krish(request)
    
    # Calculate safety scores for the routes
    scorer = calculate_route_safety(krish_ke_location, 14, "male")

    # Debugging scorer structure for verification
    print(f"Scorer type: {type(scorer)}")
    print(f"Scorer value: {scorer}")

    # Handle `scorer` if it's a JSON string or list of JSON strings
    if isinstance(scorer, str):
        scorer = json.loads(scorer)  # Convert JSON string to Python list of dictionaries
    elif isinstance(scorer, list) and isinstance(scorer[0], str):
        scorer = [json.loads(score) for score in scorer]  # Convert each JSON string in the list

    # Ensure scorer is now a list of dictionaries
    if not isinstance(scorer, list) or not all(isinstance(score, dict) for score in scorer):
        raise ValueError("Scorer must be a list of dictionaries after processing.")

    # Prepare the response object
    routes_response = {}
    for route, score in zip(directions, scorer):
        try:
            rank = score["rank"]
            safety_score = score["safety_score"]

            # Create a response entry for each route
            routes_response[f"route_Coordinates{rank}"] = {
                "polyline": route.get("polyline", ""),
                "coordinates": decoded_coordinates[directions.index(route)],
                "rank": rank,
                "time": route.get("duration", ""),
                "distance": route.get("distance", ""),
                "safety_score": safety_score
            }
        except KeyError as e:
            print(f"KeyError: Missing expected key in score: {e}")
            raise ValueError("Scorer does not have the required keys: 'rank' and 'safety_score'.")

    # Return the compiled routes as a dictionary
    return {"routes": routes_response}


async def get_nearest_emergency(lat: float, lng: float):
    """
    Return nearest emergency facility.
    For now, return dummy data.
    """
    return {"facility": "Nearest Hospital", "distance": "1.2 km"}

async def send_sos_alert(details: dict):
    """
    Process SOS alert: Send details to emergency contacts and police.
    Integrates with Twilio to send SMS alerts.
    """
    account_sid = os.getenv("TWILIO_ACCOUNT_SID", "")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN", "")
    twilio_number = os.getenv("TWILIO_PHONE_NUMBER", "")

    if not account_sid or not auth_token or not twilio_number:
        return {"error": "Twilio credentials missing"}

    client = Client(account_sid, auth_token)

    # Retrieve user details
    user_id = details.get("user_id")
    user = await get_user_by_id(user_id)
    
    if not user:
        return {"error": "User not found"}

    username = user.get("username", "Unknown User")
    location = "Current Location"  # Placeholder for live location

    message_body = f"URGENT\n{username} activated SOS on SafeYatra. They are in an emergency at [Location: {location}]. Please alert authorities."
    
    emergency_contacts = user.get("emergency_contacts", [])
    
    if not emergency_contacts:
        return {"error": "No emergency contacts found for user"}

    # Send SMS
    message_sids = []
    for contact in emergency_contacts:
        try:
            message = client.messages.create(
                body=message_body,
                from_=twilio_number,
                to=contact
            )
            message_sids.append(message.sid)
        except Exception as e:
            print(f"Failed to send SMS to {contact}: {e}")

    return {"alert": "SOS alert processed successfully", "message_sids": message_sids}
