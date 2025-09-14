# Safe Yatra Backend

## Overview
Safe Yatra is a safe routes recommendation system focusing on women and child safety. This backend, built with FastAPI and MongoDB, provides endpoints for user management, incident reporting, safe route recommendation, and emergency alerts.

## Project Structure
- **app/config.py:** Configuration settings.
- **app/database/mongo.py:** MongoDB connection setup.
- **app/models/:** Pydantic schemas for users, incidents, and routes.
- **app/routes/:** API endpoints for authentication, user, incident, and route operations.
- **app/services/:** Business logic for authentication, user management, incident handling, and route recommendation.
- **app/utils/:** Helper functions for Google API calls and security.
- **app/main.py:** FastAPI application entry point.

## Setup Instructions
1. Install dependencies: `pip install -r requirements.txt`
2. Set environment variables for `MONGODB_URL`, `GOOGLE_MAPS_API_KEY`, and `JWT_SECRET`.
3. Run the backend: `uvicorn app.main:app --reload`
4. Access the Swagger UI at: `http://127.0.0.1:8000/docs`

## Endpoints
- **Authentication:** `/auth/login`
- **User Management:** `/users/register`, `/users/{user_id}`
- **Incident Reporting:** `/incidents/` (POST), `/incidents/` (GET), `/incidents/{incident_id}`
- **Safe Route Recommendation:** `/routes/` (POST)
- **Emergency Services:** `/routes/emergency/nearest`, `/routes/sos`

## Notes
- The ML model integration and Google API functions are placeholders for demonstration.
- Proper error handling and security enhancements are recommended for production.
