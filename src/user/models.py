from sqlalchemy import Enum, String, ForeignKey, DateTime, func, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime
from decimal import Decimal

from src.common.models import Base, Image
from src.common.models import NotificationChoice, RepairUserChoice


class UserImageAssociation(Base):
    __tablename__ = "user_images"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), primary_key=True
    )
    image_id: Mapped[int] = mapped_column(
        ForeignKey("images.id", ondelete="CASCADE"), primary_key=True
    )
    display_type: Mapped[str] = mapped_column(String(50), default="gallery")

    user: Mapped["User"] = relationship(back_populates="image_associations")
    image: Mapped["Image"] = relationship(back_populates="user_associations")


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)

    first_name: Mapped[str] = mapped_column(String(220))
    last_name: Mapped[str] = mapped_column(String(220))
    email: Mapped[str] = mapped_column()
    phone_number: Mapped[str] = mapped_column()
    switching: Mapped[bool] = mapped_column()
    notification: Mapped["NotificationChoice"] = mapped_column(
        Enum(NotificationChoice, native_enum=False)
    )
    favorites: Mapped[list["Apartment"]] = relationship("Apartment", secondary="favorite", back_populates="favorites_by")


class Subscription(Base):
    __tablename__ = "subscription"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete="CASCADE"), primary_key=True)
    user: Mapped["User"] = relationship(back_populates="subscription")

    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())


class Filter(Base):
    __tablename__ = "filter"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete="CASCADE"))
    user: Mapped["User"] = relationship(back_populates="filter")

    min_price: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2))
    max_price: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2))

    min_price_for_meter: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2))
    max_price_for_meter: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2))

    min_area: Mapped[float] = mapped_column()
    max_area: Mapped[float] = mapped_column()

    repair: Mapped["RepairUserChoice"] = mapped_column(Enum(RepairUserChoice, native_enum=False), default=RepairUserChoice.Non)


class Favorite(Base):
    __tablename__ = "favorite"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    apartment_id: Mapped[int] = mapped_column(ForeignKey("apartment.id", ondelete="CASCADE"), primary_key=True)

    create_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())



