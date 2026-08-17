from fastapi import HTTPException, status, Depends, APIRouter

from src.user.repositories import UserRepository
from .security import decode_access_token, create_access_token, create_refresh_token, get_password_hash,\
    verify_password


class AuthorizationService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

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

            await self.repo.update_refresh_token(token=refresh_token, user_id=user.id)

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

    async def refresh_token(self, old_refresh_token: str):

        user_id = decode_access_token(old_refresh_token).get("sub")

        user = await self.repo.get_user(user_id)

        if not user or user.refresh_token != old_refresh_token:
            raise HTTPException(status_code=401, detail="Токен хуйня твій")
        else:

            new_refresh_token = create_refresh_token({"sub": str(user_id)})
            new_access_token = create_access_token({"sub": str(user_id)})

            await self.repo.update_refresh_token(new_refresh_token, user_id)

        return user, new_refresh_token, new_access_token













