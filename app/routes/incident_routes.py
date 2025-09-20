import os
import shutil
import requests
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from pymongo import MongoClient
from bson import ObjectId
from app.models.incident import Incident
from app.services.auth_service import get_current_user

router = APIRouter()

# ✅ Enter your MongoDB connection string here:
MONGO_CONNECTION_URL = "mongodb+srv://bhavyajain035:password1234@cluster0.qs1fe.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_CONNECTION_URL)
db = client["afe_yatra"]  # ✅ Replace with your actual DB name
collection = db["Incidents"]  # ✅ Connecting to the existing "incidents" collection

# Ensure the 'uploads' directory exists for storing images
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/incidents/")
async def create_incident_route(incident: Incident, current_user: dict = Depends(get_current_user)):
    """
    Create a new incident and store it in MongoDB. Requires authentication.
    """
    incident_dict = incident.dict()
    incident_dict["reported_at"] = datetime.now().isoformat()

    # Insert incident into MongoDB
    result = collection.insert_one(incident_dict)

    return {"id": str(result.inserted_id)}


@router.post("/incidents/{incident_id}/upload/")
async def upload_image_route(
    incident_id: str,
    image_file: UploadFile = File(...),  # ✅ Separate file upload
    current_user: dict = Depends(get_current_user)
):
    """
    Upload an image and attach it to an existing incident in MongoDB. Requires authentication.
    """
    # Check if the incident exists
    incident = collection.find_one({"_id": ObjectId(incident_id)})
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    # Save the uploaded image to the local directory
    image_filename = f"{incident_id}_{image_file.filename}"
    image_path = os.path.join(UPLOAD_DIR, image_filename)

    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image_file.file, buffer)

    # Update MongoDB document with the image filename
    collection.update_one({"_id": ObjectId(incident_id)}, {"$set": {"image_url": image_filename}})

    return {"incident_id": incident_id, "image_url": f"/uploads/{image_filename}"}


@router.get("/incidents/")
async def get_incidents_route(current_user: dict = Depends(get_current_user)):
    """
    Retrieve all reported incidents from MongoDB. Requires authentication.
    """
    incidents = list(collection.find({}))
    for incident in incidents:
        incident["_id"] = str(incident["_id"])  # Convert ObjectId to string
        if "image_url" in incident:
            incident["image_url"] = f"/uploads/{incident['image_url']}"  # Convert filename to URL

    return {"incidents": incidents}


@router.get("/incidents/{incident_id}")
async def get_incident_route(incident_id: str, current_user: dict = Depends(get_current_user)):
    """
    Retrieve details of a specific incident from MongoDB. Requires authentication.
    """
    incident = collection.find_one({"_id": ObjectId(incident_id)})
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    incident["_id"] = str(incident["_id"])  # Convert ObjectId to string
    if "image_url" in incident:
        incident["image_url"] = f"/uploads/{incident['image_url']}"

    return incident


@router.get("/incidents/nearby")
async def get_nearby_incidents(lat: float, lng: float):
    """
    Retrieve incidents near a given location (dummy function).
    """
    incidents = list(collection.find({}))  # Replace with actual geospatial query if needed
    return {"incidents": incidents}


@router.post("/incidents/report")
async def report_incident_route(incident: Incident, current_user: dict = Depends(get_current_user)):
    """
    Report a new incident and store it in MongoDB. Requires authentication.
    """
    incident_dict = incident.dict()
    incident_dict["reported_at"] = datetime.now().isoformat()

    result = collection.insert_one(incident_dict)

    return {"detail": "Incident reported successfully", "incident_id": str(result.inserted_id)}


GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")


@router.get("/search-location/")
async def search_location(query: str):
    """
    Fetch location suggestions from Google Maps API based on user query.
    """
    url = f"https://maps.googleapis.com/maps/api/place/autocomplete/json?input={query}&key={GOOGLE_MAPS_API_KEY}"

    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching location data")

    return data

