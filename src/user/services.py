from fastapi import HTTPException, status
from src.authorization.security import get_password_hash, create_access_token, create_refresh_token, verify_password
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

    async def register_user(self, email: str, password: str):
        user = await self.repo.get_user_by_email(email=email)

        if user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"This email - {email} is used")
        else:
            hashed_password = get_password_hash(password=password)

            new_user = await self.repo.create_user({
                                                       "email": email,
                                                       "password": hashed_password,
                                                       })
            refresh_token = create_refresh_token({'sub': str(new_user.id)})
            access_token = create_access_token({'sub': str(new_user.id)})

            return new_user, refresh_token, access_token

    async def login_user(self, email: str, password: str):
        user = await self.repo.get_user_by_email(email=email)

        if not user or not verify_password(plain_password=password, hashed_password=user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Your password is wrong")
        else:
            refresh_token = create_refresh_token({'sub': str(user.id)})
            access_token = create_access_token({'sub': str(user.id)})

            await self.repo.update_refresh_token(token=refresh_token, user_id=user.id)

            return user, refresh_token, access_token
