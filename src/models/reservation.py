from sqlalchemy import Integer, String, DateTime, ForeignKey, Column, Boolean, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from database import Base
from enum import Enum
from datetime import datetime
from models.social_areas import SocialArea


class ReservationStatus(str, Enum):
    Approved = 'Approved'
    Denied = 'Denied'
    Pending = 'Pending'


class Reservation(Base):
    __tablename__ = 'reservation'

    id_reservation = Column(Integer, primary_key=True, nullable=False)
    id_resident = Column(Integer, ForeignKey(
        'residents.id_residents'), nullable=False)
    id_area = Column(Integer, ForeignKey(
        'social_areas.id_social_area'), nullable=False)
    event_date = Column(DateTime, nullable=False)
    event_status = Column(SQLAlchemyEnum(
        ReservationStatus, names='reservationstatus'))
    approved_by = Column(Integer, ForeignKey(
        'residential_management.id_residential_management'), nullable=True)#hay que modificar esta columna en la DDBB para que si pueda ser null y que una ves sea aprrovada o denegada pase a tener el valor del managemen
    created_at = Column(DateTime, default=datetime.now())
    notes = Column(String(500), nullable=True)

    residential_management = relationship(
        'ResidentialManagement', back_populates='reservation', foreign_keys=[approved_by])

    social_area_info = relationship(
        'SocialArea', back_populates='reservation', foreign_keys=[id_area])

    residents = relationship(
        'Residents', back_populates='reservation', foreign_keys=[id_resident])
