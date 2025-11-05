import strawberry
from sqlalchemy.orm import Session
from app.models import Customer, Order
from app.sms import send_sms #SMS function (implement later)
from app.database import SessionLocal
from .types import MutationResponse, OrderType, CustomerType

@strawberry.input # Annotates a class as a GraphQL Input type
class CreateCustomerInput:
    name: str
    phone: str

@strawberry.input
class CreateOrderInput:
    customer__phone: str
    item: str
    amount: float
    # Time is auto-generated, so not needed here

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# create customers/orders, trigger SMS, and return responses.

@strawberry.mutation # Annotates a method or property as a GraphQL mutation
def create_customer(input: CreateCustomerInput) -> CustomerType:
    db = next(get_db())
    db_customer = Customer(name=input.name, phone=input.phone)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer) # Reload from DB to get ID
    return CustomerType(id=db_customer.id, name=db_customer.name, phone=db_customer.phone)

@strawberry.mutation
def create_order(input: CreateOrderInput) -> MutationResponse:
    db = next(get_db())
    customer = db.query(Customer).filter(Customer.phone == input.customer__phone).first()
    if not customer:
        return MutationResponse(success=False, message="Customer not found", order=None)
    
    db_order = Order(
        item=input.item,
        amount=input.amount,
        customer_id=customer.id
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order) # Reload from DB to get ID and time

    # Trigger SMS
    message = f"New order: {input.item} for amount ${input.amount}."
    send_sms(to=customer.phone, message=message)

    order_type = OrderType(
        id=db_order.id,
        item=db_order.item,
        amount=db_order.amount,
        time=db_order.time,
        customer=CustomerType(
            id=customer.id,
            name=customer.name,
            phone=customer.phone
        )
    )
    return MutationResponse(success=True, message="Order created successfully and SMS sent", order=order_type)        