# Business logic for authentication (JWT token handling)
from app.models.user import User
from app.database.mongo import get_users_collection
from app.utils.security import hash_password, verify_password, create_access_token, verify_access_token
from fastapi import HTTPException, Depends

async def register_user(user: User):
    """
    Register a new user with hashed password.
    """
    users_collection = await get_users_collection()
    
    # Check if the user already exists
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    # Hash password before storing
    user.password = hash_password(user.password)
    result = await users_collection.insert_one(user.dict())
    return str(result.inserted_id)

async def authenticate_user(email: str, password: str):
    """
    Authenticate user by verifying the email and password.
    """
    users_collection = await get_users_collection()
    user = await users_collection.find_one({"email": email})
    
    if not user or not verify_password(password, user["password"]):
        return None  # Invalid credentials

    return user  # Return user data if authentication is successful

async def login_user(email: str, password: str):
    """
    Authenticate user and generate JWT token.
    """
    user = await authenticate_user(email, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Generate JWT token with user data
    token = create_access_token(data={"sub": user["email"]})
    return {"access_token": token, "token_type": "bearer"}

async def get_current_user(token: str):
    """
    Middleware to validate JWT tokens in protected routes.
    """
    payload = verify_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return payload  # Returns decoded user data (e.g., email)
