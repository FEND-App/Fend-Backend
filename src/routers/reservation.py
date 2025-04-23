from fastapi import FastAPI, APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional, Annotated
import models
from models.persons import Person
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
import models.persons
from models.reservation import Reservation, ReservationStatus
from models.residential_management import ResidentialManagement
from models.residents import Residents
from datetime import datetime, date
from schemas.general_app.events import CreateReservation

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


@router.patch('/{id_reservation}')
def approve_reservation(id_reservation: int, status: ReservationStatus, updated_by: int, db: db_dependency):
    find_reservation = db.query(Reservation).filter(
        Reservation.id_reservation == id_reservation).first()

    find_person = db.query(ResidentialManagement).filter(
        ResidentialManagement.id_residential_management == updated_by).first()

    if not find_reservation:
        raise HTTPException(status_code=404, detail='Reservation not found')

    if not find_person:
        raise HTTPException(
            status_code=404, detail='Residential Management not found')

    try:
        find_reservation.event_status = status
        find_reservation.approved_by = updated_by

        db.commit()
        db.refresh(find_reservation)

        return {
            'id_reservation': find_reservation.id_reservation,
            'event_status': find_reservation.event_status,
            'message': 'Reservation status updated successfully'
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")



@router.get('/social_areas/{id_residential_area}')
async def list_social_areas(id_residential_area: int, db: Session = Depends(get_db)):
    try:
        areas = db.query(
            models.SocialArea
        ).join(
            models.ResidentialSocialArea,
            models.ResidentialSocialArea.social_area == models.SocialArea.id_social_area
        ).filter(
            models.ResidentialSocialArea.residential == id_residential_area
        ).all()

        return [
            {
                "id_social_area": area.id_social_area,
                "social_area": area.social_area
            } for area in areas
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching areas: {str(e)}")


@router.post('/create_Reservation/')
async def create_reservation(data: CreateReservation, db: Session = Depends(get_db)):
    try:
        social_area = db.query(models.SocialArea).filter(
            models.SocialArea.id_social_area == data.social_area_info
        ).first()

        if not social_area:
            raise HTTPException(status_code=404, detail="Error: Social area not found")

        reservation = models.Reservation(
            id_resident=data.id_residents,
            id_area=data.social_area,
            event_date=data.event_date,
            event_status="Pending",
            created_at=datetime.now(),
            notes=data.notes
        )

        db.add(reservation)
        db.commit()
        db.refresh(reservation)

        return {
            "message": "Reservation created successfully",
            "reservation_id": reservation.id_reservation
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno del sistema: {str(e)}")
