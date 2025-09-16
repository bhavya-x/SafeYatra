# Global configuration settings (DB URL, API keys)
# Configuration settings for Safe Yatra
import os

# MongoDB connection URI (can be set via environment variable)
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb+srv://bhavyajain035:password1234@cluster0.qs1fe.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Google Maps API Key (set via environment variable in production)
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# Twilio Configuration
TWILIO_SID = os.getenv("TWILIO_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "")

# JWT Secret Key for token generation (replace with secure value)
JWT_SECRET = os.getenv("JWT_SECRET", "my_very_strong_secret_2803")
# JWT Algorithm
JWT_ALGORITHM = "HS256"
# Token expiration time (e.g., 30 minutes)
ACCESS_TOKEN_EXPIRE_MINUTES = 30
