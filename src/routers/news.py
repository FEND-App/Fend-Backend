from fastapi import FastAPI, APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional, Annotated
import models
from models.news import News
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
def get_news(db: db_dependency):
    find_news = db.query(News).options(
        joinedload(News.residential_management_info).joinedload(
            ResidentialManagement.person_details)
    ).all()

    if not find_news:
        raise HTTPException(status_code=404, detail='Without News')

    response = [{
        'id_news': new.id_news,
        'title': new.title,
        'content': new.content,
        'publication_date': f"{date.strftime(new.publication_date, '%d-%m-%y')}",
        'expiration_date': f"{date.strftime(new.expiration_date, '%d-%m-%y')}",
        'residential_management': f"{new.residential_management_info.person_details.first_name} {new.residential_management_info.person_details.f_last_name}" if new.residential_management_info and new.residential_management_info.person_details else 'N/A',
        'status': new.status
    } for new in find_news]

    return response

@router.get('/{id_new}')
def get_new_by_id(id_new: int, db: db_dependency):
    find_new = db.query(News).options(
        joinedload(News.residential_management_info).joinedload(
            ResidentialManagement.person_details)
    ).filter(News.id_news == id_new).first()
    
    if not find_new:
        raise HTTPException(status_code=404, detail="New not found")
    
    response = {
        'id_news': find_new.id_news,
        'title': find_new.title,
        'content': find_new.content,
        'publication_date': f"{date.strftime(find_new.publication_date, '%d-%m-%y')}",
        'expiration_date': f"{date.strftime(find_new.expiration_date, '%d-%m-%y')}",
        'residential_management': f"{find_new.residential_management_info.person_details.first_name} {find_new.residential_management_info.person_details.f_last_name}" if find_new.residential_management_info and find_new.residential_management_info.person_details else 'N/A',
        'status': find_new.status
    }
    
    return response


@router.post('/')
def create_new(data: NewCreate, db: db_dependency):
    if data.residential_management:
        find_management = db.query(ResidentialManagement).filter(
            ResidentialManagement.id_residential_management == data.residential_management).first()

        if not find_management:
            raise HTTPException(
                status_code=404, detail='Residential Management not found')

    try:

        creating_new = News(
            title=data.title,
            content=data.content,
            publication_date=date.isoformat(data.publication_date),
            expiration_date=date.isoformat(data.expiration_date),
            residential_management=data.residential_management,
            status=data.status
        )

        db.add(creating_new)
        db.commit()
        db.refresh(creating_new)

        return {
            'id_news': creating_new.id_news,
            'title': creating_new.title,
            'content': creating_new.content,
            'publication_date': f"{date.strftime(creating_new.publication_date, '%d-%m-%y')}",
            'expiration_date': f"{date.strftime(creating_new.expiration_date, '%d-%m-%y')}",
            'residential_management': f"{creating_new.residential_management_info.person_details.first_name} {creating_new.residential_management_info.person_details.f_last_name}" if creating_new.residential_management_info and creating_new.residential_management_info.person_details else 'N/A',
        }

    except (Exception) as e:
        db.rollback()
        return {
            'message': str(e)
        }
