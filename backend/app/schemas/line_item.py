from typing import Optional
from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime

class LineItemOut(BaseModel):
    id: int
    invoice_id: int
    subscription_id: int 
    description: str 
    amount: Decimal 
    created_at: datetime 

    model_config = {"from_attributes": True}
