from fastapi import APIRouter, HTTPException, Depends
from app.models.route import RouteRequest
from app.services.route_service import get_safe_routes, get_nearest_emergency, send_sos_alert
from app.services.auth_service import get_current_user

router = APIRouter()

@router.post("/routes/")
async def safe_route_route(request: RouteRequest, current_user: dict = Depends(get_current_user)):
    """
    Return top safe routes based on start, end, and travel mode. Requires authentication.
    """
    routes = await get_safe_routes(request)
    if not routes:
        raise HTTPException(status_code=404, detail="No safe routes found")
    return routes

@router.get("/emergency/nearest")
async def nearest_emergency(lat: float, lng: float, current_user: dict = Depends(get_current_user)):
    """
    Return the nearest emergency facility (police/hospital) for a given location. Requires authentication.
    """
    facility = await get_nearest_emergency(lat, lng)
    if not facility:
        raise HTTPException(status_code=404, detail="No emergency facility found")
    return facility

@router.post("/sos/")
async def sos_alert(details: dict, current_user: dict = Depends(get_current_user)):
    """
    Send SOS alert with live location, vehicle details to emergency contacts and police. Requires authentication.
    """
    result = await send_sos_alert(details)
    return {"status": "SOS alert sent", "result": result}
