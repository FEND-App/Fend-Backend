from sqlalchemy import Integer, String, DateTime, ForeignKey, Column, Boolean, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from database import Base
from enum import Enum
from datetime import datetime


class SocialArea(Base):
    __tablename__ = 'social_areas'

    id_social_area = Column(Integer, primary_key=True, nullable=False)
    social_area = Column(String, nullable=False)

    reservation = relationship(
        'Reservation', back_populates='social_area_info')
