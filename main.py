from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers import router
from session import create_table


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_table()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)


if __name__ == "__main__":
    pass
    # import uvicorn

    # uvicorn.run(app, host="localhost", port=8000)
