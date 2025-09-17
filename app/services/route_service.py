# Business logic for route ranking using ML and external API calls
# Handles safe route recommendation and emergency/SOS features
from app.models.route import RouteRequest
from app.utils.google_api import get_directions, decode_polyline
import os
from twilio.rest import Client  # Import Twilio client
from app.services.user_service import get_user_by_id

async def get_safe_routes(request: RouteRequest):
    """
    Call Google Directions API to fetch routes, then rank them using an ML model.
    Here, we return dummy data for demonstration.
    """
    # Get routes from Google Maps (passing the extracted start and end from the request)
    directions = await get_directions(request.start, request.end, request.mode)
    decoded_coordinates = decode_polyline(directions)

    return {"Polyline_String": directions, "route_Coordinates": decoded_coordinates}

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
