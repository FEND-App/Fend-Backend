from pydantic import BaseModel
from typing import Optional
from datetime import date
from models.employees import Positions


class EmployeePatch(BaseModel):
    position: Optional[Positions] = None
    hire_date: Optional[date] = None
    employee_mobile_phone: Optional[str] = None
    is_active: Optional[bool] = None

    model_config = {
        "from_attributes": True
    }
