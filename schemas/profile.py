from pydantic import BaseModel
from typing import Optional, List

class ProfileBase(BaseModel):
    name: str
    pin: Optional[str] = None
    avatar_url: Optional[str] = None
    can_purchase: bool = False
    restricted_categories: Optional[List[int]] = None
    hidden_events: Optional[List[int]] = None

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(ProfileBase):
    pass

class Profile(ProfileBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
