from sqlalchemy import Integer, String, DateTime, ForeignKey, Column, Boolean, LargeBinary
from database import Base
from sqlalchemy.orm import relationship

class Visitor(Base):
    __tablename__ = "visitor"

    id_visitor = Column(Integer, primary_key=True, index=True)
    id_document = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    second_name = Column(String, nullable=True)
    first_lastname = Column(String, nullable=False)
    second_lastname = Column(String, nullable=True)
    phone_number = Column(String, nullable=False)
    is_adult = Column(Boolean, nullable=False, default=False)
    picture = Column(LargeBinary, nullable=True)


    visitor_qr_codes = relationship("VisitorQRCode", back_populates="visitor_id")

