from fastapi import FastAPI, APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Annotated
import models
import uuid
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from models.persons import Person
from models.residents import Residents
from models.visitor import Visitor
from models.visitor_qr_codes import VisitorQRCode
from sqlalchemy.orm import joinedload
from datetime import date, datetime, timedelta
import qrcode
from io import BytesIO
import base64

from schemas.residents.new_visitor import NewVisitorRegistration
from schemas.residents.new_resident import ResidentCreate

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
        head_resident = db.query(Residents).filter(
            Residents.person == data.person,
            Residents.resident_type == "Head"
        ).first()

        if not head_resident:
            raise HTTPException(
                status_code=403,
                detail="Solo el administrador del hogar puede agregar nuevos residentes"
            )

        person_exists = db.query(Person).filter(
            Person.id_person == data.person
        ).first()

        if not person_exists:
            raise HTTPException(
                status_code=400,
                detail="Esta persona no está registrada en el sistema"
            )

        qr_data = f"ID: {data.person}; House: {data.resident_house}"
        qr = qrcode.make(qr_data)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        qr_code_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        new_resident = Residents(
            person=data.person,
            resident_house=data.resident_house,
            resident_type="Occupant",
            is_active=True,
            resident_qr=qr_code_base64,
        )

        db.add(new_resident)
        db.commit()

        return {
            "message": "Residente agregado con éxito",
            "resident_qr": qr_code_base64
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del sistema: {str(e)}"
        )

@router.post('/Visitor_registration/')
async def Visitor_registration(data: NewVisitorRegistration, db: Session = Depends(get_db)):
    try:
        resident = db.query(Residents).filter(
            Residents.id_residents == data.resident_id
        ).first()

        if not resident:
            raise HTTPException(
                status_code=404,
                detail="Residente no registrado en el sistema"
            )

        new_visitor = Visitor(
            id_document=data.id_document,
            first_name=data.first_name,
            second_name=data.second_name,
            first_lastname=data.first_lastname,
            second_lastname=data.second_lastname,
            phone_number=data.phone_number,
            is_adult=data.is_adult,
            picture=data.picture        
        )

        db.add(new_visitor)
        db.commit()
        db.refresh(new_visitor)

        new_visitor_qr = VisitorQRCode(   #hay que modificar esta tabla en la ddbb y eliminar la columna QR_code, no es necesaria ya que se genera en el momento
            resident=resident.id_residents,
            visitor=new_visitor.id_visitor,
            generation_date=datetime.now(),
            expiration_date=datetime.now() + timedelta(days=15),
            status=data.StatuQR
        )

        db.add(new_visitor_qr)
        db.commit()
        db.refresh(new_visitor_qr)


        qr_data = f"QR_ID: {new_visitor_qr.qr_id}; | ID: {new_visitor.id_visitor}; | Resident: {resident.id_residents}"
        qr = qrcode.make(qr_data)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        qr_code_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
 
        return {
            "message": "Visitante registrado con éxito",
            "visitor_qr": qr_code_base64,
            "visitor_id": new_visitor.id_visitor #retorna este valor por si la camara del celular del guardia se arruino que solo ingrese el id y que reciba la data
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno del sistema: {str(e)}")




