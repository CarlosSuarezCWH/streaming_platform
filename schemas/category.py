from pydantic import BaseModel
from typing import List, Optional

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    parent_category_id: Optional[int] = None  # Opcional para subcategorías

class Category(BaseModel):
    id: int
    name: str
    parent_category_id: Optional[int] = None


    class Config:
        orm_mode = True
