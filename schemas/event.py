from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class EventBase(BaseModel):
    title: str
    description: str
    start_time: datetime
    end_time: datetime
    image_url: Optional[str] = None
    price: float
    stream_url: str
    parent_event_id: Optional[int] = None  # Permite identificar subeventos

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int
    category_id: int
    subevents: Optional[List["Event"]] = None  # Permitir None en subevents

    class Config:
        orm_mode = True

class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    image_url: Optional[str] = None
    price: Optional[float] = None
    stream_url: Optional[str] = None
    parent_event_id: Optional[int] = None

class EventDelete(BaseModel):
    id: int
    category_id: int

class EventList(BaseModel):
    events: List[Event]

class EventWithStream(Event):
    stream_url: str

    class Config:
        orm_mode = True
