from fastapi import FastAPI, APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Annotated
import models
import models.city
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from models.residential_management import ResidentialManagement
import models.residential_management
from sqlalchemy.orm import joinedload
from datetime import date, datetime

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


@router.get('/')
def get_managements(db: db_dependency):
    try:
        # managements = db.query(ResidentialManagement).filter(ResidentialManagement.is_active == True).all()
        managements = db.query(ResidentialManagement
                               ).options(
            joinedload(ResidentialManagement.residential_area),
            joinedload(ResidentialManagement.person_details)
        ).filter(ResidentialManagement.is_active == True).all()

        response = [
            {
                "name": f"{management.person_details.first_name} {management.person_details.f_last_name}",
                "residential": f"{management.residential_area.name_residential_area}",
                "start_date": f"{date.strftime(management.employee_star_date, '%d-%m-%Y')}",
                "phone": f"{management.employee_mobile_phone}",
                "email": f"{management.employee_email}",
                "role": f"{management.role}"
            }
            for management in managements
        ]

        return response
    except (Exception) as e:
        return {
            "message": str(e)
        }


@router.get('/{id_management}')
def get_managements(id_management: int, db: db_dependency):
    management = db.query(ResidentialManagement).options(
        joinedload(ResidentialManagement.person_details)
    ).filter(ResidentialManagement.id_residential_management == id_management).first()

    if not management:
        raise HTTPException(status_code=404, detail="Management not found")

    response = {
        "name": f"{management.person_details.first_name} {management.person_details.f_last_name}",
        "residential": f"{management.residential_area.name_residential_area}",
        "start_date": f"{date.strftime(management.employee_star_date, '%d-%m-%Y')}",
        "phone": f"{management.employee_mobile_phone}",
        "email": f"{management.employee_email}",
        "role": f"{management.role}"
    }

    return response
