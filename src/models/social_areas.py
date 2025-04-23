from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import relationship
from database import Base


class SocialArea(Base):
    __tablename__ = 'social_areas'

    id_social_area = Column(Integer, primary_key=True, nullable=False)
    social_area = Column(String, nullable=False)

    reservation = relationship(
        'Reservation', back_populates='social_area_info')
    residential_social_area = relationship(
       'ResidentialSocialArea', back_populates='social_areas')
