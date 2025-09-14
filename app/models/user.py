# Pydantic schema for user data
# Pydantic schema for user data
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    username: str
    email: EmailStr
    password: str  # Note: In production, store hashed passwords!
