from fastapi import FastAPI, APIRouter, Depends
from pydantic import BaseModel
from typing import List, Dict, Any, Optional, Annotated
import models
from models.city import City
from database import SessionLocal, engine
from sqlalchemy.orm import Session

import models.persons

app = FastAPI()
router = APIRouter()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/")
def get_cities(db: db_dependency):
    cities = db.query(City).all()
    return [{"id": city.id_city, "city": city.city_name} for city in cities]
