from fastapi import FastAPI, APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Annotated
import models
import uuid
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from models.persons import Person
from models.resident import Resident
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


@router.post('/add_resident/')
async def add_resident(data: ResidentCreate, db: Session = Depends(get_db)):
    try:
        head_resident = db.query(Resident).filter(residents.Resident.person == data.person, residents.Resident.resident_type == "Head").first()

        if not head_resident:
            raise HTTPException(status_code=403, detail="Solo el administrador del hogar puede aggregar nuevos residentes")

        person_exists = db.query(persons.Person).filter(persons.Person.person == person).first()
            if not person_exists:
                raise HTTPException(status_code=400, detail="Esta persona no esta registrada en el sistema")

        qr_data = f"ID; {data.person}; House: {data.resident_house}"
        qr = qrcode.make(qr_data)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        qr_code_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        new_resident = residents.Resident(
            person=data.person,
            resident_house=data.resident_house,
            resident_type="Occupant",
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