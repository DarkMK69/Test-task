from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas, crud, database
from app.exceptions import InsufficientStockException

app = FastAPI(
    title="Order Service API",
    version="1.0.0",
    description="REST API для управления заказами и товарами"
)

@app.get("/")
async def root():
    return {"message": "Order Service API"}

@app.post("/orders/{order_id}/items/", response_model=schemas.OrderItem)
def add_item_to_order(
    order_id: int,
    item: schemas.OrderItemCreate,
    db: Session = Depends(database.get_db)
):
    """
    Добавить товар в заказ.
    
    - Если товар уже есть в заказе, увеличивает количество
    - Если товара нет в наличии, возвращает ошибку
    """
    try:
        return crud.add_item_to_order(db, order_id, item.product_id, item.quantity)
    except InsufficientStockException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/products/{product_id}/stock", response_model=schemas.ProductStock)
def check_product_stock(product_id: int, db: Session = Depends(database.get_db)):
    """
    Проверить наличие товара на складе
    """
    try:
        return crud.get_product_stock(db, product_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/health")
def health_check():
    """Проверка статуса сервиса"""
    return {"status": "healthy"}