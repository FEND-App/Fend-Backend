from sqlalchemy import Integer, String, DateTime, ForeignKey, Column, Boolean
from sqlalchemy.orm import relationship
from database import Base


class ResidentialManagement(Base):
    __tablename__ = "residential_management"

    id_residential_management = Column(Integer, primary_key=True, index=True)
    residential = Column(Integer, ForeignKey(
        "residential_area.id_residential_area"), nullable=False)
    person = Column(Integer, ForeignKey("persons.id_person"), nullable=False)
    employee_star_date = Column(DateTime, nullable=False)
    employee_mobile_phone = Column(String(30), nullable=False)
    employee_email = Column(String(100), nullable=False)
    is_active = Column(Boolean, nullable=True, default=True)
    role = Column(String(100), nullable=False)

    # Relaciones
    residential_area = relationship(
        "ResidentialArea", back_populates="managements")
    person_details = relationship("Person", back_populates="managements")

    reservation = relationship(
        'Reservation', back_populates='residential_management')

    news = relationship('News', back_populates='residential_management_info')

    pending_payments = relationship(
        "PendingPayment", back_populates="residential_management_info")
