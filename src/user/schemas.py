from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserResponce(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserUpdate(UserBase):
    email: EmailStr | None = None
    password: str | None = None