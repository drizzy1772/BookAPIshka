import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_list_book_empty(client: AsyncClient):
    response = await client.get("/books")
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0

@pytest.mark.asyncio
async def test_list_book(client: AsyncClient, test_book):
    response = await client.get("/books")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["total"] == 1

@pytest.mark.asyncio
async def test_list_books_pagination(client: AsyncClient, test_book):
    response = await client.get("/books?limit=10&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert data["limit"] == 10
    assert data["offset"] == 0


@pytest.mark.asyncio
async def test_list_books_filter_by_author(client: AsyncClient, test_book, test_author):
    response = await client.get(f"/books?author_id={test_author.id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1

    response = await client.get("/books?author_id=999")
    data = response.json()
    assert len(data["items"]) == 0

@pytest.mark.asyncio
async def test_get_book_detail(client: AsyncClient, test_book):
    response = await client.get(f"/books/{test_book.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Title Book"
    assert data["price"] == 2000

@pytest.mark.asyncio
async def test_get_book_not_found(client: AsyncClient):
    response = await client.get("/books/999")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_create_book_as_admin(client: AsyncClient, admin_token, test_author):
    response = await client.post(
        "/books",
        json={
            "title": "New Book",
            "description": "Description",
            "price": 2500,
            "stock_quantity": 5,
            "author_id": test_author.id
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "New Book"
    assert data["price"] == 2500

@pytest.mark.asyncio
async def test_create_book_as_user_forbidden(client: AsyncClient, user_token, test_author):
    response = await client.post(
        "/books",
        json={
            "title": "Book",
            "description": "desc",
            "price": 1200,
            "author_id": test_author.id,
        },
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_create_book_negative_price(client: AsyncClient, admin_token, test_author):
    response = await client.post(
        "/books",
        json={
            "title": "Book",
            "description": "Desc",
            "price": -100,
            "author_id": test_author.id,
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 201

@pytest.mark.asyncio
async def test_update_book(client: AsyncClient, admin_token, test_book):
    response = await client.patch(
        f"/books/{test_book.id}",
        json={"price": 2999},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    assert response.json()["price"] == 2999

@pytest.mark.asyncio
async def test_delete_book(client: AsyncClient, admin_token, test_book):
    response = await client.delete(
        f"/books/{test_book.id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 204

    response = await client.get(f"/books/{test_book.id}")
    assert response.status_code == 404