from aiosqlite import connect


def get_connection():
    return connect("books.db")


async def create_table():
    async with get_connection() as connection:
        await connection.execute(
            "CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author TEXT, category TEXT)"
        )
        await connection.commit()
