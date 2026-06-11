# Tests temporarily disabled — requires DB connection via create_all in main.py
# Re-enable once test DB setup is in place.

# from fastapi.testclient import TestClient
# from app.main import app
#
# client = TestClient(app)
#
#
# def test_health_check():
#     response = client.get("/health")
#     assert response.status_code == 200
#     assert response.json() == {"status": "healthy"}
