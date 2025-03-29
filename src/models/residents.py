from sqlalchemy import Integer, String, DateTime, ForeignKey, Column, Boolean
from sqlalchemy.orm import relationship
from database import Base
import uuid

class ResidentType(Str, Enum):
    Owner = "Owner"
    Tenant = "Tenant"
    Head = "Head"
    Occupant = "Occupant"


class residents(Base):
    __tablename__ = "residents"

    id_residents = Column(as_uuid=true, primary_key=true, default=uuid.uuid4)
    person = Column(Integer, ForeignKey("persons.id_person"), nullable=False)
    resident_house = column(String, ForeignKey("properties.property_number"), nullable=False)
    resident_type = Column(Enum(ResidentType), nullable=False)
    is_active = Column(Boolean, default=True)
    resident_qr = Column(String, nullable=False)

    person = relationship("persons" back_populates="resident")
    resident_house = relationship("Properties", back_populates="resident")