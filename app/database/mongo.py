# MongoDB connection setup using Motor
import motor.motor_asyncio
from app.config import MONGODB_URL

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client["safe_yatra"]

async def get_users_collection():
    """Return the users collection."""
    return db["users"]

async def get_incidents_collection():
    """Return the incidents collection."""
    return db["incidents"]

async def get_clustered_collection():
    """Return the clustered collection."""
    return db["clustered"]  # Replace "clustered" with the actual collection name if different

async def get_crimes_collection():
    """Return the crimes collection."""
    return db["crimes"]
