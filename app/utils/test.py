# import pytest
# from fastapi.testclient import TestClient
# from app.main import app



# client = TestClient(app)

# def test_get_safe_routes():
#     response = client.post("/routes/", json={"start": "Location A", "end": "Location B", "mode": "driving"})
#     assert response.status_code == 200
#     assert "routes" in response.json()
#     assert len(response.json()["routes"]) == 3  # Check if we get top 3 routes
#     for route in response.json()["routes"]:
#         assert "polyline" in route
#         assert "rank" in route
#         assert "duration" in route
#         assert "distance" in route
