from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.models.user import User
from app.services.user_service import get_user_by_id, update_user
from app.services.auth_service import get_current_user

router = APIRouter()

# Use HTTPBearer for simple Bearer token authentication
security = HTTPBearer()

@router.put("/users/{user_id}/update")
async def update_user_route_no_auth(
    user_id: str,
    user_data: User
):
    """
    Update user details by user_id. No authentication required.
    """

    # Update the user data
    success = await update_user(user_id, user_data)
    if not success:
        raise HTTPException(status_code=404, detail="User not found or update failed")

    return {"detail": "User updated successfully"}

@router.put("/users/{user_id}/update/auth")
async def update_user_route_with_auth(
    user_id: str,
    user_data: User,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Update user details by user_id. Requires authentication.
    """

    # Extract the token from the Authorization header
    token = credentials.credentials

    # Validate the token and get the current user
    current_user = await get_current_user(token)
    if not current_user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    # Update the user data
    success = await update_user(user_id, user_data)
    if not success:
        raise HTTPException(status_code=404, detail="User not found or update failed")

    return {"detail": "User updated successfully"}

@router.post("/users")
async def register_user_route(user_data: User):
    """
    Register a new user. 
    """
    user_id = await save_user_data(user_data)
    if not user_id:
        raise HTTPException(status_code=400, detail="User already exists")
    return {"detail": "User registered successfully", "user_id": user_id}
