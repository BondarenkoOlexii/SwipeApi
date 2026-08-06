from fastapi import HTTPException, status

from .repositories import UserRepository
from .schemas import UserCreate


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def get_user(self, user_id: int):
        user = await self.repo.get_user(user_id=user_id)

        if user:
            return user
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id - {user_id} not found")
    