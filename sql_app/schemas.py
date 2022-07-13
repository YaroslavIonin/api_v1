from datetime import datetime
from typing import Union

from pydantic import BaseModel


class PriceBase(BaseModel):
    name: str
    price: str
    price_int: int


class PriceCreate(PriceBase):
    datetime: str = None


class Price(PriceBase):
    id: int

    class Config:
        orm_mode = True


class PriceUpdate(Price, PriceCreate):
    pass
