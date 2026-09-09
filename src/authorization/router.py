from dishka.integrations.fastapi import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter

from src.user.schemas import UserCreate
from src.user.schemas import UserLogin

from .schemas import RefreshSchema
from .schemas import TokenSchema
from .services import AuthorizationService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=TokenSchema)
@inject
async def registration(data: UserCreate, service: FromDishka[AuthorizationService]):
    new_user, refresh_token, access_token = await service.register_user(
        data.email, data.password
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user_id": new_user.id,
    }


@router.post("/login", response_model=TokenSchema)
@inject
async def login(data: UserLogin, service: FromDishka[AuthorizationService]):
    user, refresh_token, access_token = await service.login_user(
        data.email, data.hashed_password
    )

    return TokenSchema(
        access_token=access_token, refresh_token=refresh_token, user=user
    )


@router.post("/refresh", response_model=TokenSchema)
@inject
async def refresh_token(data: RefreshSchema, service: FromDishka[AuthorizationService]):
    user, refresh_token, access_token = await service.refresh_token(data.refresh_token)

    return TokenSchema(
        access_token=access_token, refresh_token=refresh_token, user=user
    )


@router.post("/developer/register", response_model=TokenSchema)
@inject
async def register_developer():
    pass


@router.post("/developer/login", response_model=TokenSchema)
@inject
async def login_developer():
    pass
