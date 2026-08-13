from fastapi import APIRouter, HTTPException, status

from dishka.integrations.fastapi import FromDishka, inject

from .repositories import UserRepository
from .schemas import UserCreate, UserUpdate, UserResponse
from .services import UserService


router = APIRouter(prefix='/users', tags=["User"])


@router.get("/", response_model=list[UserResponse])
@inject
async def get_users(repo: FromDishka[UserResponse]):
    return await repo.get_users()


@router.get("/{user_id}/", response_model=UserResponse)
@inject
async def get_user(service: FromDishka[UserService], user_id: int):
    return await service.get_user(user_id=user_id)


@router.post("/create_user", response_model=UserCreate)
@inject
async def create_user(user_in: UserCreate, repo: FromDishka[UserService]):
    return await repo.register_user(email=user_in.email, password=user_in.password)
