import pytest
from fastapi import status

def test_register_user(client, test_user):
    response = client.post("/register", json=test_user)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "email" in data
    assert data["email"] == test_user["email"]

def test_register_duplicate_user(client, test_user):
    # First registration
    client.post("/register", json=test_user)
    # Second registration with same email
    response = client.post("/register", json=test_user)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_login_user(client, test_user):
    # Register user first
    client.post("/register", json=test_user)
    # Login
    response = client.post(
        "/token",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(client, test_user):
    response = client.post(
        "/token",
        data={
            "username": test_user["email"],
            "password": "wrongpassword"
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED 