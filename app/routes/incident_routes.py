# Endpoints for incident reporting and retrieval
# Endpoints for incident reporting and retrieval
from fastapi import APIRouter, HTTPException, Depends
from app.models.incident import Incident
from app.services.incident_service import create_incident, fetch_incidents, fetch_incident_by_id, fetch_nearby_incidents
from app.services.auth_service import get_current_user
import os
import requests

router = APIRouter()

@router.post("/incidents/")
async def create_incident_route(incident: Incident, current_user: dict = Depends(get_current_user)):
    """
    Create a new incident. Requires authentication.
    """
    from datetime import datetime
    incident.reported_at = datetime.now().isoformat()
    incident_id = await create_incident(incident)
    return {"id": incident_id}

@router.get("/incidents/")
async def get_incidents_route(current_user: dict = Depends(get_current_user)):
    """
    Retrieve all reported incidents. Requires authentication.
    """
    incidents = await fetch_incidents()
    return {"incidents": incidents}

@router.get("/incidents/{incident_id}")
async def get_incident_route(incident_id: str, current_user: dict = Depends(get_current_user)):
    """
    Retrieve details of a specific incident. Requires authentication.
    """
    incident = await fetch_incident_by_id(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident

@router.get("/incidents/nearby")
async def get_nearby_incidents(lat: float, lng: float):
    """
    Retrieve incidents near a given location.
    """
    incidents = await fetch_nearby_incidents(lat, lng)
    return {"incidents": incidents}

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
