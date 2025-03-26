from sqlalchemy import Integer, String, DateTime, ForeignKey, Column, Boolean
from database import Base


class Person(Base):
    __tablename__ = "persons"

    id_person = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    second_name = Column(String, nullable=True)
    third_name = Column(String, nullable=True)
    f_last_name = Column(String, index=True)
    s_last_name = Column(String, nullable=True)
    born_date = Column(DateTime, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, index=True, nullable=False)
    government_issued_id = Column(String, index=True, nullable=False)
    id_user = Column(Integer, ForeignKey("users.id_user"))
