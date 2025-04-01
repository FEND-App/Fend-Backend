from sqlalchemy import Integer, String, DateTime, ForeignKey, Column, Boolean
from database import Base
from sqlalchemy.orm import relationship

class StatusQR(str, Enum):
    Active = "Active"
    Used = "Used"
    Expired = "Expired"
    Revoked = "Revoked"

class VisitorQRCode(Base):
    __tablename__ = "visitor_QR_codes"

    qr_id = Column(Integer, primary_key=True, index=True)
    resident = Column(Integer, ForeignKey("residents.id_residents"), nullable=False)
    visitor = Column(Integer, ForeignKey("visitor.id_visitor"), nullable=False)
    #QR_code = Column(String, nullable=False) esta columna hay que eliminarla en la ddbb 
    generation_date = Column(DateTime, nullable=False)
    expiration_date = Column(DateTime, nullable=False)
    status = Column(SQLAlchemyEnum(
        StatusQR, name='StatusQR'), nullable=False)

    # Relaciones
    resident = relationship("Residents", back_populates="qr_codes")
    visitor = relationship("Visitor", back_populates="qr_codes")
