from sqlalchemy import Integer, String, DateTime, ForeignKey, Column, Boolean, Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database import Base
import uuid
from enum import Enum


class ResidentType(str, Enum):
    Owner = "Owner"
    Tenant = "Tenant"
    Head = "Head"
    Occupant = "Occupant"


class Residents(Base):
    __tablename__ = "residents"

    id_residents = Column(UUID(as_uuid=True),
                          primary_key=True, default=uuid.uuid4)
    person_id = Column(Integer, ForeignKey(
        "persons.id_person"), nullable=False)
    resident_house_id = Column(String, ForeignKey(
        "properties.property_number"), nullable=False)
    resident_type = Column(SQLAlchemyEnum(
        ResidentType, name='residentstypes'), nullable=False)
    is_active = Column(Boolean, default=True)
    resident_qr = Column(String, nullable=False)

    person = relationship("persons", back_populates="residents")
    resident_house = relationship("Properties", back_populates="residents")
