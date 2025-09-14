# Pydantic schema for route requests
# Pydantic schema for route requests
from pydantic import BaseModel

class RouteRequest(BaseModel):
    start: str
    end: str
    mode: str  # e.g., driving, walking, cycling, scooter
