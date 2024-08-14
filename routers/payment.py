from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
import schemas, models, database
from utils.auth import get_current_user
from typing import List

router = APIRouter()

@router.post("/", response_model=schemas.Payment)
def create_payment(payment: schemas.PaymentCreate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    # Verificar si la compra existe y pertenece al usuario
    db_purchase = db.query(models.Purchase).filter(models.Purchase.id == payment.purchase_id, models.Purchase.user_id == current_user.id).first()
    if not db_purchase:
        raise HTTPException(status_code=404, detail="Purchase not found or not associated with this user")
    
    # Crear el pago
    db_payment = models.Payment(
        purchase_id=payment.purchase_id,
        amount=payment.amount,
        payment_method=payment.payment_method,
        status="completed",  # Aquí podrías integrar la lógica del procesador de pagos
        transaction_date=datetime.utcnow()
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    
    # Actualizar el estado de la compra
    db_purchase.status = "completed"
    db.commit()
    
    return db_payment

@router.get("/{payment_id}", response_model=schemas.Payment)
def read_payment(payment_id: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    db_payment = db.query(models.Payment).join(models.Purchase).filter(models.Payment.id == payment_id, models.Purchase.user_id == current_user.id).first()
    if not db_payment:
        raise HTTPException(status_code=404, detail="Payment not found or not associated with this user")
    return db_payment

@router.get("/", response_model=List[schemas.Payment])
def read_payments(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    payments = db.query(models.Payment).join(models.Purchase).filter(models.Purchase.user_id == current_user.id).offset(skip).limit(limit).all()
    return payments
