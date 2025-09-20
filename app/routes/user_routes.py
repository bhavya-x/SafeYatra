from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.models.user import User
from app.services.user_service import get_user_by_id, update_user
from app.services.auth_service import get_current_user

router = APIRouter()

# Use HTTPBearer for simple Bearer token authentication
security = HTTPBearer()

@router.get("/users/{user_id}")
async def get_user_route(
    user_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Retrieve user details by user_id. Requires authentication.
    """
    # Extract the token from the Authorization header
    token = credentials.credentials

    # Validate the token and get the current user
    current_user = await get_current_user(token)
    if not current_user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    # Fetch the user by user_id
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@router.put("/users/{user_id}")
async def update_user_route(
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
