from typing import Optional
from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime

class LineItemOut(BaseModel):
    id: int
    invoice_id: int
    sub

    model_config = {"from_attributes": True}