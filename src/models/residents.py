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

    id_residents = Column(Integer,
                          primary_key=True, default=uuid.uuid4)
    person = Column(Integer, ForeignKey("persons.id_person"), nullable=False)
    resident_house = Column(String, nullable=False)
    resident_type = Column(SQLAlchemyEnum(
        ResidentType, name='residentstypes'), nullable=False)
    is_active = Column(Boolean, default=True)
    resident_qr = Column(String, nullable=False)

    # Relación con Person
    person_resident_info = relationship("Person", back_populates="residents")

    # Relación con PendingResidentRequest (como residente)
    pending_reqs = relationship(
        'PendingResidentRequest',
        back_populates='residents_info',
        foreign_keys='PendingResidentRequest.resident'  # Especifica la clave foránea
    )

    # Relación con PendingResidentRequest (como cabeza de familia)
    pending_reqs_head = relationship(
        'PendingResidentRequest',
        back_populates='residents_head_info',
        foreign_keys='PendingResidentRequest.head'  # Especifica la clave foránea
    )

    reservation = relationship('Reservation', back_populates='residents')

    payment_calender_info = relationship(
        "PaymentCalender", back_populates="resident_info") 
    
    visitor_qr_codes = relationship("VisitorQRCode", back_populates="resident_id")
