from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    purchase_id = Column(Integer, ForeignKey("purchases.id"))
    amount = Column(Float, nullable=False)
    payment_method = Column(String(50), nullable=False)  # PayPal, Tarjeta, Transferencia, etc.
    status = Column(String(50), nullable=False)  # Completado, Pendiente, Fallido, etc.
    transaction_date = Column(DateTime, default=datetime.utcnow)
    
    purchase = relationship("Purchase", back_populates="payment")

