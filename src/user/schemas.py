from pydantic import BaseModel, EmailStr, ConfigDict

from src.common.models import NotificationChoice


class UserBase(BaseModel):
    email: EmailStr
    first_name: str


    last_name: str | None = None
    tg_id: int | None = None
    phone_number: str | None = None
    switching: bool | None = None
    notification: NotificationChoice | None = None


class UserCreate(UserBase):
    hashed_password: str | None = None


class UserResponse(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class UserUpdate(UserBase):
    email: EmailStr | None = None
    hashed_password: str | None = None