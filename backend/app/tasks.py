from .celery_app import celery
from .database import SessionLocal
from .services.invoice import create_invoice


@celery.task
def generate_invoice(subscription_id):
    db = SessionLocal()
    try:
        create_invoice(subscription_id, db=db)
    finally:
        db.close()
