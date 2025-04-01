from pydantic import BaseModel, Field
from typing import Optional

class StatusQR(str, enum.Enum):
    Active = "Active"
    Used = "Used"
    Expired = "Expired"
    Revoked = "Revoked"


class NewVisitorRegistration(BaseModel):
    id_document: str
    first_name: str
    second_name: Optional[str] = None
    first_last_name: str
    second_last_name: Optional[str] = None
    phone_number: str
    is_adult: bool
    picture: bytes
    resident_id: int
    StatuQR: StatusQR = StatusQR.Active
