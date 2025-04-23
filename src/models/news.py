from sqlalchemy import Integer, String, DateTime, ForeignKey, Column, Boolean
from database import Base
from datetime import datetime
from sqlalchemy.orm import relationship


class News(Base):
    __tablename__ = 'news'

    id_news = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    publication_date = Column(DateTime, nullable=False, default=datetime.now())
    expiration_date = Column(DateTime, nullable=False, default=datetime.now())
    residential_management = Column(Integer, ForeignKey(
        'residential_management.id_residential_management'), nullable=True)
    status = Column(Boolean, nullable=True, default=True)

    # Relaciones
    residential_management_info = relationship(
        'ResidentialManagement', back_populates='news')
