import enum

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Image(Base):
    __tablename__ = "image"

    id = Column(Integer, primary_key=True)
    filepath = Column(String(150))


class HouseStatusChoice(str, enum.Enum):
    Passed = "passed"
    Construction = "сonstruction"
    Planned = "planned"


class HeatingTypeChoice(str, enum.Enum):
    Gas = "gas"
    Electricity = "electricity"


class CommunicationChoice(str, enum.Enum):
    Call = "call"
    Message = "message"
    Call_And_Message = "call+message"


class HouseClassChoice(str, enum.Enum):
    Economy = "economy"
    Middle = "middle"
    Elite = "elite"


class HouseHeatingChoice(str, enum.Enum):
    Nope = "nope"
    Central = "central"
    Private = "private"


class HouseRegisterChoice(str, enum.Enum):
    Commercial = "commercial"
    Residential = "residential"


class NotificationChoice(str, enum.Enum):
    Me = "me"
    Me_And_Agent = "me_and_agent"
    Agent = "agent"
    Off = "off"


class RepairUserChoice(str, enum.Enum):
    Non = "none"
    Rough = "rough"
    Full_fledged = "full_fledged"
