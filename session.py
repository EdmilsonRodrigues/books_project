from aiosqlite import connect

count = 0


def get_connection():
    return connect("db.sqlite3")


async def create_table():
    global count
    if count == 0:
        count += 1
        async with get_connection() as connection:
            await connection.execute(
                "CREATE TABLE IF NOT EXISTS books \
    (id INTEGER PRIMARY KEY, title TEXT, author TEXT, category TEXT, rating INTEGER)"
            )
            await connection.commit()
    return True
