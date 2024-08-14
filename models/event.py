from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from database import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    description = Column(String(255), index=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    price = Column(Float)
    image_url = Column(String(255), nullable=True)
    stream_url = Column(String(255), nullable=False)
    popularity = Column(Integer, default=0)
    category_id = Column(Integer, ForeignKey("categories.id"))
    parent_event_id = Column(Integer, ForeignKey("events.id"), nullable=True)  # Referencia al evento padre
    
    subevents = relationship("Event", backref="parent_event", remote_side=[id])  # Relación con subeventos
    category = relationship("Category", back_populates="events")
