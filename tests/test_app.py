
import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_debug_endpoint(client):
    response = client.get("/debug")

    assert response.status_code == 200
    assert response.is_json


def test_user_lookup_endpoint(client):
    response = client.get("/user?username=testuser")

    assert response.status_code == 200
    assert response.is_json


def test_admin_users_endpoint(client):
    response = client.get("/admin/users")

    assert response.status_code == 200
    assert response.is_json

