from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class ReservationStatus(str, Enum):
    Approved = "Approved"
    Denied = "Denied"
    Pending = "Pending"

class CreateReservation(BaseModel):
    id_resident: int
    id_area: int
    event_date: datetime
    notes: Optional[str] = None
