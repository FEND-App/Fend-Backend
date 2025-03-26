from sqlalchemy import Integer, String, DateTime, ForeignKey, Column, Boolean
from database import Base


class City(Base):
    __tablename__ = "city"

    id_city = Column(Integer, primary_key=True, index=True, nullable=False)
    city_name = Column(String, index=True, nullable=False)
    id_state = Column(Integer, ForeignKey("states.id_state"))
