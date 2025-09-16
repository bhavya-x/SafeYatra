from pydantic import BaseModel, EmailStr, conint
from typing import List, Optional

class User(BaseModel):
    """
    Pydantic schema for user data.
    """
    email: EmailStr
    phone_number: str  # Store as a string to support country codes (+91, etc.)
    age: int
    gender: str  # Can be restricted to "Male", "Female", "Other" if needed
    password: str

    # Additional Profile Details (Optional)
    full_name: Optional[str] = None
    vehicle_number: Optional[str] = None
    vehicle_color: Optional[str] = None
    emergency_contacts: Optional[List[str]] = []  # List of up to 5 contacts
    work_address: Optional[str] = None
    home_address: Optional[str] = None
