import pytest
from httpx import AsyncClient, ASGITransport
from main import app
from session import create_table


async_client = AsyncClient(
    transport=ASGITransport(app=app), base_url="http://localhost:8000", timeout=60
    )  # type: ignore


@pytest.fixture
def book_data():
    return {
        "title": "Test Book",
        "author": "Edmilson",
        "category": "Testing",
        "rating": 5,
    }


@pytest.mark.asyncio
async def test_create_table():
    assert await create_table()


@pytest.mark.asyncio
async def test_create_book(book_data):
    response = await async_client.post("/api/books", json=book_data)
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_fail_create_book(book_data):
    book_data["rating"] = 6
    response = await async_client.post("/api/books", json=book_data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_books_by_author():
    global book_id
    response = await async_client.get(
        "/api/books",
        params={
            "author": "Edmilson",
            "title": "Test Book",
            "category": "Testing",
            "rating": 5,
        },
    )
    assert response.status_code == 200
    assert response.json()[0].get("title") == "Test Book"
    book_id = response.json()[0].get("id")
    assert book_id is not None
    assert response.json()[0].get("category") == "Testing"
    assert response.json()[0].get("author") == "Edmilson"
    assert response.json()[0].get("rating") == 5


@pytest.mark.asyncio
async def test_update_book(book_data):
    book_data["rating"] = 0
    response = await async_client.put(f"/api/books/{book_id}", json=book_data)
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_fail_get_book():
    response = await async_client.get(f"/api/books/{book_id}")
    assert response.status_code == 200
    assert response.json().get("title") == "Test Book"
    assert response.json().get("id") is not None
    assert response.json().get("category") == "Testing"
    assert response.json().get("author") == "Edmilson"
    assert response.json().get("rating") == 5


@pytest.mark.asyncio
async def test_get_book():
    response = await async_client.get("/api/books/0")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_book():
    response = await async_client.delete(
        f"/api/books/{book_id}",
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_fail_delete_book():
    response = await async_client.delete(
        f"/api/books/{book_id}",
    )
    assert response.status_code == 404
