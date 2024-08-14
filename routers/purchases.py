from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import schemas, models, database
from utils.auth import get_current_user, verify_role

router = APIRouter()

@router.post("/", response_model=schemas.Purchase)
def create_purchase(purchase: schemas.PurchaseCreate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    db_user = db.query(models.User).filter(models.User.id == purchase.user_id).first()
    db_event = db.query(models.Event).filter(models.Event.id == purchase.event_id).first()
    db_subevent = db.query(models.SubEvent).filter(models.SubEvent.id == purchase.subevent_id).first() if purchase.subevent_id else None
    
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    if purchase.subevent_id and not db_subevent:
        raise HTTPException(status_code=404, detail="Subevent not found")
    
    # Crear la compra para el evento principal
    db_purchase = models.Purchase(user_id=purchase.user_id, event_id=purchase.event_id, subevent_id=purchase.subevent_id)
    db.add(db_purchase)
    db.commit()
    db.refresh(db_purchase)
    
    # Crear compras para todos los subeventos si el usuario compró el evento principal
    if not purchase.subevent_id:  # Si se compra el evento principal
        for subevent in db_event.subevents:
            db_subevent_purchase = models.Purchase(user_id=purchase.user_id, event_id=purchase.event_id, subevent_id=subevent.id)
            db.add(db_subevent_purchase)
        db.commit()
    
    return db_purchase


@router.get("/{user_id}", response_model=List[schemas.Purchase])
def read_purchases(user_id: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    # Solo el usuario o un administrador pueden ver las compras
    if current_user.id != user_id:
        verify_role(current_user.roles, "admin")
    
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    purchases = db.query(models.Purchase).filter(models.Purchase.user_id == user_id).all()
    return purchases

@router.get("/check_access/{user_id}/{event_id}", response_model=bool)
def check_user_access(user_id: int, event_id: int, db: Session = Depends(database.get_db)):
    purchase = db.query(models.Purchase).filter(models.Purchase.user_id == user_id, models.Purchase.event_id == event_id).first()
    if purchase:
        return True
    return False
