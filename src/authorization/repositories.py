from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.user.schemas import UserInDB
from src.user.models import User


class AuthorizationRepositories:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_email(self, email: str) -> User | None:
        return await self.session.get(User, email)

    async def authenticate_user(self, email: str, password: str) -> User | None:
