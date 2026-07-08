from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.common.models import Base


class ApartmentImageAssociation(Base):
    __tablename__ = "apartment_images"

    apartment_id: Mapped[int] = mapped_column(
        ForeignKey("apartment.id", ondelete="CASCADE"), primary_key=True
    )
    image_id: Mapped[int] = mapped_column(
        ForeignKey("images.id", ondelete="CASCADE"), primary_key=True
    )


class Apartment(Base):
    __tablename__ = "apartment"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    area: Mapped[float] = mapped_column()
    price: Mapped[float] = mapped_column()
    is_actual: Mapped[bool] = mapped_column()

    main_image_id = Mapped[int] = mapped_column()
