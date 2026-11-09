from pydantic import BaseModel
from pydantic import ConfigDict

from src.common.models import HouseClassChoice
from src.common.models import HouseHeatingChoice
from src.common.models import HouseRegisterChoice


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
    id: int
    address: str | None = None
    name: str | None = None
    area: str | None = None
    location: str | None = None
    min_price: float | None = None
    price_for_meter: float | None = None


class DeleteHouse(BaseModel):
    id: int


class CreateAllForHouse(BaseModel):
    corps_amount: int  # Кількість корпусів в одному будинку
    section_amount: int  # Кількість секцій в одному корпусі
    storey_amount: int  # Кількість етажів в одній секції
    apartment_amount: int  # Кількість квартир на одному етажі


###############################################################
class CreateCorpSectStor(BaseModel):
    name: str


class GetCorpSectStor(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True)


class UpdateCorpSectStor(BaseModel):
    name: str | None = None


################################################################


class BaseGetSchema(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True)


################################################################


class NewsCreateSchema(BaseModel):
    name: str
    description: str


class InfrastructureCreateSchema(BaseModel):
    description: str
    house_type: bool
    construction_technique: str
    territory: bool
    distance_to_sea: bool | None = None
    ceiling_height: str

    status: HouseClassChoice = HouseClassChoice.Middle


class CommunicationCreateSchema(BaseModel):
    gas: bool
    electricity: bool
    sewage: bool
    water: bool
    heating: HouseHeatingChoice = HouseHeatingChoice.Nope


class RegistrationCreateSchema(BaseModel):
    variants: str
    sums: bool
    house_status: HouseRegisterChoice = HouseRegisterChoice.Residential


##################################################################################


class NewsUpdateSchema(BaseModel):
    name: str | None = None
    description: str | None = None


class InfrastructureUpdateSchema(BaseModel):
    description: str | None = None
    house_type: bool | None = None
    construction_technique: str | None = None
    territory: bool | None = None
    distance_to_sea: bool | None = None
    ceiling_height: str | None = None
    status: HouseClassChoice = HouseClassChoice.Middle


class CommunicationUpdateSchema(BaseModel):
    gas: bool | None = None
    electricity: bool | None = None
    sewage: bool | None = None
    water: bool | None = None
    heating: HouseHeatingChoice = HouseHeatingChoice.Nope


class RegistrationUpdateSchema(BaseModel):
    variants: str | None = None
    sums: bool | None = None
    house_status: HouseRegisterChoice = HouseRegisterChoice.Residential
