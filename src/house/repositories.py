from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.common.models import Image

from .models import House, HouseImageAssociation


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
