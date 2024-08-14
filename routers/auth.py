from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import schemas, models, utils, database
from schemas.user import EmailStr, ResetPassword
from utils.auth import create_access_token, get_password_hash, verify_password, decode_access_token, get_current_user
from utils.email import send_email
from datetime import timedelta
from pydantic import EmailStr  # Importa EmailStr directamente desde pydantic
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()

@router.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(database.get_db)
):
    db_user = db.query(models.User).filter(models.User.email == form_data.username).first()

    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=utils.auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.email, "user_id": db_user.id, "roles": [role.name for role in db_user.roles]},  # Añadir roles al token
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
@router.post("/request-password-reset")
def request_password_reset(email: EmailStr, db: Session = Depends(database.get_db)):  # Usar pydantic's EmailStr
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Email not registered")
    reset_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(hours=1))
    reset_link = f"http://yourdomain.com/reset-password?token={reset_token}"
    send_email(
        to_email=email,
        subject="Password Reset Request",
        body=f"Click the link to reset your password: {reset_link}"
    )
    return {"msg": "Password reset email sent"}

@router.post("/reset-password")
def reset_password(reset_data: ResetPassword, db: Session = Depends(database.get_db)):
    token_data = decode_access_token(reset_data.token)
    if token_data is None:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = db.query(models.User).filter(models.User.email == token_data.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid token or email")
    user.hashed_password = get_password_hash(reset_data.new_password)
    db.commit()
    return {"msg": "Password reset successful"}

@router.get("/me", response_model=schemas.User)
def get_current_user_info(current_user: schemas.User = Depends(get_current_user)):
    print (current_user)
    return current_user

def verify_role(user_roles, required_role: str):
    if required_role not in [role.name for role in user_roles]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"No tienes el rol necesario: {required_role}",
        )