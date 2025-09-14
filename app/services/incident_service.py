# Business logic for incident operations (CRUD in MongoDB)
# Handles incident operations (CRUD)
from app.database.mongo import get_incidents_collection
from bson import ObjectId  # Import ObjectId for MongoDB queries
from app.utils.google_api import get_current_location  # Import the new function

async def create_incident(incident):
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
    
    result = await incidents_collection.insert_one(incident_data)
    return str(result.inserted_id)

async def fetch_incidents(lat: float = None, lng: float = None):
    """
    Retrieve all incidents from the database and convert ObjectId to string.
    If latitude and longitude are provided, fetch incidents nearby.
    """
    incidents_collection = await get_incidents_collection()
    
    if lat is not None and lng is not None:
        # Fetch nearby incidents if location is provided
        incidents = await fetch_nearby_incidents(lat, lng)
    else:
        incidents = await incidents_collection.find().to_list(100)

    # Convert ObjectId to string for each incident
    for incident in incidents:
        incident["_id"] = str(incident["_id"])

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
