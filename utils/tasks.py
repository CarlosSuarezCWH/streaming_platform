from celery_app import celery_app
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models import Event, Purchase, User
from database import SessionLocal
from utils.notifications import send_notification  # Importa la función de notificaciones

@celery_app.task
def notify_users_of_upcoming_event():
    db: Session = SessionLocal()
    try:
        now = datetime.utcnow()
        upcoming_events = db.query(Event).filter(
            Event.start_time.between(now, now + timedelta(hours=1))
        ).all()

        for event in upcoming_events:
            purchases = db.query(Purchase).filter(
                Purchase.event_id == event.id
            ).all()

            for purchase in purchases:
                user = db.query(User).filter(User.id == purchase.user_id).first()
                if user:
                    send_notification(
                        to_email=user.email,
                        subject=f"Recordatorio: El evento {event.title} está por comenzar",
                        body=f"Hola {user.email},\n\nEl evento {event.title} comenzará pronto. ¡No te lo pierdas!"
                    )
    finally:
        db.close()
