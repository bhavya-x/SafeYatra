# MongoDB connection setup using Motor
# MongoDB connection setup using Motor (async driver)
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
