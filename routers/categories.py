from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import schemas, models, database
from utils.auth import get_current_user, verify_role
from models import Category
from schemas import CategoryCreate
from sqlalchemy.orm import joinedload
from fastapi.encoders import jsonable_encoder

router = APIRouter()

# Crear una nueva categoría o subcategoría
@router.post("/", response_model=schemas.Category)
def create_category(
    category: schemas.CategoryCreate, 
    db: Session = Depends(database.get_db), 
    current_user: schemas.User = Depends(get_current_user)
):
    verify_role(current_user.roles, "admin")  # Solo administradores pueden crear categorías
    
    db_category = models.Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# Obtener una categoría por ID
@router.get("/{category_id}", response_model=schemas.Category)
def read_category(category_id: int, db: Session = Depends(database.get_db)):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

# Listar categorías y subcategorías
@router.get("/", response_model=List[schemas.Category])
async def read_categories(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    categories = db.query(Category).options(joinedload(Category.subcategories)).offset(skip).limit(limit).all()
    return jsonable_encoder(categories)

# Actualizar una categoría o subcategoría
@router.put("/{category_id}", response_model=schemas.Category)
def update_category(
    category_id: int, 
    category: schemas.CategoryCreate, 
    db: Session = Depends(database.get_db), 
    current_user: schemas.User = Depends(get_current_user)
):
    verify_role(current_user.roles, "admin")  # Solo administradores pueden actualizar categorías
    
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    
    for key, value in category.dict().items():
        setattr(db_category, key, value)
    
    db.commit()
    db.refresh(db_category)
    return db_category

# Eliminar una categoría o subcategoría
@router.delete("/{category_id}", response_model=schemas.Category)
def delete_category(
    category_id: int, 
    db: Session = Depends(database.get_db), 
    current_user: schemas.User = Depends(get_current_user)
):
    verify_role(current_user.roles, "admin")  # Solo administradores pueden eliminar categorías
    
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    
    db.delete(db_category)
    db.commit()
    return db_category
