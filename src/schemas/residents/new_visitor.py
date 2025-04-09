from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class StatusQR(str, Enum):
    Active = "Active"
    Used = "Used"
    Expired = "Expired"
    Revoked = "Revoked"


class NewVisitorRegistration(BaseModel):
    id_document: str
    first_name: str
    second_name: Optional[str] = None
    first_lastname: str
    second_lastname: Optional[str] = None
    phone_number: str
    is_adult: bool
    picture: Optional[bytes] = None
    resident_id: int
    StatuQR: StatusQR = StatusQR.Active
