from fastapi import FastAPI, APIRouter, Depends, File, HTTPException, UploadFile, Form
from pydantic import BaseModel
from typing import List, Dict, Any, Optional, Annotated
from datetime import date
import models
from models.city import City
from database import AsyncSessionLocal, SessionLocal, engine
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from models.employees import Employee
from models.pending_resident_request import PendingResidentRequest
from models.persons import Person
from sqlalchemy.future import select

from models.residents import Residents
from models.users import User
from schemas.employees.patch_employee import EmployeePatch

app = FastAPI()
router = APIRouter()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_sync_dependency = Annotated[Session, Depends(get_db)]


@router.get('/', status_code=200)
def get_pending_request(db: db_sync_dependency):
    requests = db.query(PendingResidentRequest).options(
        joinedload(PendingResidentRequest.residents_info).joinedload(
            Residents.person_resident_info),
        joinedload(PendingResidentRequest.residents_head_info).joinedload(
            Residents.person_resident_info)
    ).all()

    if not requests:
        raise HTTPException(status_code=404, detail='Not pending requests')

    response = [{
        'id_request': req.id_request,
        'head': f"{req.residents_head_info.person_resident_info.first_name} {req.residents_head_info.person_resident_info.f_last_name}" if req.residents_head_info and req.residents_head_info.person_resident_info else 'N/A',
        'resident': f"{req.residents_info.person_resident_info.first_name} {req.residents_info.person_resident_info.f_last_name}" if req.residents_info and req.residents_info.person_resident_info else 'N/A',
        'request_date': f"{date.strftime(req.request_date, '%d-%m-%Y') if req.request_date else 'N/A'}",
        'status': req.status
    } for req in requests
    ]

    return response
