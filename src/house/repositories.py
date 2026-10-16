from typing import Generic
from typing import TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.common.models import Image
from src.user.models import User

from .models import House
from .models import HouseImageAssociation

M = TypeVar("M")


class BaseRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_house(self, house_id: int) -> House | None:
        return await self.session.get(House, house_id)

    async def get_manager(self, manager_id: int) -> User | None:
        return await self.session.get(User, User.id == manager_id)

    async def verify_manager(self, house_id: int, manager_id: int):
        if await self.get_manager(manager_id):
            stmt = select(House).where(
                House.id == house_id, House.manager_id == manager_id
            )
            obj = await self.session.scalar(stmt)
            if obj:
                return obj
            return None


class HouseRepositories:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_house(self, house_id: int) -> House | None:
        return await self.session.get(House, house_id)

    async def create_house(self, data: dict) -> House:
        house = House(**data)
        self.session.add(house)
        await self.session.commit()
        return house

    async def update_house(self, house: House, data: dict) -> House:
        for key, value in data.items():
            setattr(house, key, value)
        await self.session.commit()
        return house

    async def delete_house(self, house: House):
        await self.session.delete(house)
        await self.session.commit()

    async def upload_file(self, file: str, house_id: int, type: str) -> House:
        new_image = Image(filepath=file)
        house_image = HouseImageAssociation(
            house_id=house_id, image_id=new_image, display_type=type
        )

        self.session.add(house_image)
        await self.session.commit()

    async def get_house_images(self, house_id: int, display_type: str):
        stmt = (
            select(HouseRepositories)
            .where(
                HouseImageAssociation.house_id == house_id,
                HouseImageAssociation.display_type == display_type,
            )
            .options(selectinload(HouseImageAssociation.image.filepath))
        )
        return await self.session.scalar(stmt)


class DetailHouseRepositories(Generic[M], BaseRepo):
    def __init__(self, session: AsyncSession, model: type[M]):
        super().__init__(session)
        self.Model = model

    async def get_all_from_house(self, house_id: int):
        stmt = select(self.Model).where(self.Model.house_id == house_id)
        objects = await self.session.scalars(stmt)
        return list(objects.all())

    async def get_item_from_house(self, house_id: int, item_id: int):
        if hasattr(self.Model, self.Model.id):
            stmt = select(self.Model).where(
                self.Model.house_id == house_id, self.Model.id == item_id
            )
        else:
            stmt = select(self.Model).where(self.Model.house_id == house_id)
        return await self.session.scalar(stmt)

    async def create_item(self, house_id: int, data: dict):
        payload = data.copy()

        payload[house_id] = house_id

        obj = self.Model(**data)

        self.session.add(obj)
        await self.session.commit()

        return obj

    async def update(self, data: dict, item_id: int):
        obj = await self.session.get(item_id)

        for key, value in data.items():
            setattr(obj, key, value)
        await self.session.commit()

    async def delete(self, item_id: int):
        obj = await self.session.get(item_id)

        if obj:
            await self.delete(obj)
            await self.session.commit()
        return None


class CrudClass(Generic[M]):
    def __init__(self, session: AsyncSession, model: type[M]):
        self.Model = model
        self.session = session

    async def get_all(self, item_id: int, fk_name: str):
        field = getattr(self.Model, fk_name)
        stmt = select(self.Model).where(field == item_id)
        objects = await self.session.scalars(stmt)
        return list(objects.all())

    async def get(self, item_id: int):
        return await self.session.get(self.Model, item_id)

    async def get_by_name(self, name: str, parent_id: int, fk_name: str):
        field = getattr(self.Model, fk_name)
        stmt = select(self.Model).where(self.Model.name == name, field == parent_id)
        item = await self.session.scalar(stmt)
        return item

    async def create(self, data: dict, fk_field: str, parent_id: int):
        payload = data.copy()

        payload[fk_field] = parent_id

        obj = self.Model(**payload)

        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, data: dict, item_id: int):
        obj = await self.session.get(item_id)

        for key, value in data.items():
            setattr(obj, key, value)
        await self.session.commit()

    async def delete(self, item_id: int):
        obj = await self.session.get(item_id)

        if obj:
            await self.delete(obj)
            await self.session.commit()
        return None
