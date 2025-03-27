from sqlalchemy import Integer, String, DateTime, ForeignKey, Column, Boolean
from sqlalchemy.orm import relationship
from database import Base


class ResidentialArea(Base):
    __tablename__ = "residential_area"

    id_residential_area = Column(
        Integer, primary_key=True, index=True, nullable=False)
    name_residential_area = Column(String, index=True, nullable=False)
    is_active = Column(Boolean, default=True, nullable=True)
    city_residential_area = Column(
        Integer, ForeignKey("city.id_city"), nullable=False)
    total_houses = Column(Integer, nullable=False)

    # Relaciones
    managements = relationship(
        "ResidentialManagement", back_populates="residential_area")
