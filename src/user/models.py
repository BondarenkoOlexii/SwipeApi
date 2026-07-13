from sqlalchemy import Enum
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.common.models import Base
from src.common.models import NotificationChoice


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(220))
    last_name: Mapped[str] = mapped_column(String(220))
    email: Mapped[str] = mapped_column()
    phone_number: Mapped[str] = mapped_column()
    switching: Mapped[bool] = mapped_column()
    notification: Mapped["NotificationChoice"] = mapped_column(
        Enum(NotificationChoice, native_enum=False)
    )
