"""Authentication API tests."""
from fastapi.testclient import TestClient

from app.database.db import engine
from app.main import app
from app.models.models import Base


def client() -> TestClient:
    """Create a clean test client with a reset database."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    return TestClient(app)


def test_register_user() -> None:
    """Registering a new user should succeed."""
    with client() as test_client:
        response = test_client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "password": "securepassword123",
            },
        )

    assert response.status_code == 200
    assert response.json()["message"] == "User registered successfully"


def test_register_duplicate_email() -> None:
    """Registering the same email twice should fail."""
    with client() as test_client:
        test_client.post(
            "/auth/register",
            json={
                "email": "duplicate@example.com",
                "password": "password123",
            },
        )
        response = test_client.post(
            "/auth/register",
            json={
                "email": "duplicate@example.com",
                "password": "password456",
            },
        )

    assert response.status_code == 400


def test_login() -> None:
    """Logging in with valid credentials should return a token."""
    with client() as test_client:
        test_client.post(
            "/auth/register",
            json={
                "email": "login@example.com",
                "password": "password123",
            },
        )
        response = test_client.post(
            "/auth/login",
            json={
                "email": "login@example.com",
                "password": "password123",
            },
        )

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_invalid_credentials() -> None:
    """Invalid credentials should be rejected."""
    with client() as test_client:
        response = test_client.post(
            "/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "wrongpassword",
            },
        )

    assert response.status_code == 401
