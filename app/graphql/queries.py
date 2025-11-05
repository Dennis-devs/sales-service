import strawberry
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import Customer, Order
from app.database import SessionLocal # DB session factory
from .types import OrderType, CustomerType

def get_db() -> Session: # Helper for DB sessions (dependency injection style)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@strawberry.field
def customer(phone: str) -> Optional[CustomerType]:
    db = next(get_db()) # Get DB session
    db_customer = db.query(Customer).filter(Customer.phone == phone).first()
    if not db_customer:
        return None
    return CustomerType(id=db_customer.id, name=db_customer.name, phone=db_customer.phone)        

@strawberry.field # Marks a function as a GraphQL query resolver
def orders_by_customer(phone: str) -> List[OrderType]:
    db = next(get_db()) # Get DB session
    customer = db.query(Customer).filter(Customer.phone == phone).first()
    if not customer:
        return []
    return [
        OrderType(
            id=order.id,
            item=order.item,
            amount=order.amount,
            time=order.time,
            customer=CustomerType(
                id=customer.id,
                name=customer.name,
                phone=customer.phone
            )
        ) for order in customer.orders
    ]