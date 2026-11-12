from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Apartment


class BaseRepo:
    def __init__(self, session: AsyncSession):
        self.session = session


class ApartmentRepo(BaseRepo):
    async def get_all_apartment(self) -> list[Apartment]:
        stmt = select(Apartment).order_by(Apartment.id)
        result = await self.session.scalars(stmt)
        return list(result.all())

    async def get_apartment(self, apartment_id: int) -> Apartment | None:
        return await self.session.get(Apartment, apartment_id)

    async def get_list_apartment(self, limit: int, offset: int) -> list[Apartment]:
        stmt = (
            select(Apartment).order_by(Apartment.id.desc()).limit(limit).offset(offset)
        )
        result = await self.session.scalars(stmt)
        return list(result.all())

    async def get_list_apartment_price_desc(
        self, limit: int, offset: int
    ) -> list[Apartment]:
        stmt = (
            select(Apartment)
            .order_by(Apartment.price.desc(), Apartment.id)
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.scalars(stmt)
        return list(result.all())

    async def get_list_apartment_price_asc(
        self, limit: int, offset: int
    ) -> list[Apartment]:
        stmt = (
            select(Apartment)
            .order_by(Apartment.price.asc(), Apartment.id)
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.scalars(stmt)
        return list(result.all())

    async def apartment_ribbon(self):
        # stmt = select(Apartment.id, Apartment.name,
        #               Apartment.area, Apartment.price,
        #               House.id, House.name).join(House, Apartment.)

        pass

    async def update_apartment(self, apartment_id: int, data: dict) -> Apartment:
        apart = await self.get_apartment(apartment_id)

        for key, value in data.items():
            setattr(apart, key, value)

        await self.session.commit()

        return apart

    async def delete_apart(self, apartment_id: int):
        apart = await self.get_apartment(apartment_id)
        await self.session.delete(apart)
        await self.session.commit()
        return True
