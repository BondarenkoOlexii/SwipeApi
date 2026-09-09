from datetime import UTC
from datetime import datetime
from datetime import timedelta

from dishka.integrations.fastapi import FromDishka
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer
from jose import JWTError
from jose import jwt
from passlib.context import CryptContext

from core.config import settings
from src.user.repositories import UserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
http_bearer = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        print("PAYLOAD Успішний", payload)

        return payload
    except JWTError as e:
        print(f"ПОМИЛКА ТОКЕНА {type(e).__name__} - {e}")
        raise HTTPException(status_code=401, detail="Токен не валідний") from None


async def token_check(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    repositories: FromDishka[UserRepository] = None,
):
    token = credentials.credentials

    id = decode_access_token(token).get("sub")

    if id:
        user = await repositories.get_user(id)

        return user
    else:
        raise HTTPException(status_code=401, detail="User diactivate")


async def developer_token_check(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    repositories: FromDishka[UserRepository] = None,
):
    token = credentials.credentials

    id = decode_access_token(token).get("sub")

    if id:
        user = await repositories.get_user(id)
        if user.user_type == "developer":
            return user
        else:
            raise HTTPException(status_code=401, detail="User is not developer")
    else:
        raise HTTPException(status_code=401, detail="User diactivate")
