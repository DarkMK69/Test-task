from sqlalchemy.orm import Session
from sqlalchemy import select
from app import models, schemas
from app.exceptions import InsufficientStockException

def add_item_to_order(db: Session, order_id: int, product_id: int, quantity: int):
    # Проверяем наличие товара
    product = db.get(models.Product, product_id)
    if not product:
        raise ValueError("Product not found")
    
    if product.quantity < quantity:
        raise InsufficientStockException(
            f"Insufficient stock for product {product_id}. "
            f"Available: {product.quantity}, Requested: {quantity}"
        )
    
    # Проверяем существование заказа
    order = db.get(models.Order, order_id)
    if not order:
        raise ValueError("Order not found")
    
    # Проверяем, есть ли уже такой товар в заказе
    existing_item = db.execute(
        select(models.OrderItem)
        .where(models.OrderItem.order_id == order_id)
        .where(models.OrderItem.product_id == product_id)
    ).scalar_one_or_none()
    
    if existing_item:
        # Увеличиваем количество
        existing_item.quantity += quantity
    else:
        # Создаем новую позицию
        existing_item = models.OrderItem(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            price=product.price
        )
        db.add(existing_item)
    
    # Уменьшаем количество на складе
    product.quantity -= quantity
    
    db.commit()
    db.refresh(existing_item)
    return existing_item

def get_product_stock(db: Session, product_id: int):
    product = db.get(models.Product, product_id)
    if not product:
        raise ValueError("Product not found")
    return {"product_id": product_id, "available_quantity": product.quantity}