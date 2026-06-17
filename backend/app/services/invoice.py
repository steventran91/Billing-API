from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timezone
from ..models.invoice import Invoice

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
    
