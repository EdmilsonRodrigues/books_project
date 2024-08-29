from typing import Annotated
from fastapi import APIRouter, Body, HTTPException, Path, Query
from fastapi.responses import JSONResponse
from models import Book, BookRequest

router = APIRouter(tags=["Books"])


@router.get("/api/books")
async def get_books(
    author: Annotated[
        str | None, Query(description="The author of the book", title="author")
    ] = None,
    title: Annotated[
        str | None, Query(description="The title of the book", title="title")
    ] = None,
    category: Annotated[
        str | None, Query(description="The category of the book", title="category")
    ] = None,
    rating: Annotated[int | None, Query(description="The rating of the book")] = None,
) -> list[Book]:
    return await Book.list_books(
        author=author, title=title, category=category, rating=rating
    )


@router.post("/api/books", status_code=201)
async def create_book(book: Annotated[BookRequest, Body(description="Book to create")]):

    await book.create()
    return JSONResponse(status_code=201, content={"message": "Book created"})


@router.get("/api/books/{book_id}")
async def get_book(
    book_id: Annotated[int, Path(description="The id of the book")]
) -> Book:
    book = await Book.get_by_id(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/api/books/{book_id}", status_code=204)
async def update_book(
    book_id: Annotated[int, Path(description="The id of the book")],
    updated_book: Annotated[BookRequest, Body(description="Book to update")],
):
    book = await Book.get_by_id(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    book.title = updated_book.title
    book.author = updated_book.author
    book.category = updated_book.category
    await book.update()


@router.delete("/api/books/{book_id}", status_code=204)
async def delete_book(book_id: Annotated[int, Path(description="The id of the book")]):
    book = await Book.get_by_id(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    await book.delete()
