from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import schemas, models, database
from utils.auth import get_current_user, verify_role
from schemas.event import EventWithStream

router = APIRouter()

# Obtener el evento más popular
@router.get("/popular", response_model=schemas.Event)
def get_popular_event(db: Session = Depends(database.get_db)):
    popular_event = db.query(models.Event).order_by(models.Event.popularity.desc()).first()
    if not popular_event:
        raise HTTPException(status_code=404, detail="No popular event found")
    return popular_event

# Buscar eventos por título
@router.get("/search", response_model=List[schemas.Event])
def search_events(query: str, db: Session = Depends(database.get_db)):
    results = db.query(models.Event).filter(models.Event.title.ilike(f"%{query}%")).all()
    if not results:
        raise HTTPException(status_code=404, detail="No matching events found")
    return results

# Crear un nuevo evento o subevento
@router.post("/", response_model=schemas.Event)
def create_event(
    event: schemas.EventCreate, 
    db: Session = Depends(database.get_db), 
    current_user: schemas.User = Depends(get_current_user)
):
    verify_role(current_user.roles, "admin")  # Solo administradores pueden crear eventos
    
    db_event = models.Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

# Obtener un evento por ID
@router.get("/{event_id}", response_model=schemas.Event)
def read_event(
    event_id: int, 
    profile_id: int = None, 
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Si se proporciona un profile_id, verificar restricciones
    if profile_id:
        db_profile = db.query(models.Profile).filter(
            models.Profile.id == profile_id,
            models.Profile.user_id == current_user.id
        ).first()
        
        if not db_profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        # Verificar si el evento está oculto
        if db_profile.hidden_events and str(event_id) in db_profile.hidden_events.split(','):
            raise HTTPException(status_code=403, detail="Access denied: Event is hidden for this profile")
        
        # Verificar si la categoría del evento está restringida
        if db_profile.restricted_categories and str(db_event.category_id) in db_profile.restricted_categories.split(','):
            raise HTTPException(status_code=403, detail="Access denied: Category is restricted for this profile")
    
    return db_event

# Listar eventos con paginación y posibles restricciones de perfil
@router.get("/", response_model=List[schemas.Event])
def read_events(
    profile_id: Optional[int] = None,
    parent_event_id: Optional[int] = None,  # Filtra por subeventos de este evento
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(database.get_db)
):
    query = db.query(models.Event)
    
    if parent_event_id is not None:
        query = query.filter(models.Event.parent_event_id == parent_event_id)

    # Si se proporciona un profile_id, aplicar restricciones
    if profile_id:
        db_profile = db.query(models.Profile).filter(
            models.Profile.id == profile_id
        ).first()

        if not db_profile:
            raise HTTPException(status_code=404, detail="Profile not found")

        # Aplicar restricciones de categorías
        if db_profile.restricted_categories:
            restricted_category_ids = [int(id) for id in db_profile.restricted_categories.split(',')]
            query = query.filter(~models.Event.category_id.in_(restricted_category_ids))
        
        # Aplicar eventos ocultos
        if db_profile.hidden_events:
            hidden_event_ids = [int(id) for id in db_profile.hidden_events.split(',')]
            query = query.filter(~models.Event.id.in_(hidden_event_ids))

    events = query.offset(skip).limit(limit).all()
    return events

# Actualizar un evento
@router.put("/{event_id}", response_model=schemas.Event)
def update_event(
    event_id: int, 
    event: schemas.EventCreate, 
    db: Session = Depends(database.get_db), 
    current_user: schemas.User = Depends(get_current_user)
):
    verify_role(current_user.roles, "admin")  # Solo administradores pueden actualizar eventos
    
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    for key, value in event.dict().items():
        setattr(db_event, key, value)
    
    db.commit()
    db.refresh(db_event)
    print(db_event)
    return db_event

# Eliminar un evento
@router.delete("/{event_id}", response_model=schemas.Event)
def delete_event(
    event_id: int, 
    db: Session = Depends(database.get_db), 
    current_user: schemas.User = Depends(get_current_user)
):
    verify_role(current_user.roles, "admin")  # Solo administradores pueden eliminar eventos
    
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    db.delete(db_event)
    db.commit()
    return db_event

# Obtener un evento con su URL de streaming, verificando si el usuario lo ha comprado
@router.get("/{event_id}/stream", response_model=schemas.Event)
def read_event_with_stream(
    event_id: int, 
    db: Session = Depends(database.get_db), 
    current_user: schemas.User = Depends(get_current_user)
):
    # Verifica si el usuario ha comprado el evento o su subevento
    purchase = db.query(models.Purchase).filter(
        models.Purchase.user_id == current_user.id, 
        models.Purchase.event_id == event_id
    ).first()
    
    if not purchase:
        raise HTTPException(status_code=403, detail="Access denied: You have not purchased this event")

    # Devuelve el evento con su URL de streaming
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if db_event:
        return db_event
    else:
        raise HTTPException(status_code=404, detail="Event not found")
