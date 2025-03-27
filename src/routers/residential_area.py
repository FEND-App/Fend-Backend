from fastapi import FastAPI, APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional, Annotated
import models
import models.city
from models.residential_area import ResidentialArea
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from schemas.residential_area.create_residential_area import ResidentialAreaCreate
from schemas.residential_area.patch_residential_area import ResidentialAreaPatch

import models.persons

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


@router.get("/")
def get_residential_areas(db: db_dependency):
    residential_areas = db.query(ResidentialArea).all()
    return [
        {
            "id": residential_area.id_residential_area,
            "residential_area": residential_area.name_residential_area,
            "active": residential_area.is_active,
            "city": residential_area.city_residential_area,
            "total_houses": residential_area.total_houses
        } for residential_area in residential_areas
    ]


@router.get("/{id_residential_area}")
def get_residential_area(id_residential_area: int, db: db_dependency):
    residential_area = db.query(ResidentialArea).filter(
        ResidentialArea.id_residential_area == id_residential_area).first()
    if not residential_area:
        raise HTTPException(status_code=404, detail="Residential not found")

    return {
        "id": residential_area.id_residential_area,
        "residential_area": residential_area.name_residential_area,
        "active": residential_area.is_active,
        "city": residential_area.city_residential_area,
        "total_houses": residential_area.total_houses
    }


@router.post("/", status_code=201)
def create_residential_area(residential_area: ResidentialAreaCreate, db: db_dependency):
    try:

        city = db.query(models.city.City).filter(
            models.city.City.id_city == residential_area.city_residential_area).first()
        if not city:
            return {"message": "City not found"}

        last_residential_area = db.query(ResidentialArea).order_by(
            ResidentialArea.id_residential_area.desc()).first()

        new_id_residential_area = last_residential_area.id_residential_area + \
            1 if last_residential_area else 1

        residential_area.id_residential_area = new_id_residential_area

        new_residential_area = ResidentialArea(
            id_residential_area=residential_area.id_residential_area,
            name_residential_area=residential_area.name_residential_area,
            city_residential_area=residential_area.city_residential_area,
            total_houses=residential_area.total_houses
        )

        db.add(new_residential_area)
        db.commit()
        db.refresh(new_residential_area)
        return {
            "message": "Residential area created successfully",
            "data": new_residential_area
        }
    except (Exception) as e:
        db.rollback()
        return {"message": str(e)}


@router.patch("/{id_residential_area}", status_code=200)
def update_residential_area(id_residential_area: int, residential: ResidentialAreaPatch, db: db_dependency):
    find_residential_area = db.query(ResidentialArea).filter(
        ResidentialArea.id_residential_area == id_residential_area).first()

    if not find_residential_area:
        raise HTTPException(status_code=404, detail="Residential not found")

    update_data = residential.dict(exclude_unset=True)

    try:
        for key, value in update_data.items():
            find_residential_area.__setattr__(key, value)

        db.commit()
        db.refresh(find_residential_area)

        return {
            "message": "Residential area updated successfully",
            "data": find_residential_area
        }
    except (Exception) as e:
        db.rollback()
        return {"message": str(e)}


@router.delete("/{id_residential_area}")
def delete_residential_area(id_residential_area: int, db: db_dependency):
    find_residential_area = db.query(ResidentialArea).filter(
        ResidentialArea.id_residential_area == id_residential_area).first()

    if not find_residential_area:
        raise HTTPException(status_code=404, detail="Residential not found")

    try:
        db.delete(find_residential_area)
        db.commit()

        return {
            "message": "Residential deleted successfully"
        }
    except (Exception) as e:
        db.rollback()
        return {"message": str(e)}
