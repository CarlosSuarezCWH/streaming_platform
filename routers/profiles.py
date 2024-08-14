from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import schemas, models, database
from utils.auth import get_current_user
from schemas.profile import ProfileCreate, ProfileUpdate, Profile 
import shutil
import os

router = APIRouter()

@router.post("/", response_model=schemas.Profile)
def create_profile(profile: schemas.ProfileCreate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    db_profile = models.Profile(**profile.dict(), user_id=current_user.id)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

@router.get("/", response_model=List[schemas.Profile])
def read_profiles(db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    # Buscar al usuario en la base de datos usando el ID
    db_user = db.query(models.User).filter(models.User.id == current_user.id).first()
    
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return db_user.profiles

@router.put("/{profile_id}", response_model=schemas.Profile)
def update_profile(profile_id: int, profile: ProfileUpdate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    db_profile = db.query(models.Profile).filter(models.Profile.id == profile_id, models.Profile.user_id == current_user.id).first()
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    for key, value in profile.dict(exclude_unset=True).items():
        setattr(db_profile, key, value)

    db.commit()
    db.refresh(db_profile)
    return db_profile


@router.delete("/{profile_id}", response_model=schemas.Profile)
def delete_profile(profile_id: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    db_profile = db.query(models.Profile).filter(models.Profile.id == profile_id, models.Profile.user_id == current_user.id).first()
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    db.delete(db_profile)
    db.commit()
    return db_profile

# Subir imagen de avatar
@router.post("/{profile_id}/avatar")
def upload_avatar(profile_id: int, file: UploadFile = File(...), db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    db_profile = db.query(models.Profile).filter(models.Profile.id == profile_id, models.Profile.user_id == current_user.id).first()
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    file_location = f"static/avatars/{profile_id}_{file.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    
    db_profile.avatar_url = file_location
    db.commit()
    db.refresh(db_profile)
    return {"info": "Avatar uploaded successfully", "url": file_location}

# Seleccionar perfil al iniciar sesión
@router.get("/select/{profile_id}", response_model=schemas.Profile)
def select_profile(profile_id: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    db_profile = db.query(models.Profile).filter(models.Profile.id == profile_id, models.Profile.user_id == current_user.id).first()
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    return db_profile
