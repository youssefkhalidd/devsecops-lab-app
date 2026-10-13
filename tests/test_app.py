import sqlite3
import pytest
from app1 import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    # Give each test its own temporary database.
    db_path = tmp_path / "users.db"

    monkeypatch.chdir(tmp_path)

    # Initialize the database schema and test data.
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL
        )
    """)
    conn.execute(
        "INSERT INTO users (username) VALUES (?)",
        ("testuser",)
    )
    conn.commit()
    conn.close()

    app.config["TESTING"] = True

    with app.test_client() as test_client:
        yield test_client


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
