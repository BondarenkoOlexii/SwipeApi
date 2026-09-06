from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

from src.common.models import NotificationChoice


class UserBase(BaseModel):
    email: EmailStr
    first_name: str | None = None

    last_name: str | None = None
    tg_id: int | None = None
    phone_number: PhoneNumber | None = None
    switching: bool | None = None
    notification: NotificationChoice | None = None


class UserLogin(BaseModel):
    email: EmailStr
    hashed_password: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class UserUpdate(UserBase):
    email: EmailStr | None = None
    hashed_password: str | None = None


class ProfileUpdate(BaseModel):
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    tg_id: int | None = None
    phone_number: PhoneNumber | None = None
    switching: bool | None = None
    notification: NotificationChoice | None = None


class UserInDB(UserResponse):
    hashed_password: str
