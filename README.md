<div align="center">

# 🚦 SafeYatra — Backend

**FastAPI + MongoDB backend for the Safe-Yatra safe-route recommendation platform (women & child safety).**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Database-47A248?style=flat-square&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![Render](https://img.shields.io/badge/Render-Deployed-46E3B7?style=flat-square&logo=render&logoColor=white)](https://render.com/)

</div>

---

## Overview

The SafeYatra backend exposes APIs for user management, incident reporting, safe-route recommendation, and emergency alerts. It is built with FastAPI, persists data in MongoDB, and integrates with Google Maps for routing and geocoding.

## Features

- 🔐 **Authentication** — JWT-based login for users and emergency contacts
- 🚨 **Incident reporting** — geo-tagged reports with categorisation
- 🗺️ **Safe-route recommendation** — weights routes against incident density and crime data
- 🆘 **Emergency endpoints** — nearest emergency services + SOS broadcast
- 📋 **Auto-generated docs** — Swagger UI at `/docs`

## API Surface

| Group | Endpoints |
|---|---|
| Auth | `POST /auth/login` |
| Users | `POST /users/register`, `GET /users/{user_id}` |
| Incidents | `POST /incidents/`, `GET /incidents/`, `GET /incidents/{id}` |
| Routes | `POST /routes/` |
| Emergency | `GET /routes/emergency/nearest`, `POST /routes/sos` |

## Project Layout

```
app/
├── config.py                # Environment & settings
├── database/mongo.py        # Mongo connection
├── models/                  # Pydantic schemas (user, incident, route)
├── routes/                  # API endpoints
├── services/                # Business logic (auth, crime, route, ...)
├── utils/                   # Google Maps + security helpers
└── main.py                  # FastAPI entrypoint
```

## Getting Started

```bash
git clone https://github.com/bhavya-x/SafeYatra.git
cd SafeYatra
pip install -r requirements.txt

export MONGODB_URL="mongodb+srv://..."
export GOOGLE_MAPS_API_KEY="..."
export JWT_SECRET="$(openssl rand -hex 32)"

uvicorn app.main:app --reload
# Swagger at http://127.0.0.1:8000/docs
```

## Deployment

`render.yaml` is included for one-click deploys on Render. Configure the environment variables above in the Render dashboard.

## Roadmap

- [ ] Replace placeholder ML scoring with trained route-risk model
- [ ] Realtime SOS via WebSockets
- [ ] Rate limiting and audit logging
- [ ] Admin dashboard
