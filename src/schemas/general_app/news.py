from pydantic import BaseModel, optional, Field
from datetime import date

from models.news import News

class NewsUpdate(BaseModel):
    content: optional[str] = None
    expiration_date: optional[date] = None
    residental_management: optional[int] = None
    status: optional[bool] = None

