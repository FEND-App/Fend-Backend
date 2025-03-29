from fastapi import FastAPI, APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Annotated
import models
import models.city
import uuid
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from models.persons import Person
from models.residential_management import ResidentialManagement
from models.resident import Resident
from sqlalchemy.orm import joinedload
from datetime import date, datetime

from schemas.residential_management.residential_management import (
    ResidentialManagementCreate,
    ResidentialManagementUpdate,
    ResidentialManagementResponse,
)

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


@router.post('/residential_management/', response_model=ResidentialManagementResponse)
def create__residential_management(data: ResidentialManagementCreate, db: db_dependency):
    new_person = Person(
        first_name=data.first_name,
        second_name=data.second_name,
        third_name=data.third_name,
        f_last_name=data.f_last_name,
        s_last_name=data.s_last_name,
        born_date=data.born_date,
        email=data.email,
        phone=data.phone,
        government_issued_id=data.government_issued_id
    )

    db.add(new_person)
    db.commit()
    db.refresh(new_person)

    new_management = ResidentialManagement(
        residential=data.residential,
        person=new_person.id_person,
        employee_star_date=data.employee_star_date,
        employee_mobile_phone=data.employee_mobile_phone,
        employee_email=data.employee_email,
        role=data.role
    )

    db.add(new_management)
    db.commit()
    db.refresh(new_management)

    return new_management


@router.get('/')
def get_managements(db: db_dependency):
    try:
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


@router.put('/residential_management/{id_management}', response_model=ResidentialManagementResponse)
def update_management(id_management: int, data: ResidentialManagementUpdate, db: db_dependency):
    try:
        management = db.query(ResidentialManagement).filter(
            ResidentialManagement.id_residential_management == id_management).first()

        if not management:
            raise HTTPException(status_code=404, detail="Management no existe")

        person = db.query(models.Person).filter(
            models.Person.id_person == management.person).first()

        if not person:
            raise HTTPException(status_code=404, detail="Persona no existe")

        if data.email:
            person.email = data.email
        if data.phone:
            person.phone = data.phone
        if data.government_issued_id:
            person.government_issued_id = data.government_issued_id

        if data.employee_mobile_phone:
            management.employee_mobile_phone = data.employee_mobile_phone
        if data.employee_email:
            management.employee_email = data.employee_email
        if data.role:
            management.role = data.role
        if data.residential:
            management.residential = data.residential
        if data.is_active is not None:
            management.is_active = data.is_active

        db.commit()
        db.refresh(management)

        return management

    except (Exception) as e:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Error al actualizar el management: {str(e)}")



@router.post('/add_head_resident/')
async def add_head_resident(data: ResidentCreate, db: Session = Depends(get_db)):
    try:
        existing_head = db.query(residents.Resident).filter(residents.Resident.resident_type == "Head", residents.Resident.resident_house == data.resident_house).first()

        if existing_head:
            raise HTTPException(status_code=400, detail="Ya existe un residente principal para esta residencia")

        person_exists = db.query(persons.Person).filter(persons.Person.person == data.person).first()
        if person_exists:
            raise HTTPException(status_code=400, detail="Esta persona no esta registrada en el sistema")

        qr_data = f"ID; {data.person}; House: {data.resident_house}"
        qr = qrcode.make(qr_data)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        qr_code_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        new_resident = residents.Resident(
            person=data.person,
            resident_house=data.resident_house,
            resident_type="Head",
            is_active=True,
            resident_qr=qr_code_base64,
        )

        db.add(new_resident)
        db.commit()

        return {"message": "Residente principal agregado con exito", "resident_qr": qr_code_base64}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del sistemA: {str(e)}")