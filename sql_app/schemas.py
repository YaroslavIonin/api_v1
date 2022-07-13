from datetime import datetime
from pydantic import BaseModel


class PriceBase(BaseModel):
    name: str
    price: str
    price_int: int


class PriceCreate(PriceBase):
    pass


class Price(PriceBase):
    id: int
    datetime: datetime

    class Config:
        orm_mode = True


class PriceUpdate(Price, PriceCreate):
    pass
