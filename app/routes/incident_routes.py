# Endpoints for incident reporting and retrieval
# Endpoints for incident reporting and retrieval
from fastapi import APIRouter, HTTPException, Depends
from app.models.incident import Incident
from app.services.incident_service import create_incident, fetch_incidents, fetch_incident_by_id, fetch_nearby_incidents
from app.services.auth_service import get_current_user

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
