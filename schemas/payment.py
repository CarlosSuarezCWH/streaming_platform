from pydantic import BaseModel
from datetime import datetime

class PaymentBase(BaseModel):
    purchase_id: int
    amount: float
    payment_method: str
    status: str  # Estado del pago: 'completed', 'pending', 'failed', etc.

class PaymentCreate(PaymentBase):
    pass

class Payment(PaymentBase):
    id: int
    transaction_date: datetime

    class Config:
        orm_mode = True
