from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Float
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    event_id = Column(Integer, ForeignKey("events.id"))  # Referencia a la tabla de eventos
    purchase_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="completed")
    
    user = relationship("User")
    event = relationship("Event")  # Relación con el evento
    payment = relationship("Payment", back_populates="purchase", uselist=False)