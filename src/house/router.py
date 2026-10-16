from typing import Annotated
from typing import Generic
from typing import TypeVar

from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from fastapi import Depends
from fastapi import UploadFile

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


@router.post("/upload/files")
@inject
async def upload_files(
    files: list[UploadFile],
    service: FromDishka[HouseService],
    current_user: Annotated[User, Depends(token_check)],
):
    return await service.upload_images(house_id=current_user.id, images=files)


ServiceType = TypeVar("ServiceType")
CreateSchemaType = TypeVar("CreateSchemaType")
GetSchemaType = TypeVar("GetSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")


class GenericCrudRouter(
    Generic[CreateSchemaType, GetSchemaType, UpdateSchemaType, ServiceType]
):
    def __init__(
        self,
        create_schema: type[CreateSchemaType],
        update_schema: type[UpdateSchemaType],
        get_schema: type[GetSchemaType],
        prefix: str,
        tags: str,
        service_type: type[ServiceType],
    ):
        self.router = APIRouter(
            prefix=f"/{prefix}", tags=[tags], route_class=DishkaRoute
        )

        self._registry(create_schema, get_schema, update_schema, service_type)

    def _registry(self, create_schema, get_schema, update_schema, service_type):
        @self.router.get("/{parent_id}", response_model=get_schema)
        @inject
        async def get_entity(parent_id: int, service_type: FromDishka[service_type]):
            return await service_type.get_entity(parent_id)

        @self.router.post("/{parent_id}/create", response_model=create_schema)
        async def create_entity(parent_id: int, service_type: FromDishka[service_type]):
            return await service_type.create_entity(
                parent_id, create_schema.model_dump()
            )

        @self.router.patch(
            "/{parent_id}/{item_id}/update", response_model=update_schema
        )
        async def update_entity(item_id: int, service_type: FromDishka[service_type]):
            return await service_type.update_entity(item_id, update_schema.model_dump())

        @self.router.delete("/delete")
        async def delete_entity(item_id: int, service_type: FromDishka[service_type]):
            return await service_type.delete_entity(item_id)
