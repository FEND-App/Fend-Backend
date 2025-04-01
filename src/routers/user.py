from fastapi import FastAPI, APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from typing import List, Dict, Any, Optional, Annotated
from models import persons, users
from database import SessionLocal, engine
from sqlalchemy.orm import Session
import os
import hmac
import hashlib
import secrets
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

app = FastAPI()
router = APIRouter()

security = HTTPBearer()

CLERK_WEBHOOK_SECRET = os.getenv("CLERK_WEBHOOK_SECRET")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def verify_clerk_webhook(request: Request, secret: str):
    # Function to verify the webhook signature
    signature_header = request.headers.get("svix-signature", "")
    if not signature_header:
        raise HTTPException(
            status_code=400, detail="Missing signature in the header")

    try:
        parts = signature_header.split(",")
        timestamp = parts[0].split("=")[1]
        signature = parts[1].split("=")[1]

        payload = await request.body()
        signed_payload = f"{timestamp}.{payload.decode()}"

        expected_signature = hmac.new(
            secret.encode(),
            signed_payload.encode(),
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(signature, expected_signature):
            raise HTTPException(status_code=400, detail="Invalid signature")

    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error verifying signature: {e}")


@router.post('/create_user_clerk_webhook/')
async def create_user_clerk_webhook(request: Request, db: Session = Depends(get_db)):
    try:
        payload = await request.json()

        await verify_clerk_webhook(request, CLERK_WEBHOOK_SECRET)

        if "data" not in payload or "type" not in payload:
            raise HTTPException(
                status_code=400, detail="Invalid webhook payload, missing information")

        if payload["type"] != "user.created":
            return {"message": "Event is not of type user.created, ignored by the system"}

        user_data = payload["data"]

        existing_user = db.query(users.User).filter(
            users.User.id_user == user_data["id_user"]).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        new_user = users.User(
            id_user=user_data["id_user"],  # Clerk should return the ID
            username=user_data["username"],
            is_active=True
        )

        db.add(new_user)
        db.commit()

        existing_person = db.query(persons.Person).filter(
            persons.Person.id_person == user_data["id_person"]).first()
        if existing_person:
            raise HTTPException(
                status_code=400, detail="Person already exists")

        attributes = user_data.get("attributes", {})
        new_person = persons.Person(
            id_person=user_data["id_person"],
            first_name=user_data["first_name"],
            second_name=user_data["second_name"],
            third_name=user_data["third_name"],
            f_last_name=user_data["f_last_name"],
            s_last_name=user_data["s_last_name"],
            born_date=user_data["born_date"],
            email=user_data["email"],
            phone=user_data["phone"],
            government_issued_id=user_data["government_issued_id"],
            id_user=new_user.id_user
        )

        db.add(new_person)
        db.commit()

        return {"message": "User and person created successfully"}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")
