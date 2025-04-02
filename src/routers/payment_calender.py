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
from datetime import date

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
