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
from models.persons import Person
from sqlalchemy.future import select

from models.users import User

app = FastAPI()
router = APIRouter()

models.Base.metadata.create_all(bind=engine)


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

async def get_async_db():
    async with AsyncSessionLocal() as db:
        yield db


db_dependency = Annotated[AsyncSession, Depends(get_async_db)]


@router.get('/')
async def get_employees(db: db_dependency):
    query = select(Employee).options(joinedload(Employee.users_details))
    result = await db.execute(query)  # Usa `await` para ejecutar la consulta
    employees = result.scalars().all()

    return [
        {
            "id": employee.id_employee,
            # "name": f"{employee.person_details.first_name} {employee.person_details.f_last_name}",
            "position": employee.position,
            "hire_date": f"{date.strftime(employee.hire_date, '%d-%m-%Y')}",
            "phone": employee.employee_mobile_phone,
            "photo": employee.photo,
            "is_active": employee.is_active
        }
        for employee in employees
    ]


@router.post('/')
async def create_employee(
    person: Annotated[int, Form()],
    position: Annotated[str, Form()],
    hire_date: Annotated[date, Form()],
    employee_mobile_phone: Annotated[str, Form()],
    # Archivo manejado como parámetro independiente
    photo: Annotated[UploadFile, File()],
    db: db_dependency
):
    try:
        # Verificar si la persona existe
        result = await db.execute(select(User).filter(User.id_user == person))
        find_person = result.scalars().first()

        if not find_person:
            raise HTTPException(status_code=404, detail="Person not found")

        print(position)
        print(find_person.id_user)

        # Leer el archivo como datos binarios
        photo_data = await photo.read()

        # Crear el nuevo empleado
        new_employee = Employee(
            person=person,
            position=position,
            hire_date=hire_date,
            employee_mobile_phone=employee_mobile_phone,
            photo=photo_data  # Guardar los datos binarios en la columna BYTEA
        )

        db.add(new_employee)
        await db.commit()
        await db.refresh(new_employee)

        return {
            "message": "Employee created successfully",
            "data": {
                "id": new_employee.id_employee,
                "person": new_employee.person,
                "position": new_employee.position,
                "hire_date": new_employee.hire_date,
                "employee_mobile_phone": new_employee.employee_mobile_phone,
                "is_active": new_employee.is_active,
            }
        }
        # return 0
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
