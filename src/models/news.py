from sqlalchemy import Integer, String, DateTime, ForeignKey, Column, Boolean
from sqlalchemy.orm import relationship
from database import Base


class news(Base):
    __tablename__ = "news"

    id_news = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    publication_date = Column(DateTime, nullable=False)
    expiration_date = Column(DateTime, nullable=False)
    residental_management = Column(Integer, ForeignKey("residential_management.id_residential_management"), nullable=False)
    status = Column(Boolean, nullable=False)

    # Relaciones
    residential_management = relationship("ResidentialManagement", back_populates="news")