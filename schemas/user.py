from pydantic import BaseModel, EmailStr, validator
from typing import List, Optional

class ProfileBase(BaseModel):
    name: str
    pin: Optional[str] = None
    avatar_url: Optional[str] = None
    can_purchase: bool = False
    restricted_categories: Optional[List[int]] = None
    hidden_events: Optional[List[int]] = None

    # Validadores para convertir cadenas a listas
    @validator('restricted_categories', pre=True, always=True)
    def convert_restricted_categories(cls, v):
        if isinstance(v, str):
            return [int(x) for x in v.split(',')] if v else []
        return v

    @validator('hidden_events', pre=True, always=True)
    def convert_hidden_events(cls, v):
        if isinstance(v, str):
            return [int(x) for x in v.split(',')] if v else []
        return v

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(ProfileBase):
    pass

class Profile(ProfileBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class RoleBase(BaseModel):
    name: str

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    email: str
    is_active: bool
    is_superuser: bool
    email_verified: bool
    roles: List[Role] = []
    profiles: List[Profile] = []  # Relación con los perfiles adicionales

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[EmailStr] = None
    id: Optional[int] = None

class UserLogin(BaseModel):
    username: EmailStr
    password: str

class ResetPassword(BaseModel):
    email: EmailStr
    new_password: str
    token: str
