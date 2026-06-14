import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_order_success(client: AsyncClient, user_token, test_book):
    response = await client.post(
        "/orders",
        json={"book_id": test_book.id, "quantity": 2},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["quantity"] == 2
    assert data["total_price"] == test_book.price * 2

@pytest.mark.asyncio
async def test_create_order_unauthorized(client: AsyncClient, test_book):
    response = await client.post(
        "/orders",
        json={"book_id": test_book.id, "quantity": 1},
    )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_create_order_book_not_found(client: AsyncClient, user_token):
    response = await client.post(
        "/orders",
        json={"book_id": 999, "quantity": 1},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_create_order_insufficient_stock(client: AsyncClient, user_token, test_book):
    response = await client.post(
        "/orders",
        json={"book_id": test_book.id, "quantity": 100},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 400
    assert "Not enough stock" in response.json()["detail"]

@pytest.mark.asyncio
async def test_crate_order_zero_quantity(client: AsyncClient, user_token, test_book):
    response = await client.post(
        "/orders",
        json={"book_id": test_book.id, "quantity": 0},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_order_decreases_stock(client: AsyncClient, user_token, test_book, db_session):
    initial_stock = test_book.stock_quantity
    await client.post(
        "/orders",
        json={"book_id": test_book.id, "quantity": 3},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    await db_session.refresh(test_book)
    assert test_book.stock_quantity == initial_stock - 3