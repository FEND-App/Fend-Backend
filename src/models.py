from sqlalchemy import Integer, String, DateTime, ForeignKey, Column, Boolean
from src.database import Base, engine

class User(Base):
    __tablename__ = "users"

    id_user = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    creates_at = Column(DateTime)
    updated_at = Column(DateTime)