from sqlalchemy import Integer, String, DateTime, ForeignKey, Column, Boolean
from sqlalchemy.orm import relationship
from database import Base
from datetime import date, datetime


class PendingResidentRequest(Base):
    __tablename__ = 'pending_resident_request'

    id_request = Column(Integer, primary_key=True)
    head = Column(Integer, ForeignKey(
        'residents.id_residents'), nullable=False)
    resident = Column(Integer, ForeignKey(
        'residents.id_residents'), nullable=False)
    request_date = Column(DateTime, nullable=False, default=datetime.now())
    status = Column(Boolean, nullable=True)

    # Relación con Residents (como residente)
    residents_info = relationship(
        'Residents',
        back_populates='pending_reqs',
        # Aqui Especificamos la clave foránea ya que hay mas de una relación
        foreign_keys=[resident]
    )

    # Relación con Residents (como cabeza de familia)
    residents_head_info = relationship(
        'Residents',
        back_populates='pending_reqs_head',
        # Aqui Especificamos la clave foránea ya que hay mas de una relación
        foreign_keys=[head]
    )
