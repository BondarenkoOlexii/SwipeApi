from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from dishka import AsyncContainer
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import Settings
from core.providers import RepoProvider
from core.providers import RepositoryProvider
from src.user.router import router as user_router
from src.authorization.router import router as auth_router

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    print("Все стартануло")
    yield
    print("Все зупинилось")


def create_app() -> FastAPI:
    app = FastAPI(title="Title", lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost",
            "http://localhost:8080",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    settings = Settings()
    container: AsyncContainer = make_async_container(
        RepoProvider(), RepositoryProvider(), context={Settings: settings}
    )
    setup_dishka(container, app)

    app.include_router(user_router)
    app.include_router(auth_router)

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
