from re import sub
from decimal import Decimal
from datetime import datetime
import requests
from bs4 import BeautifulSoup

PRODUCT_URL = "https://www.ikea.com/ru/ru/cat/kryuchki-polki-nastennye-organayzery-st006/"

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
}
page = requests.get(url=PRODUCT_URL, headers=headers)

soup = BeautifulSoup(page.content, "lxml")
product_title = soup.find_all(
    "span",
    class_="pip-header-section__title--small notranslate"
)[4:]

product_price = soup.find_all(
    "span",
    class_="pip-price__integer"
)[4:]


product_price = [_.get_text().replace(",", ".").replace(' ', '') for _ in product_price]


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Numeric, DateTime
from sqlalchemy.orm import Session


Base = declarative_base()

class Price(Base):
    __tablename__ = "price"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    datetime = Column(DateTime)
    price = Column(String(64))
    price_int = Column(Numeric(10, 2))

    def __repr__(self):
        return f"{self.name} | {self.price}"


engine = create_engine("sqlite:///db.sqlite")
Base.metadata.create_all(engine)

session = Session(bind=engine)

def add_price(product_title, product_price, product_price_int):
    is_exist = session.query(Price).filter(Price.name==product_title).order_by(Price.datetime.desc()).first()
    if not is_exist:
        session.add(
            Price(name=product_title, datetime=datetime.now(), price = product_price + ' р.', price_int = int(product_price_int))
        )
        session.commit()
    elif is_exist.price_int != product_price_int:
        session.add(
            Price(name=product_title, datetime=datetime.now(), price = product_price + ' Р.', price_int = int(product_price_int))
        )
        session.commit()

for i in range(0, min(len(product_title), len(product_price))):
    add_price(product_title[i].get_text(), product_price[i], int(product_price[i]))

items = session.query(Price).all()
[print(_) for _ in items]