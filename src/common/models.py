from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Image(Base):
    id = Column(Integer, primary_key=True)
    filepath = Column(String(150))
