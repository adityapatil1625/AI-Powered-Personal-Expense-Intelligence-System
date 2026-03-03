"""Tests for authentication API."""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_register_user():
    """Test user registration."""
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "securepassword123"
        }
    )
    assert response.status_code == 200
    assert "message" in response.json()


def test_register_duplicate_email():
    """Test registering with duplicate email."""
    client.post(
        "/auth/register",
        json={
            "email": "duplicate@example.com",
            "password": "password123"
        }
    )
    response = client.post(
        "/auth/register",
        json={
            "email": "duplicate@example.com",
            "password": "password456"
        }
    )
    assert response.status_code == 400


def test_login():
    """Test user login."""
    # Register first
    client.post(
        "/auth/register",
        json={
            "email": "login@example.com",
            "password": "password123"
        }
    )
    # Try login
    response = client.post(
        "/auth/login",
        json={
            "email": "login@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_invalid_credentials():
    """Test login with invalid credentials."""
    response = client.post(
        "/auth/login",
        json={
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401
