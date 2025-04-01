from sqlalchemy import Integer, String, DateTime, ForeignKey, Column, Boolean
from database import Base
from sqlalchemy.orm import relationship

class Visitor(Base):
    __tablename__ = "visitor"

    id_visitor = Column(Integer, primary_key=True, index=True)
    id_document = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    second_name = Column(String, nullable=True)
    last_name = Column(String, nullable=False)
    second_last_name = Column(String, nullable=True)
    phone_number = Column(String, nullable=False)
    is_adult = Column(Boolean, nullable=False, default=False)
    Picture = Column(LargeBinary, nullable=True)


    qr_codes = relationship("visitor_QR_codes", back_populates="visitor")

