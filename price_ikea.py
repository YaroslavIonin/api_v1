import requests
from bs4 import BeautifulSoup
from .sql_app import schemas, main, crud


def add_price(product_title, product_price, product_price_int):
    crud.create_price(main.get_db, schemas.PriceCreate(name=product_title, price=product_price, price_int=product_price_int))
    return


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

for i in range(0, min(len(product_title), len(product_price))):
    add_price(product_title[i].get_text(), product_price[i], int(product_price[i]))
