from fastapi import FastAPI, APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional, Annotated

from sqlalchemy import and_
import models
from models.news import News
from models.payment_calender import PaymentCalender
from models.pending_payments import PendingPayment
from models.persons import Person
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
import models.persons
from models.reservation import Reservation, ReservationStatus
from models.residential_management import ResidentialManagement
from models.residents import Residents
from datetime import date, datetime

from schemas.news.create_new import NewCreate

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
def get_payment_calender(db: db_dependency, id_resident: int = None, pendings: bool = False):
    query = db.query(PaymentCalender).options(
        joinedload(PaymentCalender.pending_payment_info).joinedload(
            PendingPayment.residential_management_info).joinedload(ResidentialManagement.person_details),
        joinedload(PaymentCalender.resident_info).joinedload(
            Residents.person_resident_info)
    )

    filters = []

    if id_resident:
        filters.append(PaymentCalender.resident == id_resident)

    if pendings:
        filters.append(PaymentCalender.status == True)

    if filters:
        query = query.filter(and_(*filters))

    payments_calender = query.all()

    if not payments_calender:
        raise HTTPException(status_code=404, detail="No payments available...")

    result = []

    for payment in payments_calender:
        resident_found = False
        for item in result:
            if item["resident"] == payment.resident:

                pending_pay = {
                    "id_pending_payments": payment.pending_payment_info.id_pending_payments,
                    "amount": payment.pending_payment_info.amount,
                    "payment_date": payment.pending_payment_info.payment_date,
                    "residential_management": f"{payment.pending_payment_info.residential_management_info.person_details.first_name} {payment.pending_payment_info.residential_management_info.person_details.f_last_name}",
                    "payment_description": payment.pending_payment_info.payment_description,
                    "generation_date": payment.pending_payment_info.generation_date,
                    "is_active": payment.pending_payment_info.is_active,
                    "id_payment_calendar": payment.id_payment_calendar,
                    "status_payment_calendar": payment.status
                }

                item["pending_payments"].append(pending_pay)
                resident_found = True
                break

        if not resident_found:
            result.append({
                "resident": payment.resident,
                "resident_name": f"{payment.resident_info.person_resident_info.first_name} {payment.resident_info.person_resident_info.f_last_name}",
                "pending_payments": [{
                    "id_pending_payments": payment.pending_payment_info.id_pending_payments,
                    "amount": payment.pending_payment_info.amount,
                    "payment_date": payment.pending_payment_info.payment_date,
                    "residential_management": f"{payment.pending_payment_info.residential_management_info.person_details.first_name} {payment.pending_payment_info.residential_management_info.person_details.f_last_name}",
                    "payment_description": payment.pending_payment_info.payment_description,
                    "generation_date": payment.pending_payment_info.generation_date,
                    "is_active": payment.pending_payment_info.is_active,
                    "id_payment_calendar": payment.id_payment_calendar,
                    "status_payment_calendar": payment.status
                }],
            })

    return result


@router.get('/payment/dates/{id_resident}')
def get_payment_dates(id_resident: int, db: db_dependency):
    find_resident = db.query(Residents).filter(
        Residents.id_residents == id_resident).first()

    if not find_resident:
        raise HTTPException(status_code=404, detail="Resident not found")

    get_dates = db.query(PaymentCalender).options(
        joinedload(PaymentCalender.resident_info).joinedload(
            Residents.person_resident_info),
        joinedload(PaymentCalender.pending_payment_info)
    ).filter(and_(PaymentCalender.resident == id_resident, PendingPayment.is_active == True, PaymentCalender.status == False)).all()

    if not get_dates:
        raise HTTPException(
            status_code=404, detail="Pending payments not found")

    result = []

    for payment in get_dates:
        pending_pay = {
            "id_pending_payment": payment.pending_payment_info.id_pending_payments,
            "payment_date": f"{date.strftime(payment.pending_payment_info.payment_date, '%d-%m-%Y')}",
            "payment_description": payment.pending_payment_info.payment_description,
            "amount": payment.pending_payment_info.amount,
            "is_late": True if payment.pending_payment_info.payment_date < date.today() else False
        }

        result.append(pending_pay)

    response = {
        "id_resident": get_dates[0].resident,
        "name": f"{get_dates[0].resident_info.person_resident_info.first_name} {get_dates[0].resident_info.person_resident_info.f_last_name}",
        "pending_payments": result
    }

    return response


@router.patch('/pay/{id_resident}/{id_payment_calendar}')
def pay(id_resident: int, id_payment_calendar: int, db: db_dependency):
    find_resident = db.query(Residents).filter(
        Residents.id_residents == id_resident).first()

    if not find_resident:
        raise HTTPException(status_code=404, detail="Resident not found")

    try:
        get_payment_calender = db.query(PaymentCalender).filter(and_(PaymentCalender.resident == id_resident, PendingPayment.is_active ==
                                                                     True, PaymentCalender.status == False, PaymentCalender.id_payment_calendar == id_payment_calendar)).first()

        if not get_payment_calender:
            raise HTTPException(
                status_code=404, detail="Payment calender not found")

        get_pending_payment = db.query(PendingPayment).filter(
            PendingPayment.id_pending_payments == get_payment_calender.pending_payments).first()

        if not get_pending_payment:
            raise HTTPException(
                status_code=404, detail="Pending payments not found")

        get_payment_calender.status = True
        get_pending_payment.is_active = False

        db.commit()
        db.refresh(get_payment_calender)
        db.refresh(get_pending_payment)

        return {
            "message": "Payment successfully processed",
            "payment_calendar": {
                "id_payment_calendar": get_payment_calender.id_payment_calendar,
                "status": get_payment_calender.status
            },
            "pending_payment": {
                "id_pending_payment": get_pending_payment.id_pending_payments,
                "is_active": get_pending_payment.is_active
            }
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")
