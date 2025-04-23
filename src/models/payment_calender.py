from sqlalchemy import Integer, String, DateTime, ForeignKey, Column, Boolean
from sqlalchemy.orm import relationship
from database import Base


class PaymentCalender(Base):
    __tablename__ = "payment_calendar"

    id_payment_calendar = Column(Integer, primary_key=True, index=True)
    resident = Column(Integer, ForeignKey(
        "residents.id_residents"), nullable=False)
    pending_payments = Column(Integer, ForeignKey(
        "pending_payments.id_pending_payments"), nullable=False)
    status = Column(Boolean, nullable=False)

    # Relaciones
    pending_payment_info = relationship(
        "PendingPayment", back_populates="payment_calender_info", foreign_keys=[pending_payments]
    )

    resident_info = relationship(
        "Residents", back_populates="payment_calender_info", foreign_keys=[resident])
