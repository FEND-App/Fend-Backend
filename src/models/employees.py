from sqlalchemy import Integer, String, DateTime, ForeignKey, Column, Boolean, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.dialects.postgresql import BYTEA
from enum import Enum


class Positions(str, Enum):
    Guard = 'Guard'
    Maintenance = 'Maintenance'
    Landscaping = 'Landscaping'
    Cleaning = 'Cleaning'


class Employee(Base):
    __tablename__ = "employees"

    id_employee = Column(Integer, primary_key=True)
    person = Column(Integer, ForeignKey("users.id_user"), nullable=False)
    position = Column(SQLAlchemyEnum(
        Positions, names="positions"), nullable=False)
    hire_date = Column(DateTime, nullable=False)
    employee_mobile_phone = Column(String(30), nullable=True)
    photo = Column(BYTEA, nullable=False)
    is_active = Column(Boolean, nullable=True, default=True)

    # Relaciones
    users_details = relationship("User", back_populates="employees")
