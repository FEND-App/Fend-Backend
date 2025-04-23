from sqlalchemy import Integer, String, DateTime, ForeignKey, Column, Boolean, Enum as SQLAlchemyEnum
from database import Base
from sqlalchemy.orm import relationship
from enum import Enum

class StatusQR(str, Enum):
    Active = "Active"
    Used = "Used"
    Expired = "Expired"
    Revoked = "Revoked"

class VisitorQRCode(Base):
    __tablename__ = "visitor_qr_codes"

    qr_id = Column(Integer, primary_key=True, index=True)
    resident = Column(Integer, ForeignKey("residents.id_residents"), nullable=False)
    visitor = Column(Integer, ForeignKey("visitor.id_visitor"), nullable=False)
    #QR_code = Column(String, nullable=False) esta columna hay que eliminarla en la ddbb 
    generation_date = Column(DateTime, nullable=False)
    expiration_date = Column(DateTime, nullable=False)
    status = Column(SQLAlchemyEnum(
        StatusQR, name='StatusQR'), nullable=False)

    # Relaciones
    resident_id = relationship("Residents", back_populates="visitor_qr_codes")
    visitor_id = relationship("Visitor", back_populates="visitor_qr_codes")
