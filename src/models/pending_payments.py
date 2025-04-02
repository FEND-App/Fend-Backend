from sqlalchemy import Integer, String, DateTime, ForeignKey, Column, Boolean
from sqlalchemy.orm import relationship
from database import Base


class PendingPayment(Base):
    __tablename__ = "pending_payments"

    id_pending_payments = Column(Integer, primary_key=True, index=True)
    payment_description = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    generation_date = Column(DateTime, nullable=False)
    payment_date = Column(DateTime, nullable=False)
    is_active = Column(Boolean, nullable=True, default=True)
    residential_management = Column(Integer, ForeignKey(
        "residential_management.id_residential_management"), nullable=False)

    # Relaciones
    residential_management_info = relationship(
        "ResidentialManagement", back_populates="pending_payments")
    payment_calender_info = relationship(
        "PaymentCalender", back_populates="pending_payment_info")
