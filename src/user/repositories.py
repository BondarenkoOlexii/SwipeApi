from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User
from .schemas import UserCreate, UserUpdate


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_users(self) -> list[User]:
        stmt = select(User).order_by(User.id)
        result: Result = await self.session.execute(stmt)
        users = result.scalars().all()
        return list(users)

    async def get_user(self, user_id: int) -> User | None:
        return await self.session.get(User, user_id)

    async def create_user(self, user_in: UserCreate) -> User:
        user = User(**user_in.model_dump())
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete_user(self, user: User) -> None:
        await self.session.delete(user)
        await self.session.commit()

    async def update_user(self, user_update: UserUpdate, user: User) -> User:
        for key, value in user_update.model_dump().items():
            setattr(user, key, value)
        await self.session.commit()
        return user

    async def update_user_partial(self, user_update: UserUpdate, user: User) -> User:
        for key, value in user_update.model_dump(exclude_unset=True).items():
            setattr(user, key, value)
        await self.session.commit()
        return user
