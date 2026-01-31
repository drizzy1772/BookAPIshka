import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_list_authors_empty(client: AsyncClient):
    response = await client.get("/authors")
    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.asyncio
async def test_list_authors(client: AsyncClient, test_author):
    response = await client.get("/authors")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Test Author"

@pytest.mark.asyncio
async def test_create_author_as_admin(client: AsyncClient, admin_token):
    response = await client.post(
        "/authors",
        json={
            "name": "New Author",
            "bio": "bio text",
            "birth_date": "1985-05-12",
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "New Author"

@pytest.mark.asyncio
async def test_create_author_as_user_forbidden(client: AsyncClient, user_token):
    response = await client.post(
        "authors",
        json={
            "name": "Another Autor",
            "bio": "Bio",
            "birth_date": "1990-06-04",
        },
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_create_author_unauthorized(client: AsyncClient):
    response = await client.post(
        "/authors",
        json={
            "name": "Author",
            "bio": "bio",
            "birth_date": "1980-01-11",
        },
    )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_get_author_detail(client: AsyncClient, test_author):
    response = await client.get(f"/authors/{test_author.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Author"
    assert "books" in data

@pytest.mark.asyncio
async def test_author_not_found(client: AsyncClient):
    response = await client.get("/authors/999")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_create_author_future_birth_date(client: AsyncClient, admin_token):
    response = await client.post(
        "/authors",
        json={
            "name": "Created Author",
            "bio": "bio",
            "birth_date": "2093-05-020",
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 422
