from pydantic import BaseModel, ConfigDict


class CreateHouse(BaseModel):
    address: str
    name: str
    area: str
    location: str
    min_price: float
    price_for_meter: float


class GetHouse(CreateHouse):
    id: int
    model_config = ConfigDict(from_attributes=True)


class UpdateHouse(BaseModel):
    address: str | None = None
    name: str | None = None
    area: str | None = None
    location: str | None = None
    min_price: float | None = None
    price_for_meter: float | None = None

