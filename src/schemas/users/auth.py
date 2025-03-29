from pydantic import BaseModel, EmailStr, Field, Optional, validator
from datetime import date


Class ClerkWebhook(BaseModel):
    id_person: int
    first_name: str
    second_name: Optional[str] = None
    third_name: Optional[str] = None
    f_lasta_name: str
    s_last_name: Optional[str] = None
    born_date: date
    email: EmailStr
    phone: str
    government_issued_id: str
    username: str
    password: str
    