from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(255))
    avatar_url = Column(String(255), nullable=True)
    pin = Column(String(4), nullable=True)
    avatar_url = Column(String, nullable=True)
    can_purchase = Column(Boolean, default=False)
    restricted_categories = Column(String(255), nullable=True)  # IDs de categorías restringidas
    hidden_events = Column(String(255), nullable=True)  # IDs de eventos ocultos

    parent_user = relationship("User", back_populates="profiles")
