from email import message
from http.client import HTTPMessage, HTTPResponse
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/price/", response_model=schemas.Price)
def create_price(price: schemas.PriceCreate, db: Session = Depends(get_db)):
    db_price = crud.get_price_by_name(db, name=price.name)
    if db_price and db_price.price_int == price.price_int:
        raise HTTPException(status_code=400, detail="Товар с такой ценой уже существует")
    return crud.create_price(db=db, price=price)


@app.get("/prices/", response_model=list[schemas.Price])
def read_prices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    prices = crud.get_prices(db, skip=skip, limit=limit)
    return prices


@app.get("/prices/{price_id}", response_model=schemas.Price)
def read_price(price_id: int, db: Session = Depends(get_db)):
    db_price = crud.get_price(db, id=price_id)
    if db_price is None:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return db_price


@app.delete("/prices/{price_id}", response_model=dict)
def delete_price(price_id: int, db: Session = Depends(get_db)):
    db_price = crud.get_price(db, id=price_id)
    if db_price is None:
        raise HTTPException(status_code=404, detail="Товар не найден")
    crud.del_price(db, id=price_id)
    return {
        'message': 'Товар удалён'
    }


@app.put("/prices/{price_id}", response_model=schemas.Price)
def update_price(price_id: int, new_price: schemas.PriceBase, db: Session = Depends(get_db)):
    db_price = crud.get_price(db, id=price_id)
    if db_price is None:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return crud.updt_price(db, new_price, id=price_id)
    