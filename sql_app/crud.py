from datetime import datetime
from http.client import HTTPResponse
from statistics import mode
from sqlalchemy.orm import Session

import models, schemas


def get_price(db: Session, id: int):
    return db.query(models.Price).filter(models.Price.id == id).first()


def get_price_by_name(db: Session, name: str):
    return db.query(models.Price).filter(models.Price.name == name).order_by(models.Price.datetime.desc()).first()


def get_prices(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Price).offset(skip).limit(limit).all()


def create_price(db: Session, price: schemas.PriceCreate):
    dt = datetime.now()
    db_price = models.Price(
        name=price.name,
        datetime= dt,
        price=price.price, 
        price_int=price.price_int
    )
    db.add(db_price)
    db.commit()
    db.refresh(db_price)
    return db_price


def del_price(db: Session, id: int):
    db.query(models.Price).filter(models.Price.id == id).delete()
    db.commit()


def updt_price(db: Session, new_price: schemas.PriceCreate, id: int):
    old_price = db.query(models.Price).filter(models.Price.id == id).first()
    old_price.name, old_price.price, old_price.price_int = new_price.name, new_price.price, new_price.price_int
    db.commit()
    db.refresh(old_price)
    return old_price

