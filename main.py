from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers import router
from session import create_table


version = "2.0.0"


tags_info = [{"name": "Books", "description": "Endpoints related to books"}]


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_table()
    yield


app = FastAPI(lifespan=lifespan, version=version)
app.include_router(router)


if __name__ == "__main__":
    pass
    # import uvicorn

    # uvicorn.run(app, host="localhost", port=8000)
