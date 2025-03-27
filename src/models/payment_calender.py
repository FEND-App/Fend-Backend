from sqlalchemy import Integer, String, DateTime, ForeignKey, Column, Boolean
from sqlalchemy.orm import relationship
from database import Base

class payment_calender(Base):
    __tablename__ = "payment_calender"

    id_payment_calender = Column(Integer, primary_key=True, index=True)
    residents = Column(Integer, ForeignKey("residents.id_residents"), nullable=False)
    pending_payment = Column(Integer, ForeignKey("pending_payment.id_pending_payment"), nullable=False)
    status = Column(Boolean, nullable=False)

    # Relaciones
    resident = relationship(
        "Residents", back_populates="payment_calender")
    pending_payment = relationship("PendingPayment", back_populates="payment_calender", cascade="all, delete-orphan")