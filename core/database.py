from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from core.config import settings


def new_engine():
    return create_async_engine(settings.database_url, echo=True)


def new_session_maker(engine):
    return async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
