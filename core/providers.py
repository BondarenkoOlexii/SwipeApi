from collections.abc import AsyncIterable
from pathlib import Path
from typing import NewType

from dishka import Provider
from dishka import Scope
from dishka import from_context
from dishka import provide
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.authorization.services import AuthorizationService
from src.common.storage import StorageFile
from src.house.models import Corps
from src.house.models import Section
from src.house.models import Storey
from src.house.repositories import CrudClass
from src.house.repositories import HouseRepositories
from src.house.services import BuildEntityService
from src.house.services import HouseService
from src.user.repositories import UserRepository
from src.user.services import UserService

from .config import Settings
from .database import new_engine
from .database import new_session_maker

CorpsService = NewType("CorpsService", BuildEntityService[Corps])
SectionService = NewType("SectionService", BuildEntityService[Section])
StoreyService = NewType("StoreyService", BuildEntityService[Storey])


class RepoProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_engine(self, settings: Settings) -> AsyncIterable[AsyncEngine]:
        engine = new_engine()
        yield engine
        await engine.dispose()

    @provide(scope=Scope.APP)
    def get_session_marker(
        self, engine: AsyncEngine
    ) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(engine)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            yield session


class RepositoryProvider(Provider):
    @provide(scope=Scope.APP)
    def get_storage(self) -> StorageFile:
        return StorageFile(upload_dir=Path("media"))

    scope = Scope.REQUEST

    user_repo = provide(UserRepository)
    user_service = provide(UserService)
    auth_service = provide(AuthorizationService)
    house_service = provide(HouseService)
    house_repositories = provide(HouseRepositories)

    @provide
    def get_corps_service(self, session: AsyncSession) -> CorpsService:
        repo = CrudClass(session=session, model=Corps)
        return CorpsService(
            BuildEntityService(repo=repo, model_type=Corps, fk_field_name="house_id")
        )

    @provide
    def get_section_service(self, session: AsyncSession) -> SectionService:
        repo = CrudClass(session=session, model=Section)
        return SectionService(
            BuildEntityService(repo=repo, model_type=Section, fk_field_name="corps_id")
        )

    @provide()
    def get_storey_service(self, session: AsyncSession) -> StoreyService:
        repo = CrudClass(session=session, model=StoreyService)
        return StoreyService(
            BuildEntityService(repo=repo, model_type=Storey, fk_field_name="section_id")
        )
