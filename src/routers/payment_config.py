from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import PaymentCalender, PendingPayment
from schemas.residential_management.payments import PendingPaymentsCreate, PaymentCalenderCreate
from database import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/configure_payment/")
def configure_payment(resident_id: int, payment_data: PaymentCalenderCreate, db: Session = Depends(get_db)):
    new_payment = PaymentCalender(
        resident=resident_id,
        pending_payment=payment_data.pending_payment,
        status=payment_data.status,
    )

    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)

    for payment in payment_data.pending_payment:
        new_pending_payment = PendingPayment(
            payment_description=payment.payment_description,
            amount=payment.amount,
            generation_date=payment.generation_date,
            payment_date=payment.payment_date,
            is_active=True,
            residential_management=resident_id,  # Corrected to use resident_id
        )

        db.add(new_pending_payment)

    db.commit()

    return {"message": "Configuración de pagos realizada con éxito"}


@router.get("/payment_info/{resident_id}")
def get_payment_info(resident_id: int, db: Session = Depends(get_db)):
    payment_calender = db.query(PaymentCalender).filter(
        PaymentCalender.resident == resident_id).first()
    if not payment_calender:
        raise HTTPException(
            status_code=404, detail="No se encontraron pagos configurados para esta residencia")

    pending_payments = db.query(PendingPayment).filter(
        PendingPayment.residential_management == resident_id).all()

    return {
        "payment_calender": payment_calender,
        "pending_payments": pending_payments
    }


@router.put("/update_payment/{resident_id}")
def update_payment(resident_id: int, payment_data: PaymentCalenderCreate, db: Session = Depends(get_db)):
    payment_calender = db.query(PaymentCalender).filter(
        PaymentCalender.resident == resident_id).first()
    if not payment_calender:
        raise HTTPException(
            status_code=404, detail="No se encontraron pagos configurados para esta residencia")

    payment_calender.pending_payment = payment_data.pending_payment
    payment_calender.status = payment_data.status

    db.commit()

    for payment in payment_data.pending_payment:
        pending_payment = db.query(PendingPayment).filter(
            PendingPayment.payment_description == payment.payment_description,
            PendingPayment.residential_management == resident_id  # Added filter for resident_id
        ).first()
        if not pending_payment:
            new_pending_payment = PendingPayment(
                payment_description=payment.payment_description,
                amount=payment.amount,
                generation_date=payment.generation_date,
                payment_date=payment.payment_date,
                is_active=True,
                residential_management=resident_id,  # Corrected to use resident_id
            )

            db.add(new_pending_payment)
        else:
            pending_payment.payment_description = payment.payment_description
            pending_payment.amount = payment.amount
            pending_payment.payment_date = payment.payment_date
            pending_payment.generation_date = payment.generation_date
            pending_payment.is_active = payment.is_active

    db.commit()

    return {"message": "Configuración de pagos actualizada con éxito"}


@router.delete("/delete_payment/{resident_id}")
def delete_payment(resident_id: int, db: Session = Depends(get_db)):
    payment_calender = db.query(PaymentCalender).filter(
        PaymentCalender.resident == resident_id).first()
    if not payment_calender:
        raise HTTPException(
            status_code=404, detail="No se encontraron pagos configurados para esta residencia")

    pending_payments = db.query(PendingPayment).filter(
        PendingPayment.residential_management == resident_id).all()
    for payment in pending_payments:
        db.delete(payment)

    db.delete(payment_calender)
    db.commit()

    return {"message": "Configuración de pagos eliminada con éxito"}
