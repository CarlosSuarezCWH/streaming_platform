from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    parent_category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    subcategories = relationship("Category", backref='parent', remote_side=[id])
    events = relationship("Event", back_populates="category")
