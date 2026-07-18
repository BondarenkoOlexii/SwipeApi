from fastapi import Depends, FastAPI
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
import structlog
from dishka import make_async_container, AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from fastapi.middleware.cors import CORSMiddleware

from core.providers import RepoProvider
from core.config import Settings


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    print("Все стартануло")
    yield
    print("Все зупинилось")


def create_app() -> FastAPI:

    app = FastAPI(
        title="Title",
        lifespan=lifespan
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost",
            "http://localhost:8080",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    settings = Settings()
    container: AsyncContainer = make_async_container(RepoProvider(), context={Settings: settings})
    setup_dishka(container, app)

    #app.include_router()

    @app.get("/")
    async def root():
        return {"message": "Server Life Dishka also"}

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
