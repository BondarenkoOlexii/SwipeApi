from typing import Annotated
from typing import Generic
from typing import TypeVar

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
from .services import BuildEntityService
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


# def create_building_entity_router(prefix: str, tag: str, service_type: type) -> APIRouter:
#     build_entity_router = APIRouter(prefix=prefix, tags=[tag])
#
#     @build_entity_router.get("/", response_model=GetCorpSectStor)
#     @inject
# async def get_corp_sect_stor(item_id: int, service:FromDishka[])

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
GetSchemaType = TypeVar("GetSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")


class GenericCRUDRouters(Generic[CreateSchemaType, GetSchemaType, UpdateSchemaType]):
    def __init__(
        self,
        create_schema: type[CreateSchemaType],
        get_schema: type[GetSchemaType],
        update_schema: type[UpdateSchemaType],
        prefix: str,
        tags: str,
    ):
        self.create_schema = create_schema
        self.get_schema = get_schema
        self.update_schema = update_schema
        self.prefix = prefix

        self.router = APIRouter(prefix=f"/{prefix}", tags=[tags])

    async def router_get(self, item_id: int, service: FromDishka[BuildEntityService]):
        return await service.get_entity(item_id)

    async def router_create(
        self,
        data_schema: CreateSchemaType,
        service: FromDishka[BuildEntityService],
        parent_id: int,
    ):
        return await service.create_entity(
            parent_id=parent_id, data=data_schema.model_dump()
        )

    async def router_update(
        self,
        data_schema: UpdateSchemaType,
        service: FromDishka[BuildEntityService],
        item_id: int,
    ):
        return await service.update_entity(
            data=data_schema.model_dump(), item_id=item_id
        )

    async def router_delete(
        self, item_id: int, service: FromDishka[BuildEntityService]
    ):
        return await service.delete_entity(item_id=item_id)

    def register_routers(self):
        self.router.add_api_route("/get", self.router_get, methods=["GET"])
        self.router.add_api_route("/create", self.router_create, methods=["POST"])
        self.router.add_api_route("/update", self.router_update, methods=["PATCH"])
        self.router.add_api_route("/delete", self.router_delete, methods=["DELETE"])
