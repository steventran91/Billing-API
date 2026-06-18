from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.invoice import Invoice
from ..schemas.invoice import InvoiceOut, InvoiceListOut
from ..services.invoice import get_invoice, get_invoices, pay_invoice
from ..core.dependencies import get_current_user

router = APIRouter(prefix="/invoices", tags=["invoices"])

@router.get("/", response_model=list[InvoiceListOut])
def get_invoice_list(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return get_invoices(db=db, tenant_id=current_user.tenant_id)

@router.get("/{invoice_id}", response_model=InvoiceOut)
def get_invoice_by_id(invoice_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return get_invoice(db=db, invoice_id=invoice_id, tenant_id=current_user.tenant_id)

@router.post("/{invoice_id}/pay", response_model=InvoiceOut)
def make_invoice_payment(invoice_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return pay_invoice(invoice_id=invoice_id, db=db, tenant_id=current_user.tenant_id)