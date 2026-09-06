import uuid
from pathlib import Path

import aiofiles
from fastapi import UploadFile
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import UPLOAD_DIR

from .models import User


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

    async def get_user_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_by_tg_id(self, tg_id: int) -> User | None:
        stmt = select(User).where(User.tg_id == tg_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_user(self, user_data: dict) -> User:
        user = User(**user_data)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete_user(self, user: User) -> None:
        await self.session.delete(user)
        await self.session.commit()

    async def update_user(self, user_update: dict, user: User) -> User:
        for key, value in user_update.items():
            setattr(user, key, value)
        await self.session.commit()
        return user

    async def update_refresh_token(self, token: str | None, user_id: int) -> User:
        stmt = update(User).where(User.id == user_id).values(refresh_token=token)
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_user_by_refresh_token(self, token: str) -> User | None:
        stmt = select(User).where(User.refresh_token == token)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def upload_profile_image(self, file: UploadFile):
        extencion = Path(file.filename or "").suffix.lower()
        unique_name = f"{uuid.uuid4()}{extencion}"

        destination = UPLOAD_DIR / unique_name

        async with aiofiles.open(destination, "wb") as buffer:
            while content := await file.read(1024 * 1024):
                await buffer.write(content)
