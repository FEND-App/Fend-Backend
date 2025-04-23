from sqlalchemy import Integer, String, DateTime, ForeignKey, Column, Boolean
from database import Base


class States(Base):
    __tablename__ = "states"

    id_state = Column(Integer, primary_key=True, index=True, nullable=False)
    state_name = Column(String, index=True, nullable=False)
    id_country = Column(Integer, ForeignKey("country.id_country"))
