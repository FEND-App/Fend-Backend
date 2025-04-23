from sqlalchemy import Integer, String, DateTime, ForeignKey, Column, Boolean
from database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id_user = Column(Integer, primary_key=True, index=True)
    clerk_id = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    # password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    # Relaciones
    employees = relationship("Employee", back_populates="users_details")
    persons_info = relationship("Person", back_populates="info_user", uselist=False)
