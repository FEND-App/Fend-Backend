from fastapi import FastAPI, APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional, Annotated
import models
from models.persons import Person
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
import models.persons
from models.reservation import Reservation
from models.residential_management import ResidentialManagement
from models.residents import Residents
from datetime import date

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
def get_reservations(db: db_dependency):
    reservations = db.query(Reservation).options(
        joinedload(Reservation.residential_management).joinedload(
            ResidentialManagement.person_details),
        joinedload(Reservation.social_area_info),
        joinedload(Reservation.residents).joinedload(
            Residents.person_resident_info)
    ).all()

    if not reservations:
        raise HTTPException(status_code=404, detail='Without Reservations')

    response = [{
        'id_reservation': reservation.id_reservation,
        'resident': f"{reservation.residents.person_resident_info.first_name} {reservation.residents.person_resident_info.f_last_name}" if reservation.residents and reservation.residents.person_resident_info else 'N/A',
        'social_area': f"{reservation.social_area_info.social_area}" if reservation.social_area_info and reservation.social_area_info.social_area else 'N/A',
        'event_date': f"{date.strftime(reservation.event_date, '%d-%m-%y')}",
        'event_status': reservation.event_status,
        'approved_by': f"{reservation.residential_management.person_details.first_name} {reservation.residential_management.person_details.f_last_name}" if reservation.residential_management and reservation.residential_management.person_details else 'N/A',
        'notes': reservation.notes if reservation.notes else 'N/A'
    } for reservation in reservations]

    return response
