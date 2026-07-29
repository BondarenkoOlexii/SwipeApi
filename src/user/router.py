from fastapi import APIRouter, HTTPException, status

from dishka.integrations.fastapi import FromDishka, inject

from .repositories import UserRepository
from .schemas import UserCreate, UserUpdate, UserBase, UserResponse


router = APIRouter(prefix='/user', tags=["User"])


@router.get("/", response_model=list[UserResponse])
@inject
async def get_users(repo: FromDishka[UserResponse]):
    return await repo.get_users()

@router.get("/{user_id}/", response_model=UserResponse)
@inject
async def get_user(repo: FromDishka[UserRepository], user_id: int):
    user = await repo.get_user(user_id=user_id)

    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {user_id} not found"
    )


@router.post("/create_user", response_model=UserResponse)
@inject
async def create_user(user_in: UserCreate, repo: FromDishka[UserRepository]):
    return await repo.create_user(user_in=user_in)