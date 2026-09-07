from typing import Annotated

from dishka.integrations.fastapi import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from fastapi import Depends
from fastapi import UploadFile

from src.authorization.dependencies import token_check

from .models import User
from .schemas import ProfileUpdate
from .schemas import UserResponse
from .services import UserService

router = APIRouter(prefix="/users", tags=["User"])


# @router.get("/", response_model=list[UserResponse])
# @inject
# async def get_users(service: FromDishka[UserService]):
#     return await service.get_user()


@router.get("/profile", response_model=UserResponse)
@inject
async def get_user(service: FromDishka[UserService], user_id: int):
    return await service.get_user(user_id=user_id)


# @router.get("/{user_id}/update", response_model=UserResponse)
# @inject
# async def get_profile(
#     data: ProfileUpdate, current_user: Annotated[str, Depends(token_check)]
# ):
#     return {"email": current_user.email, "id": current_user.id}


@router.patch("/profile/update")
@inject
async def update_profile(
    user_schema: ProfileUpdate,
    service: FromDishka[UserService],
    current_user: Annotated[User, Depends(token_check)],
) -> UserResponse:
    updated_user = await service.update_user(
        user_id=current_user.id, user_data=user_schema.model_dump()
    )
    return updated_user


@router.post("/profile/update/avatar")
@inject
async def update_profile_avatar(
    current_user: Annotated[User, Depends(token_check)],
    image: UploadFile,
    service: FromDishka[UserService],
):
    update_image = await service.update_profile_avatar(
        user_id=current_user.id, image=image
    )
    return update_image
