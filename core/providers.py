from collections.abc import AsyncIterable

from dishka import Provider
from dishka import Scope
from dishka import from_context
from dishka import provide
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from .config import Settings
from .database import new_engine
from .database import new_session_maker


class RepoProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_engine(self, settings: Settings) -> AsyncIterable:
        return new_engine(settings.get_db_url)

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
