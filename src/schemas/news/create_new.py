from typing import Optional
from pydantic import BaseModel
from datetime import date


class NewCreate(BaseModel):
    title: str
    content: str
    publication_date: date
    expiration_date: date
    residential_management: int = None,
    status: bool = True
