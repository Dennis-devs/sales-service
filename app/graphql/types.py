import strawberry
from typing import List, Optional
from datetime import datetime

@strawberry.type
class CustomerType:
    id: int
    name: str
    phone: str

@strawberry.type
class OrderType:
    id: int
    item: str
    amount: float
    time: datetime
    customer: Optional[CustomerType]

@strawberry.type
class MutationResponse:
    success: bool
    message: str
    order: Optional[OrderType]    