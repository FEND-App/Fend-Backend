from sqlalchemy import Integer, String, DateTime, ForeignKey, Column, Boolean
from sqlalchemy.orm import relationship
from database import Base


class ResidentialSocialArea(Base):
    __tablename__ = "residenttial_social_area"

    id_rsa = Column(
        Integer, primary_key=True, index=True, nullable=False)
    residential = Column(
        Integer, ForeignKey("residential_area.id_residential_area"), nullable=False)
    social_area = Column(
        Integer, ForeignKey("social_areas.id_social_area"), nullable=False)


    #relaciones
    residential_area = relationship(
        "ResidentialArea", back_populates="residential_social_area")
    social_areas = relationship(
        "SocialAreas", back_populates="residential_social_area")