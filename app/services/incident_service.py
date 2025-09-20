# Business logic for incident operations (CRUD in MongoDB)
from app.database.mongo import get_incidents_collection
from bson import ObjectId
from app.utils.google_api import get_current_location
from app.models.incident import Incident  # Importing the Incident model

async def create_incident(incident: Incident):
    """
    Insert a new incident into the incidents collection.
    Automatically fetches the user's current location.
    """
    incidents_collection = await get_incidents_collection()
    
    # Fetch the user's current location
    lat, lng = get_current_location()
    
    # Include the location in the incident data
    incident_data = incident.dict()
    incident_data['location'] = {
        'lat': lat,
        'lng': lng
    }

    result = await incidents_collection.insert_one(incident_data)  # Store incident data in the incidents collection
    return str(result.inserted_id)

async def save_incident_data(incident: Incident):
    """
    Save incident data to the incidents collection.
    """
    incidents_collection = await get_incidents_collection()
    result = await incidents_collection.insert_one(incident.dict())  # Save incident data to the incidents collection
    return str(result.inserted_id)

async def fetch_incidents():
    """
    Retrieve all incidents from the incidents collection.
    """
    incidents_collection = await get_incidents_collection()
    incidents = await incidents_collection.find().to_list(100)  # Fetch the first 100 incidents
    for incident in incidents:
        incident["_id"] = str(incident["_id"])  # Convert ObjectId to string for JSON serialization
    return incidents

async def fetch_incident_by_id(incident_id: str):
    """
    Retrieve a single incident by its ID and convert ObjectId to string.
    """
    incidents_collection = await get_incidents_collection()

    try:
        object_id = ObjectId(incident_id)  # Convert string to ObjectId
        incident = await incidents_collection.find_one({"_id": object_id})

        if incident:
            incident["_id"] = str(incident["_id"])  # Convert ObjectId to string for JSON serialization
            return incident
    except Exception as e:
        print(f"Error retrieving incident: {e}")
        return None  # Return None if conversion fails

    return None  # Return None if no incident is found

async def fetch_nearby_incidents(lat: float, lng: float):
    """
    Retrieve incidents near a given latitude and longitude.
    Note: This is a placeholder; use geospatial queries if needed.
    """
    incidents_collection = await get_incidents_collection()
    # Example: Return first 10 incidents (replace with proper geospatial query)
    incidents = await incidents_collection.find().to_list(10)
    return incidents
