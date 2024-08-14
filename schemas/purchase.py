from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PurchaseBase(BaseModel):
    user_id: int
    event_id: int  # Ya no es necesario tener subevent_id

class PurchaseCreate(PurchaseBase):
    pass

class Purchase(PurchaseBase):
    id: int
    status: Optional[str]  # Permitir que status sea opcional

    class Config:
        orm_mode = True
