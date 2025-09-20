from app.database.mongo import get_crimes_collection
from datetime import datetime

async def update_recency():
    """
    Update the recency field for all documents in the crimes collection.
    """
    crimes_collection = await get_crimes_collection()
    current_time = datetime.utcnow()
    await crimes_collection.update_many({}, {"$set": {"recency": current_time}})
