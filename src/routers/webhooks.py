from fastapi import APIRouter, HTTPException, Request, Response, Depends, status
from typing import Dict, Any
from svix.webhooks import Webhook, WebhookVerificationError
import os

from sqlalchemy.orm import Session
from database import SessionLocal
from datetime import datetime
from models.users import User

router = APIRouter()

# This should be set as an environment variable
secret = os.getenv("CLERK_WEBHOOK_SECRET")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/clerk/webhook")
async def clerk_webhook(request: Request, response: Response, db: Session = Depends(get_db)):
    headers = request.headers
    payload = await request.body()

    try:
        wh = Webhook(secret)
        msg = wh.verify(payload, headers)
        
        userData = msg.get("data")
        
        new_user = User(
            username=userData.get("email_addresses")[0].get("email_address"),
            clerk_id=userData.get("id"),
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
            
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
    except WebhookVerificationError as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return
    