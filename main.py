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
from src.authorization.router import router as auth_router
from src.house.router import GenericDetailHouseRouter
from src.house.router import GenericHouseRouter
from src.house.router import router as house_router
from src.house.schemas import BaseGetSchema
from src.house.schemas import CommunicationCreateSchema
from src.house.schemas import CommunicationUpdateSchema
from src.house.schemas import CreateCorpSectStor
from src.house.schemas import GetCorpSectStor
from src.house.schemas import InfrastructureCreateSchema
from src.house.schemas import InfrastructureUpdateSchema
from src.house.schemas import NewsCreateSchema
from src.house.schemas import NewsUpdateSchema
from src.house.schemas import RegistrationCreateSchema
from src.house.schemas import RegistrationUpdateSchema
from src.house.schemas import UpdateCorpSectStor
from src.house.services import BuildEntityService
from src.house.services import DetailHouseService
from src.user.router import router as user_router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    print("Project starts")
    yield
    print("Project end")


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
    app.include_router(house_router)

    corpus_router = GenericHouseRouter(  # ПЕРЕРОБИТИ PREFIX !!!!!
        create_schema=CreateCorpSectStor,
        get_schema=GetCorpSectStor,
        update_schema=UpdateCorpSectStor,
        service_type=BuildEntityService,
        prefix="corps",
        tags="Corps",
    )

    section_router = GenericHouseRouter(
        create_schema=CreateCorpSectStor,
        get_schema=GetCorpSectStor,
        update_schema=UpdateCorpSectStor,
        service_type=BuildEntityService,
        prefix="section",
        tags="Section",
    )

    storey_router = GenericHouseRouter(
        create_schema=CreateCorpSectStor,
        get_schema=GetCorpSectStor,
        update_schema=UpdateCorpSectStor,
        service_type=BuildEntityService,
        prefix="storey",
        tags="Storey",
    )

    infrastructure_router = GenericDetailHouseRouter(
        create_schema=InfrastructureCreateSchema,
        update_schema=InfrastructureUpdateSchema,
        get_schema=BaseGetSchema,
        service_type=DetailHouseService,
        prefix="infrastructure",
        tags="Infrastructure",
    )

    news_router = GenericDetailHouseRouter(
        create_schema=NewsCreateSchema,
        update_schema=NewsUpdateSchema,
        get_schema=BaseGetSchema,
        service_type=DetailHouseService,
        prefix="news",
        tags="News",
    )

    communication_router = GenericDetailHouseRouter(
        create_schema=CommunicationCreateSchema,
        update_schema=CommunicationUpdateSchema,
        get_schema=BaseGetSchema,
        service_type=DetailHouseService,
        prefix="communication",
        tags="Communication",
    )

    registration_router = GenericDetailHouseRouter(
        create_schema=RegistrationCreateSchema,
        update_schema=RegistrationUpdateSchema,
        get_schema=BaseGetSchema,
        service_type=DetailHouseService,
        prefix="registration",
        tags="Registration",
    )

    app.include_router(corpus_router.router)
    app.include_router(section_router.router)
    app.include_router(storey_router.router)

    app.include_router(infrastructure_router.router)
    app.include_router(news_router.router)
    app.include_router(communication_router.router)
    app.include_router(registration_router.router)

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
