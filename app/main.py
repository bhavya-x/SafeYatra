from fastapi import FastAPI
from app.routes.auth_routes import router as auth_router
from app.routes.user_routes import router as user_router
from app.routes.incident_routes import router as incident_router
from app.routes.route_routes import router as route_router
from app.database.mongo import get_users_collection, get_incidents_collection
import motor.motor_asyncio
from app.config import MONGODB_URL
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(
    title="Safe Yatra Backend",
    description="Backend for Safe Yatra, a safe routes recommendation system.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (Change this in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers for different functionalities
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(incident_router, prefix="/incidents", tags=["Incidents"])
app.include_router(route_router, prefix="/routes", tags=["Routes"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

