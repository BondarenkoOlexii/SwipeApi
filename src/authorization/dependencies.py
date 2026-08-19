from dishka.integrations.fastapi import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from src.authorization.security import decode_access_token
from src.authorization.security import http_bearer
from src.user.repositories import UserRepository


@inject
async def token_check(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    repositories: FromDishka[UserRepository] = None,
):
    token = credentials.credentials

    user_id = int(decode_access_token(token).get("sub"))

    if user_id:
        user = await repositories.get_user(user_id)
        if user:
            return user
        else:
            raise HTTPException(status_code=401, detail="User deleted")
    else:
        raise HTTPException(status_code=401, detail="User diactivate")
