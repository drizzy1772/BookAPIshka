import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    response = await client.post(
        "/auth/register",
        json={
            "username": "username123",
            "email": "user.email@example.com",
            "password": "password123",
        },
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "username123"
    assert data["email"] == "user.email@example.com"
    assert "password" not in data

@pytest.mark.asyncio
async def test_register_duplicate_name(client: AsyncClient, test_user):
    response = await client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "another.user@gmail.com",
            "password": "password123",
        },
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()

@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, test_user):
    response = await client.post(
        "/auth/login",
        json={
            "username": "testuser",
            "password": "testpass123",
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"