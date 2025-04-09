from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

from models.news import News

class NewsUpdate(BaseModel):
    content: Optional[str] = None
    expiration_date: Optional[date] = None
    residental_management: Optional[int] = None
    status: Optional[bool] = None

