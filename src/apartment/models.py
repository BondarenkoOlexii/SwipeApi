from sqlalchemy import ForeignKey, String, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.common.models import Base, Image, HouseStatusChoice, HeatingTypeChoice, CommunicationChoice


class ApartmentImageAssociation(Base):
    __tablename__ = "apartment_images"

    apartment_id: Mapped[int] = mapped_column(
        ForeignKey("apartment.id", ondelete="CASCADE"), primary_key=True
    )
    image_id: Mapped[int] = mapped_column(
        ForeignKey("images.id", ondelete="CASCADE"), primary_key=True
    )
    display_type: Mapped[str] = mapped_column(String(50), default="gallery")

    apartment: Mapped["Apartment"] = relationship(back_populates="image_associations")
    image: Mapped["Image"] = relationship()


class Apartment(Base):
    __tablename__ = "apartment"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    area: Mapped[float] = mapped_column()
    price: Mapped[float] = mapped_column()
    is_actual: Mapped[bool] = mapped_column()

    image_associations: Mapped[list["ApartmentImageAssociation"]] = relationship("ApartmentImageAssociation",
                                                                                 back_populates="apartment",
                                                                                 cascade="all, delete-orphan",
                                                                                 lazy="selection")

    favorites: Mapped[list["User"]] = relationship("User", secondary="favorite", back_populates="favorites")


class DetailApartment(Base):
    __tablename__ = "detail_apartment"

    apartment_id: Mapped[int] = mapped_column(ForeignKey('apartment.id', ondelete="CASCADE"), primary_key=True)
    apartment: Mapped["Apartment"] = relationship(back_populates="detail")

    description: Mapped[str] = mapped_column(Text, nullable=True)
    type: Mapped[str] = mapped_column(String(220), nullable=True)
    adress: Mapped[str] = mapped_column(Text, nullable=True)
    location: Mapped[str] = mapped_column(Text, nullable=True)

    number_of_rooms: Mapped[str] = mapped_column(String(220))
    layout: Mapped[str] = mapped_column(String(220), nullable=True)
    kitchen_area: Mapped[float] = mapped_column()

    heating_type: Mapped[HeatingTypeChoice] = mapped_column(Enum(HeatingTypeChoice, native_enum=False, length=10))
    balcony: Mapped[bool] = mapped_column()
    mortgage: Mapped[bool] = mapped_column()
    agent_commission: Mapped[bool] = mapped_column(nullable=True)
    state: Mapped[str] = mapped_column(String(220))

    communication: Mapped[CommunicationChoice] = mapped_column(Enum(CommunicationChoice, native_enum=False, length=10))


class Advantages(Base):
    __tablename__ = "advantages"

    apartment_id: Mapped[int] = mapped_column(ForeignKey('apartment.id', ondelete="CASCADE"), primary_key=True)
    apartment: Mapped["Apartment"] = relationship(back_populates="advantages")

    advantage_1: Mapped[bool] = mapped_column()
    advantage_2: Mapped[bool] = mapped_column()
    advantage_3: Mapped[bool] = mapped_column()
    advantage_4: Mapped[bool] = mapped_column()
    advantage_5: Mapped[bool] = mapped_column()
    advantage_6: Mapped[bool] = mapped_column()
