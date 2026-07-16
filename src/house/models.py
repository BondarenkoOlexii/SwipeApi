from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.common.models import Base
from src.common.models import HouseClassChoice
from src.common.models import HouseHeatingChoice
from src.common.models import HouseRegisterChoice


class House(Base):
    __tablename__ = "house"

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()
    area: Mapped[float] = mapped_column()
    price_for_meter: Mapped[float] = mapped_column()
    min_price: Mapped[float] = mapped_column()
    location: Mapped[str] = mapped_column()

    corps: Mapped[list["Corps"]] = relationship(
        "Corps", back_populates="house", cascade="all, delete-orphan"
    )


class Corps(Base):
    __tablename__ = "house_corps"
    id: Mapped[int] = mapped_column(primary_key=True)

    house_id: Mapped[int] = mapped_column(ForeignKey("house.id", ondelete="CASCADE"))
    house: Mapped["House"] = relationship(back_populates="house_corps")

    name: Mapped[str] = mapped_column()

    sections: Mapped[list["Section"]] = relationship(
        "Section", back_populates="corps", cascade="all, delete-orphan"
    )


class Section(Base):
    __tablename__ = "house_section"

    id: Mapped[int] = mapped_column(primary_key=True)

    corps_id: Mapped[int] = mapped_column(
        ForeignKey("house_corps.id", ondelete="CASCADE")
    )
    corps: Mapped[list["Corps"]] = relationship(back_populates="corps_section")

    name: Mapped[str] = mapped_column()

    storey: Mapped[list["Storey"]] = relationship(
        "Section", back_populates="corps", cascade="all, delete-orphan"
    )


class Storey(Base):
    __tablename__ = "house_storey"

    id: Mapped[int] = mapped_column(primary_key=True)

    section_id: Mapped[int] = mapped_column(
        ForeignKey("house_section.id", ondelete="CASCADE")
    )
    section: Mapped[list["Section"]] = relationship(back_populates="storey")

    name: Mapped[str] = mapped_column()


class Infrastructure(Base):
    __tablename__ = "infrastructure"

    house_id: Mapped[int] = mapped_column(
        ForeignKey("house.id", ondelete="CASCADE"), primary_key=True
    )
    house: Mapped["House"] = relationship(back_populates="infrastructure")

    description: Mapped[str] = mapped_column(Text())
    status: Mapped[HouseClassChoice] = mapped_column(
        Enum(HouseClassChoice, native_enum=False), default=HouseClassChoice.Middle
    )
    house_type: Mapped[bool] = mapped_column()
    construction_technique: Mapped[str] = mapped_column(Text())
    territory: Mapped[bool] = (
        mapped_column()
    )  # Тут якщо True значить територія відкрита; False - закрита
    distance_to_sea: Mapped[str] = mapped_column(nullable=True)
    ceiling_height: Mapped[str] = mapped_column()


class News(Base):
    __tablename__ = "news"

    id: Mapped[int] = mapped_column(primary_key=True)
    house_id: Mapped[int] = mapped_column(ForeignKey("house.id", ondelete="CASCADE"))
    house: Mapped["House"] = relationship(back_populates="news")

    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column(Text())


class Communication(Base):
    __tablename__ = "communication"

    id: Mapped[int] = mapped_column(primary_key=True)
    house_id: Mapped[int] = mapped_column(ForeignKey("house.id", ondelete="CASCADE"))
    house: Mapped["House"] = relationship(back_populates="communication")

    gas: Mapped[bool] = mapped_column()  # Газ підключенний або ні
    electricity: Mapped[bool] = mapped_column()  # Електрика або підключення або ні
    sewage: Mapped[bool] = mapped_column()  # Каналізація підключена або ні
    water: Mapped[bool] = mapped_column()  # Вода є або ні
    heating: Mapped["HouseHeatingChoice"] = mapped_column(
        Enum(HouseHeatingChoice, native_enum=False), default=HouseHeatingChoice.Nope
    )


class Registration(Base):
    __tablename__ = "registration"

    id: Mapped[int] = mapped_column(primary_key=True)
    house_id: Mapped[int] = mapped_column(ForeignKey("house.id", ondelete="CASCADE"))
    house: Mapped["House"] = relationship(back_populates="registration")

    variants: Mapped[str] = mapped_column(String(220))
    sums: Mapped[bool] = mapped_column()  # True якщо повне і False якщо не повне
    house_status: Mapped["HouseRegisterChoice"] = mapped_column(
        Enum(HouseRegisterChoice, native_enum=False),
        default=HouseRegisterChoice.Residential,
    )


class CalculationVariant(Base):
    __tablename__ = "calculation_variant"

    id: Mapped[int] = mapped_column(primary_key=True)
    registration_id: Mapped[int] = mapped_column(
        ForeignKey("registration.id", ondelete="CASCADE")
    )
    registration: Mapped["Registration"] = relationship(
        back_populates="calculation_variant"
    )

    name: Mapped[str] = mapped_column(String(220))
