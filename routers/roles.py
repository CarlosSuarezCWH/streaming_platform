from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import schemas, models, database
from utils.auth import get_current_user, verify_role
#info de commit
router = APIRouter()

@router.post("/assign-role", response_model=schemas.User)
def assign_role_to_user(
    user_id: int, 
    role_name: str, 
    db: Session = Depends(database.get_db), 
    current_user: schemas.User = Depends(get_current_user)
):
    # Solo los superusuarios pueden asignar roles
    verify_role(current_user.roles, "admin")
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    role = db.query(models.Role).filter(models.Role.name == role_name).first()

    if not user or not role:
        raise HTTPException(status_code=404, detail="Usuario o rol no encontrado")
    
    user.roles.append(role)
    db.commit()
    db.refresh(user)
    return user


@router.post("/remove-role", response_model=schemas.User)
def remove_role_from_user(user_id: int, role_name: str, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    verify_role(current_user.roles, "admin")
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    role = db.query(models.Role).filter(models.Role.name == role_name).first()

    if not user or not role:
        raise HTTPException(status_code=404, detail="User or role not found")
    
    user.roles.remove(role)
    db.commit()
    db.refresh(user)
    return user
