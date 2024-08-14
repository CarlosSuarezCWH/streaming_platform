import os
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
from schemas import TokenData
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import List
from dotenv import load_dotenv
from database import get_db
from sqlalchemy.orm import Session
import models, schemas
#informacion para poder subir un commit :)
# Cargar las variables de entorno
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")  # Definir oauth2_scheme

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "id": data.get("id")})  # Incluir id
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        user_id: int = payload.get("user_id")  # Asegúrate de que se obtenga el user_id
        if email is None or user_id is None:
            raise credentials_exception()
        token_data = TokenData(email=email, id=user_id)  # Asegúrate de pasar el user_id
        return token_data
    except JWTError:
        raise credentials_exception()

def credentials_exception() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

def verify_role(user_roles: List[str], required_role: str):
    if required_role not in user_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have the necessary permissions",
        )

# Dependency to get the current user based on the access token
async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> schemas.User:
    # Decodificar el token de acceso
    token_data = decode_access_token(token)
    if token_data is None:
        raise credentials_exception()

    # Consultar el usuario en la base de datos
    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    if user is None:
        raise credentials_exception()

    # Devolver el objeto User completo
    return schemas.User.from_orm(user)

# Dependency to get the current active user
async def get_current_active_user(current_user: TokenData = Depends(get_current_user)) -> TokenData:
    # Aquí puedes agregar la lógica para verificar si el usuario está activo
    return current_user

# Dependency to get the current superuser
async def get_current_superuser(current_user: TokenData = Depends(get_current_user)) -> TokenData:
    verify_role(current_user.roles, "superuser")
    return current_user

def verify_role(user_roles, required_role: str):
    if required_role not in [role.name for role in user_roles]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"No tienes el rol necesario: {required_role}",
        )