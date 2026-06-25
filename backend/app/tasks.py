from .celery_app import celery
from .database import SessionLocal
from .services.invoice import create_invoice
from .services.subscription import get_due_subscriptions


@celery.task
def generate_invoice(subscription_id):
    db = SessionLocal()
    try:
        create_invoice(subscription_id, db=db)
    finally:
        db.close()

@celery.task
def dispatch_due_invoices():
    db = SessionLocal()
    try:
        subscriptions = get_due_subscriptions(db)
        for sub in subscriptions:
            generate_invoice.delay(sub.id)
    finally:
        db.close()
