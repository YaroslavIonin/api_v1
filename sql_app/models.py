from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from .database import Base

class Price(Base):
    __tablename__ = "price"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    datetime = Column(DateTime, None)
    price = Column(String(64))
    price_int = Column(Numeric(10, 2))

    def __repr__(self):
        return f"{self.name} | {self.price}"