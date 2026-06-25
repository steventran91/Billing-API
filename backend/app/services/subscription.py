from sqlalchemy.orm import Session
from datetime import datetime, timezone
from ..models.invoice import Invoice
from ..models.subscription import Subscription
from ..models.line_item import LineItem


def get_due_subscriptions(db: Session) -> list[Subscription]:
    subscriptions = db.query(Subscription).filter(Subscription.status == "active").all()
    due_subscriptions = []
    for sub in subscriptions:
        invoice = db.query(Invoice).join(LineItem ,LineItem.invoice_id == Invoice.id).filter(LineItem.subscription_id == sub.id).order_by(Invoice.due_date.desc()).first()
        if not invoice:
            due_subscriptions.append(sub)
        else:
            if invoice.due_date <= datetime.now(timezone.utc):
                due_subscriptions.append(sub)
        
    
    return due_subscriptions