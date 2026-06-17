from typing import Optional
from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime

class InvoiceOut(BaseModel):
    id: int
    tenant_id: int 
    status: str
    total_amount: Decimal
    due_date: datetime
    payment_date: Optional[datetime] = None
    issued_at: datetime

    model_config = {"from_attributes": True}

class InvoiceListOut(BaseModel):
    id: int
    status: str
    tenant_id: int
    total_amount: Decimal
    due_date: datetime

    model_config = {"from_attributes": True}

