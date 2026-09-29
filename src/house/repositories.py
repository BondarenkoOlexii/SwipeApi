from typing import Generic
from typing import TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.common.models import Image

from .models import House
from .models import HouseImageAssociation

M = TypeVar("M")


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


class CrudClass(Generic[M]):
    def __init__(self, session: AsyncSession, model: type[M]):
        self.Model = model
        self.session = session

    async def get_all(self, item_id: int, fk_name: str):
        field = getattr(self.Model, fk_name)
        stmt = select(self.Model).where(field == item_id)
        objects = self.session.scalars(stmt)
        return list(objects.all())

    async def get(self, item_id: int):
        return self.session.get(self.Model, item_id)

    async def get_by_name(self, name: str, parent_id: int, fk_name: str):
        field = getattr(self.Model, fk_name)
        stmt = select(self.Model).where(name=name and field == parent_id)
        item = self.session.scalar(stmt)
        return item

    async def create(self, data: dict, fk_field: str, parent_id: int):
        payload = data.copy()

        payload[fk_field] = parent_id

        obj = self.Model(**payload)

        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, data: dict):
        for key, value in data.items():
            setattr(self.Model, key, value)
        await self.session.commit()

    async def delete(self):
        await self.session.delete(self.Model)
        await self.session.commit()
