from typing import Annotated
from pydantic import BaseModel, Field
from session import get_connection


class BookRequest(BaseModel):
    title: Annotated[str, Field(description="The title of the book", title="Title")]
    author: Annotated[str, Field(description="The author of the book", title="Author")]
    category: Annotated[
        str, Field(description="The category of the book", title="Category")
    ]
    rating: Annotated[
        int, Field(description="The rating of the book", title="Rating", ge=0, le=5)
    ]

    async def create(self):
        async with get_connection() as connection:
            await connection.execute(
                "INSERT INTO books (title, author, category, rating) VALUES (?, ?, ?, ?)",
                (self.title, self.author, self.category, self.rating),
            )
            await connection.commit()


class Book(BookRequest):
    id: Annotated[int, Field(description="The id of the book")]

    @classmethod
    def from_fetch(
        cls, id: int, title: str, author: str, category: str, rating: int = 0
    ):
        return cls(id=id, title=title, author=author, category=category, rating=rating)

    @classmethod
    async def get_by_id(cls, book_id: int):
        async with get_connection() as connection:
            async with connection.execute(
                "SELECT * FROM books WHERE id = ?", (book_id,)
            ) as cursor:
                row = await cursor.fetchone()
            if row is None:
                return None
            return cls.from_fetch(*row)

    async def update(self):
        async with get_connection() as connection:
            await connection.execute(
                "UPDATE books SET title = ?, author = ?, category = ?, rating = ? WHERE id = ?",
                (self.title, self.author, self.category, self.rating, self.id),
            )
            await connection.commit()

    async def delete(self):
        async with get_connection() as connection:
            await connection.execute("DELETE FROM books WHERE id = ?", (self.id,))
            await connection.commit()

    @classmethod
    async def list_books(cls, **kwargs):
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        async with get_connection() as connection:
            if not kwargs:
                async with connection.execute("SELECT * FROM books") as cursor:
                    rows = await cursor.fetchall()
                return [cls.from_fetch(*row) for row in rows]
            query = "SELECT * FROM books WHERE"
            params = []
            for key, value in kwargs.items():
                query += f" {key} = ? AND"
                params.append(value)
            query = query[:-4]
            async with connection.execute(query, params) as cursor:
                rows = await cursor.fetchall()
            return [cls.from_fetch(*row) for row in rows]
