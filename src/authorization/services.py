from fastapi import HTTPException
from fastapi import status

from src.common.models import UserTypes
from src.user.repositories import UserRepository

from .security import create_access_token
from .security import create_refresh_token
from .security import decode_access_token
from .security import get_password_hash
from .security import verify_password


class AuthorizationService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def register_user(self, email: str, password: str):
        user = await self.repo.get_user_by_email(email=email)

        if not user:
            hashed_password = get_password_hash(password=password)

            new_user = await self.repo.create_user(
                {
                    "email": email,
                    "hashed_password": hashed_password,
                    "user_type": UserTypes.User,
                }
            )
            refresh_token = create_refresh_token(
                {"sub": str(new_user.id), "role": str(new_user.user_type)}
            )
            access_token = create_access_token(
                {"sub": str(new_user.id), "role": str(new_user.user_type)}
            )

            await self.repo.update_refresh_token(
                token=refresh_token, user_id=new_user.id
            )

            return new_user, refresh_token, access_token
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"This email - {email} is used",
            )

    async def login_user(self, email: str, password: str):
        user = await self.repo.get_user_by_email(email=email)

        if user and verify_password(
            plain_password=password, hashed_password=user.hashed_password
        ):
            refresh_token = create_refresh_token(
                {"sub": str(user.id), "role": str(user.user_type)}
            )
            access_token = create_access_token(
                {"sub": str(user.id), "role": str(user.user_type)}
            )

            await self.repo.update_refresh_token(token=refresh_token, user_id=user.id)

            return user, refresh_token, access_token

        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Your password is wrong",
            )

    async def refresh_token(self, old_refresh_token: str):
        user_id = int(decode_access_token(old_refresh_token).get("sub"))

        user = await self.repo.get_user(user_id)

        if user and user.refresh_token == old_refresh_token:
            new_refresh_token = create_refresh_token(
                {"sub": str(user_id), "role": str(user.user_type)}
            )
            new_access_token = create_access_token(
                {"sub": str(user_id), "role": str(user.user_type)}
            )

            await self.repo.update_refresh_token(new_refresh_token, user_id)

            return user, new_refresh_token, new_access_token
        else:
            raise HTTPException(status_code=401, detail="Токен хуйня твій")
