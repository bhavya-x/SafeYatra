from fastapi import APIRouter, HTTPException, Depends
from app.models.user import User
from app.services.auth_service import authenticate_user, create_access_token, register_user, get_current_user, login_user
from app.utils.security import verify_access_token

router = APIRouter()

@router.post("/register")
async def register(user: User):
    """
    Register a new user and store hashed password.
    """
    user_id = await register_user(user)
    if not user_id:
        raise HTTPException(status_code=400, detail="User already exists")
    return {"message": "User registered successfully", "user_id": user_id}

@router.post("/login")
async def login(user: User):
    """
    Authenticate user and return a JWT token.
    """
    token = await login_user(user.email, user.password)
    return token

@router.get("/profile")
async def get_profile(token: str):
    """
    Example protected route. Returns user profile if authenticated.
    """
    current_user = await get_current_user(token)
    return {"message": "Welcome!", "user": current_user}
