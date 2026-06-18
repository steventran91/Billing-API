from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timezone
from ..models.line_item import LineItem
from ..services.invoice import get_invoice

def get_line_items(db: Session, invoice_id: int, tenant_id: int) -> list[LineItem]:
    invoice = get_invoice(db=db, invoice_id=invoice_id, tenant_id=tenant_id)
    line_items = db.query(LineItem).filter(LineItem.invoice_id == invoice.id).all()
    return line_items

