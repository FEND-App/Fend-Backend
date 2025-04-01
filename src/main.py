from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any, Optional, Annotated
import models
from models.users import User
from routers import persons
from routers import country
from routers import city
from routers import residential_area
from routers import residential_management
from routers import employees
from routers import pending_resident_request
from routers import reservation
from database import SessionLocal, engine
from sqlalchemy.orm import Session

app = FastAPI()

app.include_router(persons.router, prefix="/persons")
app.include_router(country.router, prefix="/country")
app.include_router(city.router, prefix="/city")
app.include_router(residential_area.router, prefix="/residential_area")
app.include_router(residential_management.router,
                   prefix="/residential_management")
app.include_router(employees.router,
                   prefix="/employees")
app.include_router(pending_resident_request.router,
                   prefix="/pending_resident_request")
app.include_router(reservation.router,
                   prefix="/reservation")

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/")
def root():
    return {"Hello": "World"}


@app.get("/users/")
def get_users(db: db_dependency):
    users = db.query(User.id_user, User.username, User.is_active).all()
    return [{"id_user": User.id, "name": User.username, "Active": User.is_active} for User in users]
