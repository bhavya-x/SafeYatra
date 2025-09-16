# Business logic for user operations
# Handles user-related operations
from app.models.user import User
from app.database.mongo import get_users_collection
from bson import ObjectId  # Import ObjectId for MongoDB queries

async def register_user(user: User):
    """
    Register a new user in the database.
    """
    users_collection = await get_users_collection()
    # Check if user exists (by email or username)
    existing = await users_collection.find_one({"email": user.email})
    if existing:
        return None  # or raise an exception
    result = await users_collection.insert_one(user.dict())
    return str(result.inserted_id)

async def update_user(user_id: str, user_data: User):
    """
    Update user details in the database.
    """
    users_collection = await get_users_collection()
    object_id = ObjectId(user_id)  # Convert string to ObjectId
    update_result = await users_collection.update_one(
        {"_id": object_id},
        {"$set": user_data.dict(exclude_unset=True)}  # Update only provided fields
    )
    return update_result.modified_count > 0  # Return True if update was successful

async def get_user_by_id(user_id: str):
    """
    Retrieve user details from the database by user_id.
    """
    users_collection = await get_users_collection()

    try:
        object_id = ObjectId(user_id)  # Convert string to ObjectId
        user = await users_collection.find_one({"_id": object_id})
        if user:
            user["_id"] = str(user["_id"])  # Convert ObjectId to string for JSON serialization
            return user
    except Exception as e:
        print(f"Error retrieving user: {e}")
        return None  # Return None if conversion fails

    return None  # User not found
