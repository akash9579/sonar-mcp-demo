from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_users_search_requires_authentication():
    response = client.get("/users/search", params={"query": "alice"})
    assert response.status_code == 401
