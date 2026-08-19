from typing import Annotated

from dishka.integrations.fastapi import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from fastapi import Depends

from src.authorization.dependencies import token_check

from .schemas import UserResponse
from .services import UserService

router = APIRouter(prefix="/users", tags=["User"])


@router.get("/", response_model=list[UserResponse])
@inject
async def get_users(repo: FromDishka[UserResponse]):
    return await repo.get_users()


@router.get("/{user_id}/", response_model=UserResponse)
@inject
async def get_user(service: FromDishka[UserService], user_id: int):
    return await service.get_user(user_id=user_id)


@router.get("/profile", response_model=UserResponse)
@inject
async def get_profile(current_user: Annotated[str, Depends(token_check)]):
    return {"email": current_user.email, "id": current_user.id}
