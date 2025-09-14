from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CategoryBase(BaseModel):
    name: str
    parent_id: Optional[int] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    name: str
    quantity: int = Field(ge=0)
    price: float = Field(ge=0)
    category_id: Optional[int] = None

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True

class ProductStock(BaseModel):
    product_id: int
    available_quantity: int

class ClientBase(BaseModel):
    name: str
    address: str

class ClientCreate(ClientBase):
    pass

class Client(ClientBase):
    id: int

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    client_id: int
    status: Optional[str] = "created"

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    order_date: datetime

    class Config:
        from_attributes = True

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    order_id: int
    price: float

    class Config:
        from_attributes = True