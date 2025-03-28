from pydantic import BaseModel
from typing import Annotated
from fastapi import Form
from datetime import date

from models.employees import Positions


class EmployeeCreate(BaseModel):
    person: Annotated[int, Form()]
    position: Annotated[Positions, Form()]
    hire_date: Annotated[date, Form()]
    employee_mobile_phone: Annotated[str, Form()]
