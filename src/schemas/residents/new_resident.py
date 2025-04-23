from pydantic import BaseModel, UUID4
from typing import Optional
from enum import Enum

class ResidentType(str, Enum):
    Owner = "Owner"
    Tenant = "Tenant"
    Head = "Head"
    Occuopant = "Occuopant"

class ResidentBase(BaseModel):
    person: UUID4
    resident_house: str 

class ResidentCreate(ResidentBase):
    resident_type: ResidentType

class ResidentResponse(ResidentBase):
    id_resident: UUID4
    is_active: bool
    resident_qr: str

    class config:
        from_attributes = True

