from pydantic import BaseModel, emailStr
from typing import Optional
from datetime import date, datetime

class ResidentialManagementCreate(BaseModel):
    residential: int
    first_name: str
    second_name: Optional[str] = None
    third_name: Optional[str] = None
    f_last_name: str
    s_last_name: Optional[str] = None
    born_date: date
    email: emailStr
    phone: str
    government_issued_id: str
    residential: int
    employee_star_date: datetime
    employee_mobile_phone: str
    employee_email: emailStr
    role: str
    is_active: Optional[bool] = True


class ResidentialManagementUpdate(BaseModel):
    email: Optional[emailStr] = None
    phone: Optional[str] = None
    goverment_issued_id: Optional[str] = None
    employee_mobile_phone: Optional[str] = None
    employee_email: Optional[emailStr] = None
    role: Optional[str] = None
    residential: Optional[int] = None

