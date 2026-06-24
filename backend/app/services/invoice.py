from decimal import Decimal
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timezone, timedelta
from ..models.invoice import Invoice
from ..models.subscription import Subscription
from ..models.subscription_plan import SubscriptionPlan
from ..models.line_item import LineItem

# get_invoices(db, tenant_id) returns all invoices for a tenant
def get_invoices(db: Session, tenant_id: int) -> list[Invoice]:
    invoices = db.query(Invoice).filter(Invoice.tenant_id == tenant_id).all()
    return invoices

# get_invoice(db, invoice_id) returns one invoice, raises 404 if not found
def get_invoice(db: Session, invoice_id: int, tenant_id: int) -> Invoice:
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id, Invoice.tenant_id == tenant_id).first()
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found"
        )
    return invoice
# pay_invoice(db, invoice_id) marks invoice as paid, sets payment_date
def pay_invoice(db: Session, invoice_id: int, tenant_id: int) -> Invoice:
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id, Invoice.tenant_id == tenant_id).first()
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found",
        )
    if invoice.status == "paid":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invoice has already been paid",
        )

    invoice.status = "paid"
    invoice.payment_date = datetime.now(timezone.utc)
    db.commit()
    db.refresh(invoice)
    return invoice

def create_invoice(subscription_id: int, db: Session) -> Invoice:
    subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not subscription:
        raise ValueError(
            "Subscription not found"
        )
    subscripion_plan = db.query(SubscriptionPlan).filter(SubscriptionPlan.id == subscription.subscription_plan_id).first()
    if not subscripion_plan:
        raise ValueError(
            "Subscription plan not found"
        )
    
    issued_at = datetime.now(timezone.utc)

    invoice = Invoice(
        tenant_id = subscription.tenant_id,
        status = "unpaid",
        total_amount = Decimal("0.00"),
        issued_at = issued_at,
        due_date = issued_at + timedelta(days=subscripion_plan.billing_cycle),
        payment_date = None, 
    )
    db.add(invoice)
    db.commit()
    db.refresh(invoice)

    line_item = LineItem(
        amount = subscripion_plan.price,
        description = subscripion_plan.name,
        subscription_id = subscription.id,
        invoice_id = invoice.id,
    )
    invoice.total_amount = line_item.amount
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    db.add(line_item)
    db.commit()
    db.refresh(line_item)

    return invoice
        
    