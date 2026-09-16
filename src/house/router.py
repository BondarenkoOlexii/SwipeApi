from typing import Annotated

from dishka.integrations.fastapi import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from fastapi import Depends

from src.authorization.dependencies import token_check
from src.user.models import User

from .schemas import CreateHouse
from .schemas import DeleteHouse
from .schemas import GetHouse
from .schemas import UpdateHouse
from .services import HouseService

router = APIRouter(prefix="/house", tags=["House"])


@router.get("/get", response_model=GetHouse)
@inject
async def get_house(service: FromDishka[HouseService], house_id: int):
    return await service.get_house(house_id)


@router.post("/create")
@inject
async def create_house(
    service: FromDishka[HouseService],
    house_schema: CreateHouse,
    current_user: Annotated[User, Depends(token_check)],
):
    return await service.create_house(
        data=house_schema.model_dump(), manager_id=current_user.id
    )


@router.patch("/update")
@inject
async def update_house(
    service: FromDishka[HouseService],
    house_schema: UpdateHouse,
    current_user: Annotated[User, Depends(token_check)],
):
    return await service.update_house(
        house_id=house_schema.id,
        house_data=house_schema.model_dump(),
        manager_id=current_user.id,
    )


@router.delete("/delete")
@inject
async def delete_house(
    service: FromDishka[HouseService],
    current_user: Annotated[User, Depends(token_check)],
    house_id: DeleteHouse,
):
    return await service.delete_house(manager_id=current_user.id, house_id=house_id.id)
