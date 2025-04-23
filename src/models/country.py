from sqlalchemy import Integer, String, DateTime, ForeignKey, Column, Boolean, Enum as SQLAlchemyEnum
from database import Base, engine
from enum import Enum


class Countries(str, Enum):
    Argentina = 'Argentina'
    Bolivia = 'Bolivia'
    Brasil = 'Brasil'
    Chile = 'Chile'
    Colombia = 'Colombia'
    CostaRica = 'CostaRica'
    Cuba = 'Cuba'
    Ecuador = 'Ecuador'
    EEUU = 'EEUU'
    ElSalvador = 'ElSalvador'
    Guatemala = 'Guatemala'
    Honduras = 'Honduras'
    Mexico = 'Mexico'
    Nicaragua = 'Nicaragua'
    Panama = 'Panama'
    Paraguay = 'Paraguay'
    Peru = 'Peru'
    RepublicaDominicana = 'RepublicaDominicana'
    Uruguay = 'Uruguay'
    Venezuela = 'Venezuela'


class Country(Base):
    __tablename__ = "country"

    id_country = Column(Integer, primary_key=True, index=True, nullable=False)
    country = Column(SQLAlchemyEnum(Countries, names='countries'),
                     index=True, nullable=False)
