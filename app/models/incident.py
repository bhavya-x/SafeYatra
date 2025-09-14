# Pydantic schema for incident data
# Pydantic schema for incident data
from pydantic import BaseModel
from typing import Optional, Dict

class Incident(BaseModel):
    location: str 
    description: str
    user_id: str
    route_info: Optional[Dict] = {}  # Can hold additional route details
    travel_mode: str
    reported_at: Optional[str] = None  # To be set during creation
