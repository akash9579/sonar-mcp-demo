from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_sql_injection_blocked():
    response = client.get("/users/search?query=' OR 1=1 --")
    # This should be blocked with a 400, but our vulnerable code
    # doesn't sanitize input, so it won't behave as expected
    assert response.status_code == 400

    
