from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime


class PendingPaymentsCreate(BaseModel):
    payment_descrtiption: str
    amount: float
    generation_date: datetime
    payment_date: datetime
    is_active: bool
    residential_management: int


class PaymentCalenderCreate(BaseModel):
    pendig_payment: int
    status: str

    class Config:
        orm_mode = True
